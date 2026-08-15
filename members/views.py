import io

import qrcode
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse

from attendance.tokens import generate_checkin_token
from notifications.models import Notification

from .services import calculate_rudra_score


@login_required
def dashboard(request):
    profile = getattr(request.user, 'member_profile', None)
    membership = None
    notifications = []
    rudra_score = None
    if profile:
        membership = profile.memberships.order_by('-created_at').first()
        notifications = Notification.objects.filter(recipient=request.user)[:10]
        rudra_score = calculate_rudra_score(profile)

    return render(request, 'members/dashboard.html', {
        'profile': profile,
        'membership': membership,
        'notifications': notifications,
        'rudra_score': rudra_score,
    })


@login_required
def membership_card(request):
    profile = getattr(request.user, 'member_profile', None)
    if not profile:
        return render(request, 'members/no_profile.html')
    membership = profile.current_membership or profile.memberships.order_by('-created_at').first()
    return render(request, 'members/card.html', {'profile': profile, 'membership': membership})


@login_required
def membership_card_qr(request):
    profile = getattr(request.user, 'member_profile', None)
    if not profile:
        return HttpResponseNotFound()

    token = generate_checkin_token(profile.member_id)
    checkin_url = request.build_absolute_uri(reverse('checkin_scan', args=[token]))

    img = qrcode.make(checkin_url, box_size=8, border=2)
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    return HttpResponse(buffer.getvalue(), content_type='image/png')
