from django.contrib import admin
from django.urls import include, path

################## Untuk Media ##################
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

from main import views as v
from dashboard import views as vd

urlpatterns = [
    # Default Django
    path('admin/', admin.site.urls),

    # Main Frontend
    path('', v.home, name='home'),
    path('teamfrl/', v.teamfrl, name='teamfrl'),

    # path('dashboard/', include('dashboard.urls')),
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),

    path('spk/',include('rekomendasi_jurusan.urls', namespace='rekomendasi_jurusan')),

]

################## Untuk Media ##################
urlpatterns += staticfiles_urlpatterns()
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
