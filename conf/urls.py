from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from conf import settings
from conf.swagger import schema_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('repository/', include('apps.repos.urls')),
    path('api/v1/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='api_docs'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
