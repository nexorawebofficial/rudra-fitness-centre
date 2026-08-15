from django.core.management.base import BaseCommand

from website.models import FAQ

FAQS = [
    ("Do I need a prior fitness background to join?", "No. RUDRA FITNESS welcomes complete beginners as well as experienced athletes. Our trainers will build a plan around your current fitness level."),
    ("Are the training sessions separate for men and women?", "The gym floor is open to all members. We maintain a clean, respectful, safety-first environment for everyone."),
    ("Can I freeze or pause my membership?", "Yes, speak to the front desk about pausing your membership for medical or travel reasons."),
    ("What should I bring on my first visit?", "Comfortable workout clothes, a water bottle, a small towel, and a valid ID for registration."),
    ("Is personal training available?", "Yes, our trainers offer one-on-one sessions in addition to general gym access. Ask at the front desk for current availability and pricing."),
    ("How do I renew my membership?", "You can renew from your member dashboard once online payment is enabled, or speak to our front desk staff directly."),
]


class Command(BaseCommand):
    help = "Seeds a starter set of frequently asked questions."

    def handle(self, *args, **options):
        created_count = 0
        for order, (question, answer) in enumerate(FAQS):
            _, created = FAQ.objects.get_or_create(
                question=question,
                defaults={"answer": answer, "display_order": order},
            )
            if created:
                created_count += 1
        self.stdout.write(self.style.SUCCESS(f"Seeded FAQs: {created_count} new entr(y/ies) created."))
