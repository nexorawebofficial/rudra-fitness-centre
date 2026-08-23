from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from website.sitemaps import StaticViewSitemap
from website.views import service_worker, assetlinks

sitemaps = {'static': StaticViewSitemap}

admin.site.site_header = 'RUDRA FITNESS Administration'
admin.site.site_title = 'RUDRA FITNESS Admin'
admin.site.index_title = 'Content Management'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sw.js', service_worker, name='service-worker'),
    path('.well-known/assetlinks.json', assetlinks, name='assetlinks'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'), name='robots'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path('accounts/', include('users.urls')),
    path('dashboard/', include('members.urls')),
    path('manage/', include('management_app.urls')),
    path('', include('attendance.urls')),
    path('', include('website.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
