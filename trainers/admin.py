from django.contrib import admin

from .models import Trainer


@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialty', 'experience_years', 'is_active', 'display_order')
    list_filter = ('is_active',)
    list_editable = ('display_order', 'is_active')
    search_fields = ('name', 'specialty')
