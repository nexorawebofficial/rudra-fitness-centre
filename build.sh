#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email='admin@rudrafitness.com').exists():
    User.objects.create_superuser('admin@rudrafitness.com', 'GymAdmin@123')
"

python manage.py shell -c "
from trainers.models import Trainer
from memberships.models import MembershipPlan

if Trainer.objects.filter(name='Sunny').exists():
    Trainer.objects.filter(name='Sunny').update(specialty='Fitness Trainer', phone='8957808077', experience_years=2)
else:
    Trainer.objects.create(name='Sunny', specialty='Fitness Trainer', phone='8957808077', experience_years=2)

if not MembershipPlan.objects.filter(name='1 Month Plan').exists():
    MembershipPlan.objects.create(name='1 Month Plan', price=500, duration_days=30, benefits='Full gym access\nLocker facility\nFree fitness assessment', is_popular=False, display_order=1)

if not MembershipPlan.objects.filter(name='3 Month Plan').exists():
    MembershipPlan.objects.create(name='3 Month Plan', price=1200, duration_days=90, benefits='Full gym access\nLocker facility\nFree fitness assessment\nBest value - save vs monthly', is_popular=True, display_order=2)
"

python manage.py seed_diet_plans
python manage.py seed_faqs
python manage.py seed_testimonials
