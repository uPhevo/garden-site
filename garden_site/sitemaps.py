from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from flowers.models import Flower

class StaticViewSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return ['home', 'catalog', 'about', 'contacts', 'personals']

    def location(self, item):
        return reverse(item)

class FlowerSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.7

    def items(self):
        return Flower.objects.all()

    # теперь location можно оставить по умолчанию, т.к. get_absolute_url есть
    # def location(self, obj):
    #     return obj.get_absolute_url()
