# flowers/sitemaps.py
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Flower  # или твоя модель товаров

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'weekly'

    def items(self):
        return ['home', 'catalog', 'about', 'contacts', 'personals']

    def location(self, item):
        return reverse(item)

class FlowerSitemap(Sitemap):
    priority = 0.7
    changefreq = 'daily'

    def items(self):
        return Flower.objects.all()

    def location(self, obj):
        return obj.get_absolute_url()
