# RUDRA FITNESS

A full-stack gym management platform built with Django: public marketing site, member
registration & login, membership plans, an admin dashboard, attendance via QR check-in,
a digital membership card, and an editable content system (CMS) so the gym owner can
change text, images, prices and contact details without touching code.

## Project status

Online payment (Razorpay) is intentionally **not wired up yet** — new memberships are
created with status `pending` until payment is added. Everything else described below
is implemented and covered by automated tests.

## Project structure

```
core/               Django project settings, root URLs
users/               Custom user model (email-based login), registration & auth views
members/             Member profiles, member dashboard, digital membership card, RUDRA Score
memberships/         Membership plans & subscriptions, expiry-reminder scheduled job
payments/            Payment model (Razorpay fields ready; checkout not yet wired up)
attendance/          Attendance records, QR check-in scanning endpoint
diets/                Diet categories & plans (Weight Management, Muscle Building, etc.)
trainers/             Trainer profiles
notifications/        In-app notification model + helper functions
website/              Public site views/CMS (WebsiteSettings, gallery, testimonials, FAQ, enquiries)
management_app/       Custom staff admin dashboard (stats, charts, member/attendance/enquiry management)
templates/             All HTML templates, organized by app
static/                CSS, JS, icons, PWA manifest/service worker
media/                  User-uploaded images (created at runtime, not in git)
```

Each app owns its own `models.py`, `admin.py`, `migrations/`, and (where relevant)
`views.py`/`urls.py`/`tests.py` — a standard modular Django layout.

## Local setup (Windows / Mac / Linux)

1. **Install Python 3.12+** from python.org (or your OS package manager).

2. **Create and activate a virtual environment**
   ```
   python -m venv venv
   venv\Scripts\activate        # Windows
   source venv/bin/activate     # Mac/Linux
   ```

3. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```

4. **Create your `.env` file** — copy `.env.example` to `.env` and fill in real values:
   ```
   copy .env.example .env        # Windows
   cp .env.example .env          # Mac/Linux
   ```
   At minimum, generate a real `SECRET_KEY`:
   ```
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```
   Local development uses SQLite by default (`DATABASE_URL=sqlite:///db.sqlite3`), so
   no separate database server is required to get started.

5. **Run migrations** (creates the database tables)
   ```
   python manage.py migrate
   ```

6. **Create an admin account**
   ```
   python manage.py createsuperuser
   ```
   You'll be prompted for an email and password (the site uses email, not username, to log in).

7. **(Optional) Seed sample data** — a trainer, two membership plans, and a diet
   category/plan, so the site isn't empty:
   ```
   python manage.py shell -c "
   from trainers.models import Trainer
   from memberships.models import MembershipPlan
   from diets.models import DietCategory, DietPlan
   Trainer.objects.get_or_create(name='Sunny', defaults={'specialty': 'Fitness Trainer', 'experience_years': 2})
   MembershipPlan.objects.get_or_create(name='1 Month Plan', defaults={'price': 500, 'duration_days': 30, 'benefits': 'Full gym access\nLocker facility', 'display_order': 1})
   MembershipPlan.objects.get_or_create(name='3 Month Plan', defaults={'price': 1200, 'duration_days': 90, 'benefits': 'Full gym access\nLocker facility\nBest value', 'is_popular': True, 'display_order': 2})
   cat, _ = DietCategory.objects.get_or_create(name='Weight Management', defaults={'description': 'Balanced nutrition to support healthy weight goals.'})
   DietPlan.objects.get_or_create(category=cat, title='Beginner Weight Management Plan', defaults={'breakfast': 'Oats with fruit and a boiled egg', 'lunch': 'Grilled chicken or paneer with brown rice and salad', 'foods_to_include': 'Vegetables, whole grains, lean protein, fruit', 'foods_to_limit': 'Sugary drinks, fried snacks, refined flour'})
   "
   ```

8. **Run the development server**
   ```
   python manage.py runserver
   ```
   Visit `http://127.0.0.1:8000/` for the public site, `/admin/` for Django's built-in
   admin, and `/manage/` for the custom staff dashboard (log in with your superuser
   account at either — they share the same login).

