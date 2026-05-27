from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('catalog/', include('apps.catalog.urls')),
    path('reviews/', include('apps.reviews.urls')),
    path('promo/', include('apps.promo.urls')),
    path('analytics/', include('apps.analytics.urls')),
    path('api/', include('apps.api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'КрышаРиэлт — Админка'
admin.site.site_title = 'КрышаРиэлт'
