import datetime

from django.utils import timezone


def calculate_rudra_score(profile):
    """A non-medical, gym-consistency indicator (0-100) based on recent
    attendance and current membership status. This is NOT a fitness,
    health, or medical assessment of any kind.
    """
    thirty_days_ago = timezone.now() - datetime.timedelta(days=30)
    recent_visits = profile.attendance_records.filter(check_in_time__gte=thirty_days_ago).count()

    # Target ~12 visits/month (3x/week) for the full attendance component.
    attendance_component = min(recent_visits, 12) / 12 * 70

    membership = profile.current_membership
    membership_component = 30 if membership and not membership.is_expired else 0

    return round(attendance_component + membership_component)
