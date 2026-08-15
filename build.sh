#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@rudrafitness.com', 'GymAdmin@123')
"

python manage.py shell -c "
from website.models import Trainer, MembershipPlan

if Trainer.objects.filter(name='Sunny').exists():
    Trainer.objects.filter(name='Sunny').update(specialization='Fitness Trainer', phone='8957808077', experience_years=2)
else:
    Trainer.objects.create(name='Sunny', specialization='Fitness Trainer', phone='8957808077', experience_years=2)

if not MembershipPlan.objects.filter(name='Joining Fee').exists():
    MembershipPlan.objects.create(name='Joining Fee', price=500, duration_days=0, features='One-time registration fee\nFull gym access setup\nFitness assessment', is_popular=False)

if not MembershipPlan.objects.filter(name='1 Month Plan').exists():
    MembershipPlan.objects.create(name='1 Month Plan', price=500, duration_days=30, features='Full gym access\nLocker facility\nFree fitness assessment', is_popular=False)

if not MembershipPlan.objects.filter(name='3 Month Plan').exists():
    MembershipPlan.objects.create(name='3 Month Plan', price=1200, duration_days=90, features='Full gym access\nLocker facility\nFree fitness assessment\nBest value - save vs monthly', is_popular=True)
"
