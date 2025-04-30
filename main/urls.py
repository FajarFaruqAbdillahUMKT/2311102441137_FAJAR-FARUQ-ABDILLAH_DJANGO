"""
URL configuration for main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include, path

################## Untuk Media ##################
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

# from .views import home
# from .views import contact
# from .views import service
from .views import * #pake import * (bintang) biar ga cape manggil 1 1

urlpatterns = [
    path('admin/', admin.site.urls),


    path('', home1, name='home-1.html'),
    path('home-1.html', home1, name='home-1.html'),
    path('home-2.html', home2, name='home-2.html'),
    path('home-3.html', home3, name='home-2.html'),
    path('home-4.html', home4, name='home-2.html'),
    path('home-5.html', home5, name='home-2.html'),
    path('home-6.html', home6, name='home-2.html'),


    path('contact-frl.html', contactfrl, name='contact-frl'),
    path('contact-stl.html', contactstl, name='contact-stl'),

    path('service-frl.html', servicefrl, name='service-frl'),
    path('service-stl.html', servicestl, name='service-stl'),

    path('portfolio-1-frl.html', portfolio1frl, name='portfolio-1-frl'),
    path('portfolio-1-stl.html', portfolio1stl, name='portfolio-1-stl'),
    path('portfolio-2-frl.html', portfolio2frl, name='portfolio-2-frl'),
    path('portfolio-2-stl.html', portfolio2stl, name='portfolio-2-stl'),
    path('portfolio-3-frl.html', portfolio3frl, name='portfolio-3-frl'),
    path('portfolio-3-stl.html', portfolio3stl, name='portfolio-3-stl'),

    path('team-frl.html', teamfrl, name='team-frl'),
    path('team-stl.html', teamstl, name='team-stl'),

    path('rekomendasi/', include('rekomendasi.urls')),

]

################## Untuk Media ##################
urlpatterns += staticfiles_urlpatterns()
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
