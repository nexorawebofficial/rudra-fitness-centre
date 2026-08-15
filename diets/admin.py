from django.contrib import admin

from .models import DietCategory, DietPlan


@admin.register(DietCategory)
class DietCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'display_order')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(DietPlan)
class DietPlanAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_published', 'updated_at')
    list_filter = ('category', 'is_published')
    search_fields = ('title',)
