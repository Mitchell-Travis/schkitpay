from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from accounts import views as account_view
from accounts import utils as utils_view
from pwa import views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('friends/' , include('friends.urls', namespace='friends')),
    path('wellet/', include('wellet.urls')), 
    path('home/', include('core.urls')),
    path('home/', include('pwa.urls')),
    path('pwa/manifest.json', views.manifest),
    path('pwa/serviceworker.js', views.service_worker),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

