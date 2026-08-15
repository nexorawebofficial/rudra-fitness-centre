import datetime
from decimal import Decimal

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.db.models import Count, Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from attendance.models import Attendance
from members.models import MemberProfile
from memberships.models import Membership, MembershipPlan
from notifications.services import notify_user
from payments.models import Payment
from website.models import Enquiry


def _month_buckets(months=6):
    today = timezone.localdate()
    buckets = []
    year, month = today.year, today.month
    for _ in range(months):
        buckets.append((year, month))
        month -= 1
        if month == 0:
            month, year = 12, year - 1
    return list(reversed(buckets))


def _max_value(items, key='value'):
    values = [item[key] for item in items]
    return max(values) if values and max(values) > 0 else 1


@staff_member_required
def dashboard(request):
    today = timezone.localdate()

    total_members = MemberProfile.objects.count()
    active_memberships = Membership.objects.filter(status=Membership.STATUS_ACTIVE, end_date__gte=today).count()
    expired_memberships = Membership.objects.filter(
        Q(status=Membership.STATUS_EXPIRED) | Q(status=Membership.STATUS_ACTIVE, end_date__lt=today)
    ).count()
    new_registrations_today = MemberProfile.objects.filter(created_at__date=today).count()
    todays_payments = Payment.objects.filter(status=Payment.STATUS_PAID, created_at__date=today).count()
    total_revenue = Payment.objects.filter(status=Payment.STATUS_PAID).aggregate(total=Sum('amount'))['total'] or Decimal('0')
    renewals = max(Membership.objects.count() - total_members, 0)
    attendance_today = Attendance.objects.filter(check_in_time__date=today).count()
    open_enquiries = Enquiry.objects.filter(is_resolved=False).count()

    growth_chart, revenue_chart = [], []
    for year, month in _month_buckets(6):
        count = Membership.objects.filter(created_at__year=year, created_at__month=month).count()
        revenue = Payment.objects.filter(
            status=Payment.STATUS_PAID, created_at__year=year, created_at__month=month,
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
        label = datetime.date(year, month, 1).strftime('%b')
        growth_chart.append({'label': label, 'value': count})
        revenue_chart.append({'label': label, 'value': round(float(revenue))})

    attendance_chart = []
    for i in range(6, -1, -1):
        day = today - datetime.timedelta(days=i)
        count = Attendance.objects.filter(check_in_time__date=day).count()
        attendance_chart.append({'label': day.strftime('%a'), 'value': count})

    plan_popularity = list(
        MembershipPlan.objects.annotate(member_count=Count('memberships'))
        .values('name', 'member_count').order_by('-member_count')
    )

    context = {
        'total_members': total_members,
        'active_memberships': active_memberships,
        'expired_memberships': expired_memberships,
        'new_registrations_today': new_registrations_today,
        'todays_payments': todays_payments,
        'total_revenue': total_revenue,
        'renewals': renewals,
        'attendance_today': attendance_today,
        'open_enquiries': open_enquiries,
        'growth_chart': growth_chart,
        'growth_max': _max_value(growth_chart),
        'revenue_chart': revenue_chart,
        'revenue_max': _max_value(revenue_chart),
        'attendance_chart': attendance_chart,
        'attendance_max': _max_value(attendance_chart),
        'plan_popularity': plan_popularity,
        'plan_popularity_max': _max_value(plan_popularity, key='member_count'),
        'recent_enquiries': Enquiry.objects.filter(is_resolved=False)[:5],
        'recent_registrations': MemberProfile.objects.select_related('user').order_by('-created_at')[:5],
    }
    return render(request, 'management/dashboard.html', context)


@staff_member_required
def member_list(request):
    query = request.GET.get('q', '').strip()
    status = request.GET.get('status', '')
    plan_id = request.GET.get('plan', '')

    members = MemberProfile.objects.select_related('user').prefetch_related('memberships').order_by('-created_at')

    if query:
        members = members.filter(
            Q(member_id__icontains=query)
            | Q(user__first_name__icontains=query)
            | Q(user__last_name__icontains=query)
            | Q(user__email__icontains=query)
            | Q(user__phone_number__icontains=query)
        )
    if status:
        members = members.filter(memberships__status=status).distinct()
    if plan_id:
        members = members.filter(memberships__plan_id=plan_id).distinct()

    paginator = Paginator(members, 20)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'management/members.html', {
        'page_obj': page_obj,
        'query': query,
        'status': status,
        'plan_id': plan_id,
        'plans': MembershipPlan.objects.all(),
        'status_choices': Membership.STATUS_CHOICES,
    })


