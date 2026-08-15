from .models import WebsiteSettings


def site_settings(request):
    """Makes editable website settings available in every template as `site_settings`."""
    return {'site_settings': WebsiteSettings.load()}
