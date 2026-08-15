from django.db import models
from django.utils.text import slugify


class DietCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'name']
        verbose_name_plural = 'Diet categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class DietPlan(models.Model):
    category = models.ForeignKey(DietCategory, on_delete=models.CASCADE, related_name='plans')
    title = models.CharField(max_length=150)
    breakfast = models.TextField(blank=True)
    lunch = models.TextField(blank=True)
    snack = models.TextField(blank=True)
    dinner = models.TextField(blank=True)
    hydration_notes = models.TextField(blank=True)
    general_notes = models.TextField(blank=True)
    foods_to_include = models.TextField(blank=True)
    foods_to_limit = models.TextField(blank=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category__display_order', 'title']

    def __str__(self):
        return f"{self.title} ({self.category.name})"
