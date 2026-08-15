from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.db import transaction
from django.shortcuts import redirect, render

from members.models import MemberProfile
from memberships.models import Membership
from notifications.services import notify_admins, notify_user

from .forms import MemberRegistrationForm

User = get_user_model()


def register(request):
    if request.user.is_authenticated:
        return redirect('member_dashboard')

    if request.method == 'POST':
        form = MemberRegistrationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            name_parts = data['full_name'].strip().split(' ', 1)
            first_name = name_parts[0]
            last_name = name_parts[1] if len(name_parts) > 1 else ''

            with transaction.atomic():
                user = User.objects.create_user(
                    email=data['email'],
                    password=data['password1'],
                    first_name=first_name,
                    last_name=last_name,
                    phone_number=data['phone_number'],
                )
                profile = MemberProfile.objects.create(
                    user=user,
                    date_of_birth=data['date_of_birth'],
                    gender=data['gender'],
                    emergency_contact_name=data['emergency_contact_name'],
                    emergency_contact_phone=data['emergency_contact_phone'],
                    preferred_training_time=data.get('preferred_training_time', ''),
                    fitness_goal=data.get('fitness_goal', ''),
                )
                membership = Membership.objects.create(
                    member=profile,
                    plan=data['membership_plan'],
                    status=Membership.STATUS_PENDING,
                )

            notify_admins(
                event_type='registration',
                title='New member registration',
                message=(
                    f"{profile.full_name} ({profile.member_id}) registered for "
                    f"{membership.plan.name}. Awaiting payment activation."
                ),
            )
            notify_user(
                user,
                event_type='registration',
                title='Welcome to RUDRA FITNESS',
                message=(
                    f"Your Member ID is {profile.member_id}. Complete payment to activate "
                    f"your {membership.plan.name} membership."
                ),
            )

            login(request, user)
            messages.success(
                request,
                f"Welcome to RUDRA FITNESS! Your Member ID is {profile.member_id}. "
                "Online payment is coming soon — our team will contact you to activate your membership.",
            )
            return redirect('member_dashboard')
    else:
        initial = {}
        plan_id = request.GET.get('plan')
        if plan_id:
            initial['membership_plan'] = plan_id
        form = MemberRegistrationForm(initial=initial)

    return render(request, 'users/register.html', {'form': form})
