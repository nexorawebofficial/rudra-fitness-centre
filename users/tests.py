from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import TestCase, override_settings
from django.urls import reverse

from members.models import MemberProfile
from memberships.models import Membership, MembershipPlan
from notifications.models import Notification

User = get_user_model()


class RegistrationTests(TestCase):
    def setUp(self):
        self.plan = MembershipPlan.objects.create(
            name='1 Month Plan', price=500, duration_days=30, benefits='Full gym access',
        )
        self.valid_data = {
            'full_name': 'Test Member',
            'email': 'newmember@example.com',
            'phone_number': '9876543210',
            'date_of_birth': '1995-06-15',
            'gender': MemberProfile.GENDER_MALE,
            'emergency_contact_name': 'Emergency Person',
            'emergency_contact_phone': '9876500000',
            'membership_plan': self.plan.id,
            'preferred_training_time': 'morning',
            'fitness_goal': 'General fitness',
            'password1': 'SuperSecure123!',
            'password2': 'SuperSecure123!',
        }

    def test_successful_registration_creates_member_and_pending_membership(self):
        response = self.client.post(reverse('register'), self.valid_data)
        self.assertRedirects(response, reverse('member_dashboard'))

        user = User.objects.get(email='newmember@example.com')
        self.assertTrue(user.check_password('SuperSecure123!'))
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'Member')

        profile = user.member_profile
        self.assertTrue(profile.member_id.startswith('RF-'))
        self.assertEqual(profile.emergency_contact_name, 'Emergency Person')

        membership = profile.memberships.get()
        self.assertEqual(membership.plan, self.plan)
        self.assertEqual(membership.status, Membership.STATUS_PENDING)
        self.assertIsNone(membership.start_date)

        self.assertTrue(Notification.objects.filter(is_admin_notification=True, event_type='registration').exists())
        self.assertTrue(Notification.objects.filter(recipient=user, event_type='registration').exists())

    def test_registration_logs_the_user_in(self):
        self.client.post(reverse('register'), self.valid_data)
        response = self.client.get(reverse('member_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_duplicate_email_is_rejected(self):
        User.objects.create_user(email='newmember@example.com', password='whatever123')
        response = self.client.post(reverse('register'), self.valid_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['form'], 'email', 'An account with this email already exists. Try logging in instead.')
        self.assertEqual(MemberProfile.objects.count(), 0)

    def test_password_mismatch_is_rejected(self):
        data = {**self.valid_data, 'password2': 'DifferentPassword123!'}
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['form'], 'password2', 'Passwords do not match.')
        self.assertFalse(User.objects.filter(email='newmember@example.com').exists())

    def test_weak_password_is_rejected(self):
        data = {**self.valid_data, 'password1': '12345678', 'password2': '12345678'}
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(email='newmember@example.com').exists())

    def test_underage_date_of_birth_is_rejected(self):
        data = {**self.valid_data, 'date_of_birth': '2020-01-01'}
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(email='newmember@example.com').exists())

    def test_invalid_phone_number_is_rejected(self):
        data = {**self.valid_data, 'phone_number': '123'}
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(email='newmember@example.com').exists())


class LoginTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='member@example.com', password='SuperSecure123!')

    def test_login_with_correct_credentials_succeeds(self):
        response = self.client.post(reverse('login'), {'username': 'member@example.com', 'password': 'SuperSecure123!'})
        self.assertRedirects(response, reverse('member_dashboard'))

    def test_login_with_wrong_password_fails(self):
        response = self.client.post(reverse('login'), {'username': 'member@example.com', 'password': 'wrong'})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_logout_ends_session(self):
        self.client.login(email='member@example.com', password='SuperSecure123!')
        self.client.post(reverse('logout'))
        response = self.client.get(reverse('member_dashboard'))
        self.assertEqual(response.status_code, 302)


class RateLimitTests(TestCase):
    def setUp(self):
        cache.clear()

    @override_settings(TESTING=False)
    def test_repeated_login_posts_from_same_ip_get_rate_limited(self):
        for _ in range(10):
            response = self.client.post(reverse('login'), {'username': 'nobody@example.com', 'password': 'wrong'})
            self.assertNotEqual(response.status_code, 429)
        response = self.client.post(reverse('login'), {'username': 'nobody@example.com', 'password': 'wrong'})
        self.assertEqual(response.status_code, 429)
