from django.urls import path
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from . import views as v

app_name = 'dashboard'

urlpatterns = [
    # Dashboard
    path('', v.dashboard, name='dashboard'),

    # Authentication
    path('login/', v.login_view, name='login'),
    path('signup/', v.signup_view, name='signup'),
    path('logout/', v.logout_view, name='logout'),
    path('password_reset/', PasswordResetView.as_view(template_name='dashboard/authentication/password_reset.html'),
         name='password_reset'),
    path('password_reset/done/',
         PasswordResetDoneView.as_view(template_name='dashboard/authentication/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='dashboard/authentication/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/',
         PasswordResetCompleteView.as_view(template_name='dashboard/authentication/password_reset_complete.html'),
         name='password_reset_complete'),

    # Mahasiswa
    path('list/', v.list_mahasiswa, name='list_mahasiswa'),
    path('create/', v.create_mahasiswa, name='create_mahasiswa'),
    path('update/<int:id>/', v.update_mahasiswa, name='update_mahasiswa'),
    path('delete/<int:id>/', v.delete_mahasiswa, name='delete_mahasiswa'), \

    # Nilai
    path('nilai/list/', v.list_nilai, name='list_nilai'),
    path('nilai/input/', v.input_nilai, name='input_nilai'),


]
