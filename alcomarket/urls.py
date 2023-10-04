from django.conf import settings
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls_auth')),
    path('profile/', include('users.urls_profile')),
    path('feedback/', include('feedbacks.urls')),
    path('', include('goods.urls')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)