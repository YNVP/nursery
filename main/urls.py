from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import debug_toolbar

urlpatterns = [
    path('user/', include('users.urls')),
    path('nursery/',include('nursery.urls')),
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'users.views.handler404'
handler500 = 'users.views.handler500'
