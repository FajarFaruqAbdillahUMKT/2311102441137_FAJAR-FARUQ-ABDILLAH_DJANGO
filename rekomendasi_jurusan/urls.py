from django.urls import path
from . import views

app_name = 'rekomendasi_jurusan'  # Namespace untuk aplikasi ini

urlpatterns = [
    path('input-nilai/', views.input_nilai_dan_rekomendasi, name='input_nilai_spk'),
    # Anda mungkin ingin URL terpisah untuk hasil, atau menampilkannya di halaman yang sama
    # Jika ingin URL terpisah untuk hasil, view perlu dipecah.
]
