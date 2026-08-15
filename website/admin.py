from django.contrib import admin

from .models import FAQ, Announcement, Enquiry, Equipment, GalleryImage, Testimonial, WebsiteSettings


@admin.register(WebsiteSettings)
class WebsiteSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not WebsiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_visible', 'display_order')
    list_filter = ('category', 'is_visible')
    list_editable = ('display_order', 'is_visible')


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('caption', 'category', 'display_order', 'is_visible', 'uploaded_at')
    list_filter = ('category', 'is_visible')
    list_editable = ('display_order', 'is_visible')


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('member_name', 'rating', 'is_published', 'display_order')
    list_editable = ('is_published', 'display_order')


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'display_order', 'is_visible')
    list_editable = ('display_order', 'is_visible')


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_editable = ('is_active',)


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'is_resolved', 'created_at')
    list_filter = ('is_resolved',)
    list_editable = ('is_resolved',)
    readonly_fields = ('created_at',)
    search_fields = ('name', 'email', 'phone', 'message')
