from django.conf import settings
from django.db import models


class Notification(models.Model):
    EVENT_REGISTRATION = 'registration'
    EVENT_PAYMENT_SUCCESS = 'payment_success'
    EVENT_MEMBERSHIP_ACTIVATED = 'membership_activated'
    EVENT_MEMBERSHIP_EXPIRING = 'membership_expiring'
    EVENT_MEMBERSHIP_EXPIRED = 'membership_expired'
    EVENT_ENQUIRY = 'enquiry'
    EVENT_ANNOUNCEMENT = 'announcement'
    EVENT_CHOICES = [
        (EVENT_REGISTRATION, 'New Registration'),
        (EVENT_PAYMENT_SUCCESS, 'Payment Successful'),
        (EVENT_MEMBERSHIP_ACTIVATED, 'Membership Activated'),
        (EVENT_MEMBERSHIP_EXPIRING, 'Membership Expiring Soon'),
        (EVENT_MEMBERSHIP_EXPIRED, 'Membership Expired'),
        (EVENT_ENQUIRY, 'New Enquiry'),
        (EVENT_ANNOUNCEMENT, 'Admin Announcement'),
    ]

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications',
        null=True, blank=True, help_text="Leave blank for admin-only notifications",
    )
    is_admin_notification = models.BooleanField(default=False)
    event_type = models.CharField(max_length=30, choices=EVENT_CHOICES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'is_read']),
            models.Index(fields=['is_admin_notification', 'is_read']),
        ]

    def __str__(self):
        return self.title
