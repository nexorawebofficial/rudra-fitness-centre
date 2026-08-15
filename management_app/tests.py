from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from members.models import MemberProfile
from memberships.models import Membership, MembershipPlan
from website.models import Enquiry

User = get_user_model()


class DashboardAccessTests(TestCase):
    def setUp(self):
        self.staff = User.objects.create_user(email='staff@example.com', password='StaffPass123!', is_staff=True)
        self.member_user = User.objects.create_user(email='member@example.com', password='MemberPass123!')

    def test_anonymous_user_redirected_to_admin_login(self):
        response = self.client.get(reverse('management:dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/admin/login/', response.url)

    def test_non_staff_member_denied(self):
        self.client.login(email='member@example.com', password='MemberPass123!')
        response = self.client.get(reverse('management:dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_staff_can_view_dashboard(self):
        self.client.login(email='staff@example.com', password='StaffPass123!')
        response = self.client.get(reverse('management:dashboard'))
        self.assertEqual(response.status_code, 200)


class MemberManagementTests(TestCase):
    def setUp(self):
        self.staff = User.objects.create_user(email='staff@example.com', password='StaffPass123!', is_staff=True)
        self.client.login(email='staff@example.com', password='StaffPass123!')

        self.member_user = User.objects.create_user(email='member@example.com', password='MemberPass123!')
        self.profile = MemberProfile.objects.create(
            user=self.member_user, gender=MemberProfile.GENDER_MALE,
            emergency_contact_name='Emergency', emergency_contact_phone='9876500000',
        )
        self.plan = MembershipPlan.objects.create(name='1 Month Plan', price=500, duration_days=30, benefits='Gym access')
        self.membership = Membership.objects.create(member=self.profile, plan=self.plan, status=Membership.STATUS_PENDING)

    def test_member_list_shows_member(self):
        response = self.client.get(reverse('management:members'))
        self.assertContains(response, self.profile.member_id)

    def test_member_search_by_member_id(self):
        response = self.client.get(reverse('management:members'), {'q': self.profile.member_id})
        self.assertContains(response, self.profile.member_id)

    def test_member_search_no_match(self):
        response = self.client.get(reverse('management:members'), {'q': 'NOT-A-REAL-ID'})
        self.assertNotContains(response, self.profile.member_id)

    def test_extend_membership_activates_pending_membership(self):
        response = self.client.post(
            reverse('management:extend_membership', args=[self.membership.id]), {'days': 30},
        )
        self.assertEqual(response.status_code, 302)
        self.membership.refresh_from_db()
        self.assertEqual(self.membership.status, Membership.STATUS_ACTIVE)
        self.assertIsNotNone(self.membership.end_date)

    def test_extend_membership_rejects_invalid_days(self):
        response = self.client.post(
            reverse('management:extend_membership', args=[self.membership.id]), {'days': '0'},
        )
        self.assertEqual(response.status_code, 302)
        self.membership.refresh_from_db()
        self.assertEqual(self.membership.status, Membership.STATUS_PENDING)

    def test_cancel_membership(self):
        response = self.client.post(reverse('management:cancel_membership', args=[self.membership.id]))
        self.assertEqual(response.status_code, 302)
        self.membership.refresh_from_db()
        self.assertEqual(self.membership.status, Membership.STATUS_CANCELLED)

    def test_toggle_member_active_deactivates_user_login(self):
        self.client.post(reverse('management:toggle_member_active', args=[self.profile.member_id]))
        self.profile.refresh_from_db()
        self.member_user.refresh_from_db()
        self.assertFalse(self.profile.is_active)
        self.assertFalse(self.member_user.is_active)


class EnquiryManagementTests(TestCase):
    def setUp(self):
        self.staff = User.objects.create_user(email='staff@example.com', password='StaffPass123!', is_staff=True)
        self.client.login(email='staff@example.com', password='StaffPass123!')
        self.enquiry = Enquiry.objects.create(name='Visitor', email='visitor@example.com', message='Question?')

    def test_open_enquiries_listed_by_default(self):
        response = self.client.get(reverse('management:enquiries'))
        self.assertContains(response, 'Visitor')

    def test_resolve_enquiry(self):
        response = self.client.post(reverse('management:resolve_enquiry', args=[self.enquiry.id]))
        self.assertEqual(response.status_code, 302)
        self.enquiry.refresh_from_db()
        self.assertTrue(self.enquiry.is_resolved)

    def test_resolved_enquiry_hidden_from_default_view(self):
        self.enquiry.is_resolved = True
        self.enquiry.save()
        response = self.client.get(reverse('management:enquiries'))
        self.assertNotContains(response, 'Visitor')
