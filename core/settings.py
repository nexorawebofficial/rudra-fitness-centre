import os
import sys
from pathlib import Path
import environ

# 1. Initialize environment variables
env = environ.Env(
    DEBUG=(bool, False)
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. Read .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

# True when running `manage.py test`. Used to disable rate limiting (see
# core/ratelimit.py) so the shared process-level cache doesn't cause tests
# to fail each other across a long test run.
TESTING = 'test' in sys.argv

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])

# Render.com sets this automatically for the deployed service
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
    CSRF_TRUSTED_ORIGINS = [f'https://{RENDER_EXTERNAL_HOSTNAME}']

# 3. Application definition (Our LEGO boxes)
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',

    # Third party apps

    # Internal Apps
    'users',
    'members',
    'trainers',
    'memberships',
    'payments',
    'attendance',
    'diets',
    'notifications',
    'website',
    'management_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Serves static files in production
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware', # Good guy stops hackers
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # Look here for HTML files
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'website.context_processors.site_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# 4. Database configuration (Uses SQLite for now, easy for you to run)
DATABASES = {
    'default': env.db(),
}

# 5. Password validation (Making sure passwords aren't too simple)
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# 6. Use modern, super-secure password hashing (Argon2)
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]


# 7. Internationalization (Language and Time)
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata' # Set to Indian time
USE_I18N = True
USE_TZ = True


# 8. Static files (CSS, JavaScript, Images we draw)
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles' # For production

# Hashed, cache-busted filenames only matter in production (and require a
# `collectstatic` run first). In local dev/tests, serve static files directly
# from STATICFILES_DIRS so nothing needs collectstatic to work.
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": (
            "whitenoise.storage.CompressedManifestStaticFilesStorage"
            if not DEBUG else
            "django.contrib.staticfiles.storage.StaticFilesStorage"
        ),
    },
}

# Belt-and-suspenders: if a static file is ever missing from the production
# manifest (e.g. a forgotten `collectstatic` run), fall back to serving it
# unhashed instead of a 500 error.
WHITENOISE_MANIFEST_STRICT = False

# 9. Media files (Photos the Boss uploads)
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 10. Tell Django to use our Custom User Model
AUTH_USER_MODEL = 'users.CustomUser'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'member_dashboard'
LOGOUT_REDIRECT_URL = 'home'

# Used for basic rate-limiting (see core/ratelimit.py). LocMemCache is
# per-process; if you scale to multiple gunicorn workers in production,
# point this at a shared cache (e.g. Redis) instead.
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
}

# 11. Security Settings for Production (These turn on when DEBUG=False)
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_SSL_REDIRECT = True # Forces HTTPS
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    X_FRAME_OPTIONS = 'DENY' # Prevents others from putting our site in a box
    SECURE_HSTS_SECONDS = 31536000 # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
