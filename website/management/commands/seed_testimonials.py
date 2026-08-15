from django.core.management.base import BaseCommand

from website.models import Testimonial

TESTIMONIALS = [
    ("Rohit Kumar", "Joining RUDRA FITNESS was the best decision for my health. The trainers actually pay attention and the equipment is always well maintained.", 5),
    ("Anjali Verma", "I was nervous about joining a gym for the first time, but the environment here is welcoming and safe. Highly recommend to anyone starting out.", 5),
]


class Command(BaseCommand):
    help = "Seeds a couple of starter member testimonials."

    def handle(self, *args, **options):
        created_count = 0
        for order, (name, quote, rating) in enumerate(TESTIMONIALS):
            _, created = Testimonial.objects.get_or_create(
                member_name=name,
                defaults={"quote": quote, "rating": rating, "display_order": order},
            )
            if created:
                created_count += 1
        self.stdout.write(self.style.SUCCESS(f"Seeded testimonials: {created_count} new entr(y/ies) created."))
