import datetime

from django.db import models
from django.utils import timezone


class MembershipPlan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration_days = models.PositiveIntegerField(help_text="Plan duration in days")
    benefits = models.TextField(help_text="One benefit per line")
    is_popular = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'price']

    def benefit_list(self):
        return [b.strip() for b in self.benefits.splitlines() if b.strip()]

    def __str__(self):
        return f"{self.name} - ₹{self.price}"


class Membership(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_ACTIVE = 'active'
    STATUS_EXPIRED = 'expired'
    STATUS_CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending Payment'),
        (STATUS_ACTIVE, 'Active'),
        (STATUS_EXPIRED, 'Expired'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]

    member = models.ForeignKey(
        'members.MemberProfile', on_delete=models.CASCADE, related_name='memberships',
    )
    plan = models.ForeignKey(MembershipPlan, on_delete=models.PROTECT, related_name='memberships')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['end_date']),
        ]

    def activate(self, start_date=None):
        self.start_date = start_date or timezone.localdate()
        self.end_date = self.start_date + datetime.timedelta(days=self.plan.duration_days)
        self.status = self.STATUS_ACTIVE
        self.save(update_fields=['start_date', 'end_date', 'status', 'updated_at'])

    @property
    def days_remaining(self):
        if not self.end_date:
            return None
        return (self.end_date - timezone.localdate()).days

    @property
    def is_expired(self):
        return self.end_date is not None and self.end_date < timezone.localdate()

    def __str__(self):
        return f"{self.member} - {self.plan.name} ({self.status})"
