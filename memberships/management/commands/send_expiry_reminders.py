import datetime

from django.core.management.base import BaseCommand
from django.utils import timezone

from memberships.models import Membership
from notifications.models import Notification
from notifications.services import notify_user


class Command(BaseCommand):
    help = (
        "Finds memberships expiring in 7/3/1 days and memberships that have just "
        "expired, and creates in-app notifications for the affected members. "
        "Intended to be run once a day via a scheduled task (cron / Render cron job)."
    )

    def handle(self, *args, **options):
        today = timezone.localdate()
        reminders_sent = 0
        expired_count = 0

        for days_out in (7, 3, 1):
            target_date = today + datetime.timedelta(days=days_out)
            memberships = Membership.objects.filter(
                status=Membership.STATUS_ACTIVE, end_date=target_date,
            ).select_related('member__user', 'plan')

            for membership in memberships:
                already_sent = Notification.objects.filter(
                    recipient=membership.member.user,
                    event_type=Notification.EVENT_MEMBERSHIP_EXPIRING,
                    created_at__date=today,
                    message__contains=membership.plan.name,
                ).exists()
                if already_sent:
                    continue
                notify_user(
                    membership.member.user,
                    event_type=Notification.EVENT_MEMBERSHIP_EXPIRING,
                    title=f"Membership expiring in {days_out} day{'s' if days_out != 1 else ''}",
                    message=(
                        f"Your {membership.plan.name} membership expires on {membership.end_date}. "
                        "Renew soon to avoid interruption."
                    ),
                )
                reminders_sent += 1

        expiring_memberships = Membership.objects.filter(
            status=Membership.STATUS_ACTIVE, end_date__lt=today,
        ).select_related('member__user', 'plan')

        for membership in expiring_memberships:
            membership.status = Membership.STATUS_EXPIRED
            membership.save(update_fields=['status', 'updated_at'])
            notify_user(
                membership.member.user,
                event_type=Notification.EVENT_MEMBERSHIP_EXPIRED,
                title="Membership expired",
                message=f"Your {membership.plan.name} membership expired on {membership.end_date}. Renew to regain access.",
            )
            expired_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"Sent {reminders_sent} expiry reminder(s), marked {expired_count} membership(s) as expired.",
        ))
