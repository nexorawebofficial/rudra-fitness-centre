from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from attendance.models import Attendance
from memberships.models import Membership, MembershipPlan

from .models import MemberProfile
from .services import calculate_rudra_score

User = get_user_model()


class MemberDashboardTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='member@example.com', password='SuperSecure123!')
        self.profile = MemberProfile.objects.create(
            user=self.user,
            gender=MemberProfile.GENDER_FEMALE,
            emergency_contact_name='Emergency Person',
            emergency_contact_phone='9876500000',
        )
        self.plan = MembershipPlan.objects.create(name='1 Month Plan', price=500, duration_days=30, benefits='Gym access')

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('member_dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_dashboard_shows_member_id_when_logged_in(self):
        self.client.login(email='member@example.com', password='SuperSecure123!')
        response = self.client.get(reverse('member_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.profile.member_id)

    def test_dashboard_shows_pending_status_before_activation(self):
        Membership.objects.create(member=self.profile, plan=self.plan, status=Membership.STATUS_PENDING)
        self.client.login(email='member@example.com', password='SuperSecure123!')
        response = self.client.get(reverse('member_dashboard'))
        self.assertContains(response, 'PAYMENT PENDING')

    def test_dashboard_shows_active_status_with_days_remaining(self):
        membership = Membership.objects.create(member=self.profile, plan=self.plan)
        membership.activate()
        self.client.login(email='member@example.com', password='SuperSecure123!')
        response = self.client.get(reverse('member_dashboard'))
        self.assertContains(response, 'ACTIVE')
        self.assertContains(response, 'DAYS REMAINING')


class RudraScoreTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(email='member@example.com', password='SuperSecure123!')
        self.profile = MemberProfile.objects.create(
            user=user, gender=MemberProfile.GENDER_MALE,
            emergency_contact_name='Emergency', emergency_contact_phone='9876500000',
        )
        self.plan = MembershipPlan.objects.create(name='1 Month Plan', price=500, duration_days=30, benefits='Gym access')

    def test_zero_score_with_no_membership_or_attendance(self):
        self.assertEqual(calculate_rudra_score(self.profile), 0)

    def test_active_membership_alone_gives_30_points(self):
        membership = Membership.objects.create(member=self.profile, plan=self.plan)
        membership.activate()
        self.assertEqual(calculate_rudra_score(self.profile), 30)

    def test_frequent_attendance_plus_active_membership_gives_full_score(self):
        membership = Membership.objects.create(member=self.profile, plan=self.plan)
        membership.activate()
        for _ in range(12):
            Attendance.objects.create(member=self.profile)
        self.assertEqual(calculate_rudra_score(self.profile), 100)

    def test_score_never_exceeds_100(self):
        membership = Membership.objects.create(member=self.profile, plan=self.plan)
        membership.activate()
        for _ in range(30):
            Attendance.objects.create(member=self.profile)
        self.assertLessEqual(calculate_rudra_score(self.profile), 100)
