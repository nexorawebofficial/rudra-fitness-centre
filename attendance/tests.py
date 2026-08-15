import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from members.models import MemberProfile

from .models import Attendance
from .tokens import generate_checkin_token, resolve_checkin_token

User = get_user_model()


class CheckinTokenTests(TestCase):
    def test_valid_token_resolves_to_member_id(self):
        token = generate_checkin_token('RF-2026-1234')
        self.assertEqual(resolve_checkin_token(token), 'RF-2026-1234')

    def test_tampered_token_is_rejected(self):
        token = generate_checkin_token('RF-2026-1234')
        self.assertIsNone(resolve_checkin_token(token + 'x'))

    def test_token_for_different_member_does_not_cross_resolve(self):
        token = generate_checkin_token('RF-2026-1234')
        self.assertNotEqual(resolve_checkin_token(token), 'RF-2026-9999')


class CheckinScanViewTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(email='member@example.com', password='SuperSecure123!')
        self.profile = MemberProfile.objects.create(
            user=user, gender=MemberProfile.GENDER_MALE,
            emergency_contact_name='Emergency', emergency_contact_phone='9876500000',
        )

    def test_valid_qr_records_attendance(self):
        token = generate_checkin_token(self.profile.member_id)
        response = self.client.get(reverse('checkin_scan', args=[token]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Attendance.objects.filter(member=self.profile).count(), 1)
        self.assertEqual(Attendance.objects.first().method, Attendance.METHOD_QR)

    def test_duplicate_checkin_within_window_is_blocked(self):
        token = generate_checkin_token(self.profile.member_id)
        self.client.get(reverse('checkin_scan', args=[token]))
        self.client.get(reverse('checkin_scan', args=[token]))
        self.assertEqual(Attendance.objects.filter(member=self.profile).count(), 1)

    def test_checkin_allowed_again_after_window_passes(self):
        Attendance.objects.create(
            member=self.profile, method=Attendance.METHOD_QR,
            check_in_time=timezone.now() - datetime.timedelta(hours=5),
        )
        token = generate_checkin_token(self.profile.member_id)
        self.client.get(reverse('checkin_scan', args=[token]))
        self.assertEqual(Attendance.objects.filter(member=self.profile).count(), 2)

    def test_invalid_token_returns_400_and_records_nothing(self):
        response = self.client.get(reverse('checkin_scan', args=['not-a-real-token']))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Attendance.objects.count(), 0)

    def test_deactivated_member_cannot_check_in(self):
        self.profile.is_active = False
        self.profile.save()
        token = generate_checkin_token(self.profile.member_id)
        self.client.get(reverse('checkin_scan', args=[token]))
        self.assertEqual(Attendance.objects.count(), 0)