@staff_member_required
def member_detail(request, member_id):
    profile = get_object_or_404(MemberProfile.objects.select_related('user'), member_id=member_id)
    memberships = profile.memberships.select_related('plan').order_by('-created_at')
    payments = Payment.objects.filter(membership__member=profile).order_by('-created_at')
    attendance_records = profile.attendance_records.order_by('-check_in_time')[:20]

    return render(request, 'management/member_detail.html', {
        'profile': profile,
        'memberships': memberships,
        'payments': payments,
        'attendance_records': attendance_records,
    })


@staff_member_required
def extend_membership(request, membership_id):
    membership = get_object_or_404(Membership, id=membership_id)
    if request.method == 'POST':
        try:
            days = int(request.POST.get('days', 0))
        except ValueError:
            days = 0
        if days > 0:
            base_date = membership.end_date if membership.end_date and membership.end_date >= timezone.localdate() else timezone.localdate()
            membership.end_date = base_date + datetime.timedelta(days=days)
            if not membership.start_date:
                membership.start_date = timezone.localdate()
            membership.status = Membership.STATUS_ACTIVE
            membership.save()
            notify_user(
                membership.member.user, event_type='membership_activated',
                title='Membership extended',
                message=f"Your membership was extended by {days} days. New expiry: {membership.end_date}.",
            )
            messages.success(request, f"Membership extended by {days} days.")
        else:
            messages.error(request, "Enter a valid number of days.")
    return redirect('management:member_detail', member_id=membership.member.member_id)


@staff_member_required
def cancel_membership(request, membership_id):
    membership = get_object_or_404(Membership, id=membership_id)
    if request.method == 'POST':
        membership.status = Membership.STATUS_CANCELLED
        membership.save(update_fields=['status', 'updated_at'])
        messages.success(request, "Membership cancelled.")
    return redirect('management:member_detail', member_id=membership.member.member_id)


@staff_member_required
def toggle_member_active(request, member_id):
    profile = get_object_or_404(MemberProfile, member_id=member_id)
    if request.method == 'POST':
        profile.is_active = not profile.is_active
        profile.user.is_active = profile.is_active
        profile.user.save(update_fields=['is_active'])
        profile.save(update_fields=['is_active', 'updated_at'])
        messages.success(request, f"Member {'activated' if profile.is_active else 'deactivated'}.")
    return redirect('management:member_detail', member_id=profile.member_id)


@staff_member_required
def attendance_list(request):
    date_str = request.GET.get('date')
    try:
        selected_date = datetime.date.fromisoformat(date_str) if date_str else timezone.localdate()
    except ValueError:
        selected_date = timezone.localdate()

    records = Attendance.objects.filter(check_in_time__date=selected_date).select_related('member').order_by('-check_in_time')
    return render(request, 'management/attendance.html', {
        'records': records,
        'selected_date': selected_date,
        'today': timezone.localdate(),
    })


@staff_member_required
def record_manual_attendance(request):
    if request.method == 'POST':
        member_id = request.POST.get('member_id', '').strip()
        try:
            profile = MemberProfile.objects.get(member_id__iexact=member_id)
        except MemberProfile.DoesNotExist:
            messages.error(request, f"No member found with ID {member_id}.")
            return redirect('management:attendance')

        recent_cutoff = timezone.now() - datetime.timedelta(hours=4)
        if Attendance.objects.filter(member=profile, check_in_time__gte=recent_cutoff).exists():
            messages.warning(request, f"{profile.full_name} already checked in recently.")
        else:
            Attendance.objects.create(member=profile, method=Attendance.METHOD_MANUAL, recorded_by=request.user)
            messages.success(request, f"Attendance recorded for {profile.full_name}.")
    return redirect('management:attendance')


@staff_member_required
def enquiry_list(request):
    show_resolved = request.GET.get('resolved') == '1'
    enquiries = Enquiry.objects.all()
    if not show_resolved:
        enquiries = enquiries.filter(is_resolved=False)
    return render(request, 'management/enquiries.html', {'enquiries': enquiries, 'show_resolved': show_resolved})


@staff_member_required
def resolve_enquiry(request, enquiry_id):
    enquiry = get_object_or_404(Enquiry, id=enquiry_id)
    if request.method == 'POST':
        enquiry.is_resolved = True
        enquiry.save(update_fields=['is_resolved'])
        messages.success(request, "Enquiry marked resolved.")
    return redirect('management:enquiries')
