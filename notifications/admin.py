from django.contrib import admin

from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_type', 'recipient', 'is_admin_notification', 'is_read', 'created_at')
    list_filter = ('event_type', 'is_admin_notification', 'is_read')
    readonly_fields = ('created_at',)
