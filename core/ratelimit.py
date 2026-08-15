"""A small, dependency-free rate limiter built on Django's cache framework.

Not a replacement for a dedicated WAF/rate-limiting service in front of a
high-traffic production deployment, but enough to blunt basic brute-force
and spam abuse of public POST endpoints (login, registration, contact form).

Note: with the default LocMemCache, counters are per-process. If you deploy
with multiple gunicorn workers, point CACHES at a shared backend (e.g. Redis)
for the limit to apply across all of them.
"""
import functools

from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse


def rate_limit(key_prefix, max_attempts=10, window_seconds=300):
    def decorator(view_func):
        @functools.wraps(view_func)
        def wrapped(request, *args, **kwargs):
            if request.method == 'POST' and not settings.TESTING:
                ip = request.META.get('REMOTE_ADDR', 'unknown')
                cache_key = f'ratelimit:{key_prefix}:{ip}'
                attempts = cache.get(cache_key, 0)
                if attempts >= max_attempts:
                    return HttpResponse(
                        "Too many attempts. Please wait a few minutes and try again.",
                        status=429,
                    )
                cache.set(cache_key, attempts + 1, window_seconds)
            return view_func(request, *args, **kwargs)
        return wrapped
    return decorator
