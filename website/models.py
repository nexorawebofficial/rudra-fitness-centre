from django.core.exceptions import ValidationError
from django.db import models


def validate_image_size(image):
    max_size_mb = 5
    if image.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f"Image file too large. Maximum size is {max_size_mb}MB.")


class WebsiteSettings(models.Model):
    """Singleton (pk=1) row holding all admin-editable site content."""

    site_title = models.CharField(max_length=100, default='RUDRA FITNESS')
    tagline = models.CharField(max_length=200, default='Train Strong. Live Strong.')

    logo = models.ImageField(upload_to='branding/', blank=True, null=True, validators=[validate_image_size])
    favicon = models.ImageField(upload_to='branding/', blank=True, null=True, validators=[validate_image_size])
    hero_image = models.ImageField(upload_to='branding/', blank=True, null=True, validators=[validate_image_size])

    home_intro_heading = models.CharField(max_length=200, default='Why choose RUDRA FITNESS?')
    home_intro_text = models.TextField(blank=True, default=(
        'Male and female training, professional trainers, modern equipment, '
        'personalized plans, flexible memberships, diet guidance and a clean, safe environment.'
    ))

    members_count = models.PositiveIntegerField(default=0, help_text="Shown in the homepage stats counter")
    trainers_count = models.PositiveIntegerField(default=0)
    years_experience = models.PositiveIntegerField(default=0)
    programs_count = models.PositiveIntegerField(default=0)

    phone_primary = models.CharField(max_length=20, blank=True)
    phone_secondary = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    google_maps_embed_url = models.URLField(blank=True)

    opening_hours = models.TextField(
        blank=True,
        help_text="One line per day, e.g. 'Mon-Sat: 6:00 AM - 10:00 PM'",
    )

    instagram_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    whatsapp_number = models.CharField(max_length=20, blank=True)

    privacy_policy = models.TextField(blank=True)
    terms_and_conditions = models.TextField(blank=True)

    todays_motivation = models.CharField(max_length=300, blank=True)
    workout_of_the_day = models.TextField(blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Website Settings'
        verbose_name_plural = 'Website Settings'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return 'Website Settings'


class Equipment(models.Model):
    CATEGORY_CARDIO = 'cardio'
    CATEGORY_STRENGTH = 'strength'
    CATEGORY_FREE_WEIGHTS = 'free_weights'
    CATEGORY_FUNCTIONAL = 'functional'
    CATEGORY_CHOICES = [
        (CATEGORY_CARDIO, 'Cardio'),
        (CATEGORY_STRENGTH, 'Strength Machines'),
        (CATEGORY_FREE_WEIGHTS, 'Free Weights'),
        (CATEGORY_FUNCTIONAL, 'Functional Training'),
    ]

    name = models.CharField(max_length=120)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default=CATEGORY_STRENGTH)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='equipment/', blank=True, null=True, validators=[validate_image_size])
    is_visible = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'name']
        verbose_name_plural = 'Equipment'

    def __str__(self):
        return self.name


class GalleryImage(models.Model):
    CATEGORY_GYM = 'gym'
    CATEGORY_EQUIPMENT = 'equipment'
    CATEGORY_TRAINERS = 'trainers'
    CATEGORY_TRAINING = 'training'
    CATEGORY_EVENTS = 'events'
    CATEGORY_MEMBERS = 'members'
    CATEGORY_CHOICES = [
        (CATEGORY_GYM, 'Gym'),
        (CATEGORY_EQUIPMENT, 'Equipment'),
        (CATEGORY_TRAINERS, 'Trainers'),
        (CATEGORY_TRAINING, 'Training'),
        (CATEGORY_EVENTS, 'Events'),
        (CATEGORY_MEMBERS, 'Members'),
    ]

    image = models.ImageField(upload_to='gallery/', validators=[validate_image_size])
    caption = models.CharField(max_length=150, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default=CATEGORY_GYM)
    display_order = models.PositiveIntegerField(default=0)
    is_visible = models.BooleanField(default=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['display_order', '-uploaded_at']

    def __str__(self):
        return self.caption or f"Gallery image #{self.pk}"


class Testimonial(models.Model):
    member_name = models.CharField(max_length=100)
    member_photo = models.ImageField(upload_to='testimonials/', blank=True, null=True, validators=[validate_image_size])
    quote = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5, help_text="1 to 5 stars")
    is_published = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['display_order', '-created_at']

    def __str__(self):
        return f"{self.member_name} ({self.rating}★)"


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    display_order = models.PositiveIntegerField(default=0)
    is_visible = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order']
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'

    def __str__(self):
        return self.question


class Announcement(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Enquiry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True)
    message = models.TextField()
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Enquiries'

    def __str__(self):
        return f"{self.name} - {self.created_at:%Y-%m-%d}"
