from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from goods.models import Good


class GoodSitemap(Sitemap):
    changefreq = 'weekly'
    protocol = 'https'
    priority = 0.9

    def items(self):
        return Good.objects.filter(active=True)

    def lastmod(self, obj):
        return obj.created_at


class StaticViewSitemap(Sitemap):
    changefreq = 'weekly'
    protocol = 'https'
    priority = 0.5

    def items(self):
        return ['goods:index']

    def location(self, item):
        return reverse(item)
