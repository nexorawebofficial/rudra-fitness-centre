import datetime

from django.shortcuts import render
from django.utils import timezone

from members.models import MemberProfile

from .models import Attendance
from .tokens import resolve_checkin_token


def checkin_scan(request, token):
    member_id = resolve_checkin_token(token)
    if not member_id:
        return render(request, 'attendance/checkin_result.html', {
            'success': False, 'message': "This QR code is invalid or has expired. Please contact the front desk.",
        }, status=400)

    try:
        profile = MemberProfile.objects.select_related('user').get(member_id=member_id)
    except MemberProfile.DoesNotExist:
        return render(request, 'attendance/checkin_result.html', {
            'success': False, 'message': "Member not found.",
        }, status=404)

    if not profile.is_active:
        return render(request, 'attendance/checkin_result.html', {
            'success': False, 'message': f"{profile.full_name}'s account is deactivated. Please see the front desk.",
        })

    recent_cutoff = timezone.now() - datetime.timedelta(hours=4)
    already_checked_in = Attendance.objects.filter(member=profile, check_in_time__gte=recent_cutoff).exists()

    if already_checked_in:
        return render(request, 'attendance/checkin_result.html', {
            'success': True, 'already': True, 'profile': profile,
            'message': f"{profile.full_name} already checked in recently.",
        })

    Attendance.objects.create(member=profile, method=Attendance.METHOD_QR)
    return render(request, 'attendance/checkin_result.html', {
        'success': True, 'already': False, 'profile': profile,
        'message': f"Welcome, {profile.full_name}! Attendance recorded.",
    })
