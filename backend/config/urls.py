from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

admin.site.site_header = 'Administración del portafolio'
admin.site.site_title = 'Portafolio'
admin.site.index_title = 'Contenido, mensajes y estadísticas'

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path('api/', include('apps.core.urls')),
    path('api/', include('apps.contact.urls')),
    path('api/', include('apps.analytics.urls')),
]

# En desarrollo Django sirve los archivos públicos subidos; en producción
# los sirve el servidor web (ver backend/README.md)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
