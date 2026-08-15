from django.contrib import admin

from .models import MemberProfile


@admin.register(MemberProfile)
class MemberProfileAdmin(admin.ModelAdmin):
    list_display = ('member_id', 'full_name', 'gender', 'is_active', 'created_at')
    list_filter = ('gender', 'is_active')
    search_fields = ('member_id', 'user__username', 'user__email', 'user__first_name', 'user__last_name')
    readonly_fields = ('member_id', 'created_at', 'updated_at')
