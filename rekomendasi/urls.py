from django.urls import path
from . import views

urlpatterns = [

    path('', views.list_mahasiswa, name='list_mahasiswa'),
    path('create/', views.create_mahasiswa, name='create_mahasiswa'),
    path('update/<int:id>/', views.update_mahasiswa, name='update_mahasiswa'),
    path('delete/<int:id>/', views.delete_mahasiswa, name='delete_mahasiswa'),
]