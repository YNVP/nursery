from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import debug_toolbar
from . import views


urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('user/', include('users.urls')),
    path('nursery/', include('nursery.urls')),
    path('plant/', include('plant.urls')),
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('orders/', include('orders.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

handler404 = 'users.views.handler404'
handler500 = 'users.views.handler500'
