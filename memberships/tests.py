import datetime

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from members.models import MemberProfile
from notifications.models import Notification

from .models import Membership, MembershipPlan

User = get_user_model()


class MembershipModelTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(email='member@example.com', password='SuperSecure123!')
        self.profile = MemberProfile.objects.create(
            user=user,
            gender=MemberProfile.GENDER_MALE,
            emergency_contact_name='Emergency Person',
            emergency_contact_phone='9876500000',
        )
        self.plan = MembershipPlan.objects.create(name='1 Month Plan', price=500, duration_days=30, benefits='Gym access')

    def test_activate_sets_status_and_end_date(self):
        membership = Membership.objects.create(member=self.profile, plan=self.plan)
        membership.activate()
        self.assertEqual(membership.status, Membership.STATUS_ACTIVE)
        self.assertEqual(membership.start_date, timezone.localdate())
        self.assertEqual(membership.end_date, timezone.localdate() + datetime.timedelta(days=30))

    def test_days_remaining_counts_down(self):
        membership = Membership.objects.create(member=self.profile, plan=self.plan)
        membership.activate(start_date=timezone.localdate() - datetime.timedelta(days=10))
        self.assertEqual(membership.days_remaining, 20)

    def test_is_expired_true_after_end_date(self):
        membership = Membership.objects.create(member=self.profile, plan=self.plan)
        membership.activate(start_date=timezone.localdate() - datetime.timedelta(days=40))
        self.assertTrue(membership.is_expired)

    def test_is_expired_false_for_pending_membership(self):
        membership = Membership.objects.create(member=self.profile, plan=self.plan)
        self.assertFalse(membership.is_expired)
        self.assertIsNone(membership.days_remaining)

    def test_plan_benefit_list_splits_lines(self):
        plan = MembershipPlan.objects.create(
            name='3 Month Plan', price=1200, duration_days=90,
            benefits='Full gym access\nLocker facility\n\nFree assessment',
        )
        self.assertEqual(plan.benefit_list(), ['Full gym access', 'Locker facility', 'Free assessment'])


class ExpiryReminderCommandTests(TestCase):
    def setUp(self):
        self.plan = MembershipPlan.objects.create(name='1 Month Plan', price=500, duration_days=30, benefits='Gym access')

    def _make_membership(self, email, end_date, status=Membership.STATUS_ACTIVE):
        user = User.objects.create_user(email=email, password='SuperSecure123!')
        profile = MemberProfile.objects.create(
            user=user, gender=MemberProfile.GENDER_MALE,
            emergency_contact_name='Emergency', emergency_contact_phone='9876500000',
        )
        return Membership.objects.create(
            member=profile, plan=self.plan, status=status,
            start_date=timezone.localdate() - datetime.timedelta(days=27), end_date=end_date,
        )

    def test_sends_reminder_for_membership_expiring_in_3_days(self):
        membership = self._make_membership('expiring3@example.com', timezone.localdate() + datetime.timedelta(days=3))
        call_command('send_expiry_reminders')
        self.assertTrue(Notification.objects.filter(
            recipient=membership.member.user, event_type=Notification.EVENT_MEMBERSHIP_EXPIRING,
        ).exists())

    def test_does_not_remind_for_membership_expiring_in_5_days(self):
        membership = self._make_membership('expiring5@example.com', timezone.localdate() + datetime.timedelta(days=5))
        call_command('send_expiry_reminders')
        self.assertFalse(Notification.objects.filter(recipient=membership.member.user).exists())

    def test_marks_past_end_date_membership_as_expired_and_notifies(self):
        membership = self._make_membership('justexpired@example.com', timezone.localdate() - datetime.timedelta(days=2))
        call_command('send_expiry_reminders')
        membership.refresh_from_db()
        self.assertEqual(membership.status, Membership.STATUS_EXPIRED)
        self.assertTrue(Notification.objects.filter(
            recipient=membership.member.user, event_type=Notification.EVENT_MEMBERSHIP_EXPIRED,
        ).exists())

    def test_running_twice_does_not_duplicate_reminders(self):
        membership = self._make_membership('expiring1@example.com', timezone.localdate() + datetime.timedelta(days=1))
        call_command('send_expiry_reminders')
        call_command('send_expiry_reminders')
        self.assertEqual(
            Notification.objects.filter(recipient=membership.member.user, event_type=Notification.EVENT_MEMBERSHIP_EXPIRING).count(),
            1,
        )
