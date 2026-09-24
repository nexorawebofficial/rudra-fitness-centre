import json

from .models import WebsiteSettings


def site_settings(request):
    """Makes editable website settings available in every template as `site_settings`."""
    settings_obj = WebsiteSettings.load()
    return {
        'site_settings': settings_obj,
        'local_business_schema_json': _build_local_business_schema(request, settings_obj),
    }


def _build_local_business_schema(request, settings_obj):
    """JSON-LD for local-business SEO, built only from real, admin-entered data.

    Opening hours are intentionally left out: schema.org requires a strict
    machine-readable format (e.g. "Mo-Sa 06:00-22:00") and the admin-editable
    `opening_hours` field is freeform text, so converting it automatically
    risks publishing incorrect structured data.
    """
    if not (settings_obj.address or settings_obj.phone_primary):
        return None

    site_url = f"{request.scheme}://{request.get_host()}"
    data = {
        '@context': 'https://schema.org',
        '@type': 'HealthClub',
        'name': settings_obj.site_title or 'RUDRA FITNESS',
        'description': settings_obj.tagline,
        'url': site_url,
        'priceRange': '$$',
    }
    if settings_obj.hero_image:
        data['image'] = f"{site_url}{settings_obj.hero_image.url}"
    if settings_obj.address:
        data['address'] = {'@type': 'PostalAddress', 'streetAddress': settings_obj.address}
    if settings_obj.phone_primary:
        data['telephone'] = settings_obj.phone_primary
    if settings_obj.email:
        data['email'] = settings_obj.email

    # Guard against a stray "</script>" in admin-entered text breaking out of the tag.
    return json.dumps(data).replace('</', '<\\/')
