from django.contrib import admin

from .models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('member', 'check_in_time', 'method', 'recorded_by')
    list_filter = ('method',)
    search_fields = ('member__member_id', 'member__user__username')
    date_hierarchy = 'check_in_time'
