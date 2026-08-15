"""Thin helpers for creating in-app notifications.

These only write Notification rows (surfaced in the admin dashboard and the
member dashboard). No SMS/email/WhatsApp provider is wired up yet -- see
notifications/README in the admin docs for how to plug one in later.
"""
from .models import Notification


def notify_admins(event_type, title, message):
    return Notification.objects.create(
        recipient=None,
        is_admin_notification=True,
        event_type=event_type,
        title=title,
        message=message,
    )


def notify_user(user, event_type, title, message):
    return Notification.objects.create(
        recipient=user,
        is_admin_notification=False,
        event_type=event_type,
        title=title,
        message=message,
    )
