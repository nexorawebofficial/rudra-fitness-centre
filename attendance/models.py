from django.conf import settings
from django.db import models
from django.utils import timezone


class Attendance(models.Model):
    METHOD_QR = 'qr'
    METHOD_MANUAL = 'manual'
    METHOD_CHOICES = [
        (METHOD_QR, 'QR Check-in'),
        (METHOD_MANUAL, 'Manual (Admin)'),
    ]

    member = models.ForeignKey(
        'members.MemberProfile', on_delete=models.CASCADE, related_name='attendance_records',
    )
    check_in_time = models.DateTimeField(default=timezone.now)
    method = models.CharField(max_length=10, choices=METHOD_CHOICES, default=METHOD_QR)
    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='attendance_recorded', help_text="Admin/staff who recorded a manual entry",
    )

    class Meta:
        ordering = ['-check_in_time']
        indexes = [models.Index(fields=['member', 'check_in_time'])]

    def __str__(self):
        return f"{self.member} @ {self.check_in_time:%Y-%m-%d %H:%M}"
