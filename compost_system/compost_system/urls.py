from django.conf.urls.static import static
from django.urls import path, include

from compost_system import settings

urlpatterns = [
                  #    path('admin/', admin.site.urls),
                  path('api/', include('api.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
