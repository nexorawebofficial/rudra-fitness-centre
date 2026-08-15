from django.db import models


class Trainer(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='trainers/', blank=True, null=True)
    qualification = models.CharField(max_length=200, blank=True)
    specialty = models.CharField(max_length=150, help_text="e.g. Strength Training, Yoga, Weight Loss")
    experience_years = models.PositiveIntegerField(default=0)
    bio = models.TextField(blank=True)
    training_categories = models.CharField(
        max_length=255, blank=True,
        help_text="Comma-separated, e.g. Weight Training, Yoga, Cardio",
    )
    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'name']

    def category_list(self):
        return [c.strip() for c in self.training_categories.split(',') if c.strip()]

    def __str__(self):
        return self.name
