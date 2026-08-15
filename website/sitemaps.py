from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    changefreq = 'weekly'

    def items(self):
        return [
            'home', 'about', 'trainers', 'equipment', 'diet_nutrition',
            'pricing', 'gallery', 'testimonials', 'faq', 'contact',
            'privacy_policy', 'terms_and_conditions',
        ]

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return 1.0 if item in ('home', 'pricing') else 0.7