## Adding your logo, hero image, and content

Nothing in the templates is hard-coded — go to `/admin/website/websitesettings/1/change/`
(or the "Website Settings" link in the `/manage/` sidebar) to upload the logo, favicon,
and homepage hero image, and to edit the tagline, stats counters, contact details,
opening hours, social links, and homepage text. Gallery photos, testimonials, FAQs,
trainers, and membership plans/prices each have their own section in `/admin/`.

## Diet plan sample content

```
python manage.py seed_diet_plans
```

Seeds Beginner/Professional x Affordable/Premium diet plans (16 plans total) across
**Beginner Nutrition**, **Performance Nutrition**, **Weight Management**, **Vegetarian
Fitness**, and **Muscle Building** — realistic meals, hydration guidance, and foods
to include/limit for each. Safe to re-run; it only creates plans that don't already
exist. Add more categories/plans any time from `/admin/diets/dietplan/`.

## More sample content

```
python manage.py seed_faqs
```

Seeds a starter set of frequently asked questions (safe to re-run).

## Running tests

```
python manage.py test
```

Runs the full automated test suite (registration validation, login/logout, membership
activation, the admin dashboard's member/attendance/enquiry actions, the QR check-in
flow including duplicate/tamper rejection, and the expiry-reminder scheduled job).

## Membership expiry reminders (scheduled job)

```
python manage.py send_expiry_reminders
```

Finds memberships expiring in 7/3/1 days and creates a notification for each member;
also auto-marks anything past its end date as `expired` and notifies the member. This
needs to run once a day — on Render, add it as a **Cron Job** service pointed at this
command; elsewhere, a system cron entry or Windows Task Scheduler task works too.

## Configuring payment (when you're ready)

The `payments` app and `Membership.status = 'pending'` flow are already in place for
Razorpay. When you have Razorpay API keys, they'll need to go into `.env` as
`PAYMENT_KEY_ID`, `PAYMENT_KEY_SECRET`, and `WEBHOOK_SECRET` — never in frontend code —
and the checkout + server-side verification views will be added on top of the existing
`Payment` model.

## Configuring email / SMS notifications (when you're ready)

Registration, payment, and membership events already create **in-app** notifications
(visible on the member dashboard and in `/admin/notifications/`). To also send real
emails/SMS/WhatsApp, configure Django's `EMAIL_*` settings (or a provider like Twilio)
and call out to them from `notifications/services.py` — the event hooks are already in
place, they just don't reach an outside inbox yet.

## Deploying to production (Render)

This repo already includes `render.yaml` and `build.sh` for Render:

1. Push this repo to GitHub and create a new **Blueprint** on Render pointing at it.
2. Render provisions a free Postgres database and a web service automatically from
   `render.yaml`, generates `SECRET_KEY`, and sets `DEBUG=False`.
3. `build.sh` runs on every deploy: installs dependencies, collects static files, runs
   migrations, and creates/updates the `admin@rudrafitness.com` superuser and seed data.
4. **Change the seeded admin password immediately after first deploy** —
   `build.sh` sets a known default (`GymAdmin@123`) purely so you can log in once.
5. Add a Render **Cron Job** service running `python manage.py send_expiry_reminders`
   on a daily schedule once you want expiry reminders in production.

For any other host: set `DEBUG=False`, `SECRET_KEY`, `ALLOWED_HOSTS`, and
`DATABASE_URL` (Postgres) as environment variables, run `collectstatic` and `migrate`
during your build step, and serve with `gunicorn core.wsgi:application`.

## Security notes

- Passwords are hashed with Argon2.
- Login is rate-limited (10 attempts / 5 min per IP); registration and the contact form
  are rate-limited per hour. See `core/ratelimit.py`.
- CSRF protection is on for all forms; Django's ORM is used everywhere (no raw SQL).
- `/admin/` and `/manage/` both require staff accounts; the member dashboard requires
  login and only ever shows the logged-in user's own data.
- Uploaded images are validated as real images (Pillow) and capped at 5MB.
- HTTPS/HSTS/secure-cookie settings activate automatically when `DEBUG=False` — see
  `core/settings.py`.
