from django.urls import path

from dashboard import views as v

urlpatterns = [
    # Dashboard
    path('', v.dashboard, name='dashboard'),

    # Authentication
    path('login/', v.login, name='login'),
    path('daftar/', v.daftar, name='daftar'),

    path('', v.list_mahasiswa, name='list_mahasiswa'),
    path('create/', v.create_mahasiswa, name='create_mahasiswa'),
    path('update/<int:id>/', v.update_mahasiswa, name='update_mahasiswa'),
    path('delete/<int:id>/', v.delete_mahasiswa, name='delete_mahasiswa'),

]
