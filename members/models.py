import random

from django.conf import settings
from django.db import models
from django.utils import timezone


def generate_member_id():
    year = timezone.now().year
    while True:
        candidate = f"RF-{year}-{random.randint(1000, 9999)}"
        if not MemberProfile.objects.filter(member_id=candidate).exists():
            return candidate


class MemberProfile(models.Model):
    GENDER_MALE = 'M'
    GENDER_FEMALE = 'F'
    GENDER_OTHER = 'O'
    GENDER_CHOICES = [
        (GENDER_MALE, 'Male'),
        (GENDER_FEMALE, 'Female'),
        (GENDER_OTHER, 'Other'),
    ]

    TRAINING_TIME_CHOICES = [
        ('', 'No preference'),
        ('early_morning', 'Early Morning (5 AM - 8 AM)'),
        ('morning', 'Morning (8 AM - 11 AM)'),
        ('afternoon', 'Afternoon (11 AM - 4 PM)'),
        ('evening', 'Evening (4 PM - 7 PM)'),
        ('night', 'Night (7 PM - 10 PM)'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='member_profile',
    )
    member_id = models.CharField(max_length=20, unique=True, editable=False, default=generate_member_id)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_phone = models.CharField(max_length=15)
    preferred_training_time = models.CharField(max_length=20, choices=TRAINING_TIME_CHOICES, blank=True)
    fitness_goal = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=['member_id'])]
        ordering = ['-created_at']

    @property
    def current_membership(self):
        return self.memberships.filter(status='active').order_by('-end_date').first()

    @property
    def full_name(self):
        return self.user.get_full_name() or self.user.username

    def __str__(self):
        return f"{self.member_id} - {self.full_name}"
