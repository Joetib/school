from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/default-auth/', include('django.contrib.auth.urls')),
    path('accounts/allauth/', include('allauth.urls')),
    path('accounts/', include('accounts.urls',  namespace="accounts")),
    path('', include('pages.urls')),
    path('administrator/', include('administrator.urls', namespace="administrator")),
]

urlpatterns = urlpatterns + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns.append(
        path("__debug__/", include(debug_toolbar.urls)),
    )