from django.db import models


class Trainer(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, blank=True)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='trainers/', blank=True, null=True)
    experience_years = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class MembershipPlan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration_days = models.PositiveIntegerField(help_text="Plan duration in days")
    features = models.TextField(help_text="One feature per line")
    is_popular = models.BooleanField(default=False)

    def feature_list(self):
        return [f.strip() for f in self.features.splitlines() if f.strip()]

    def __str__(self):
        return self.name


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.created_at:%Y-%m-%d}"
