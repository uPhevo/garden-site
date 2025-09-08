from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap, FlowerSitemap 
from django.http import HttpResponse

sitemaps = {
    'static': StaticViewSitemap(),
    'flowers': FlowerSitemap(),
}

def robots_txt(request):
    content = """User-agent: *
Disallow:

Sitemap: http://xn--80aamkkdxhxg7d7b.xn--p1ai/sitemap.xml
"""
    return HttpResponse(content, content_type="text/plain")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path("robots.txt", robots_txt),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
