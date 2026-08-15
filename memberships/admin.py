from django.contrib import admin

from .models import Membership, MembershipPlan


@admin.register(MembershipPlan)
class MembershipPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration_days', 'is_popular', 'is_active', 'display_order')
    list_editable = ('is_popular', 'is_active', 'display_order')


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('member', 'plan', 'status', 'start_date', 'end_date')
    list_filter = ('status', 'plan')
    search_fields = ('member__member_id', 'member__user__username', 'member__user__email')
    autocomplete_fields = ('member',)
