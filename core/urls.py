from django.contrib.sitemaps.views import sitemap
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import path
from django.views.generic import RedirectView
from django.views.generic.base import TemplateView

from goods.sitemaps import GoodSitemap, StaticViewSitemap


sitemaps = {
    'goods': GoodSitemap,
    'static': StaticViewSitemap,
}

urlpatterns = [
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    path('favicon.ico', RedirectView.as_view(
        url=staticfiles_storage.url('img/fav/favicon.ico'))),
    path('robots.txt', TemplateView.as_view(
        template_name="robots.txt", content_type="text/plain"),
    ),
]
