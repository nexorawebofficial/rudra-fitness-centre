from django.db import migrations


def seed_settings(apps, schema_editor):
    WebsiteSettings = apps.get_model('website', 'WebsiteSettings')
    WebsiteSettings.objects.update_or_create(
        pk=1,
        defaults={
            'site_title': 'RUDRA FITNESS',
            'tagline': 'Train Strong. Live Strong.',
            'home_intro_heading': 'Why choose RUDRA FITNESS?',
            'home_intro_text': (
                'Male and female training, professional trainers, modern equipment, '
                'personalized plans, flexible memberships, diet guidance and a clean, safe environment.'
            ),
            'members_count': 150,
            'trainers_count': 3,
            'years_experience': 5,
            'programs_count': 12,
            'phone_primary': '+91 9118940464',
            'phone_secondary': '+91 9170169747',
            'email': 'info@rudrafitness.com',
            'address': 'Sakaldhia-Mugalsarai Highway, Tarajivanpur',
            'opening_hours': 'Mon - Sat: 6:00 AM - 10:00 PM\nSun: 7:00 AM - 1:00 PM',
        },
    )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_announcement_enquiry_faq_galleryimage_testimonial_and_more'),
    ]

    operations = [
        migrations.RunPython(seed_settings, noop),
    ]
