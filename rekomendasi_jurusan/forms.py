# dalam rekomendasi_jurusan/forms.py

from django import forms
from .models import Kriteria

class InputNilaiForm(forms.Form):
    # Field opsional untuk nama dan NIM
    nama_mahasiswa = forms.CharField(label='Nama Mahasiswa', max_length=150, required=False)
    nim = forms.CharField(label='NIM', max_length=20, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ambil semua kriteria dari database untuk membuat field input nilai secara dinamis
        daftar_kriteria = Kriteria.objects.all().order_by('id') # Urutkan agar konsisten tampilannya

        for kriteria in daftar_kriteria:
            self.fields[f'nilai_{kriteria.id}'] = forms.FloatField(
                label=f'Nilai {kriteria.nama_kriteria}',
                min_value=0,
                max_value=100, # Asumsi nilai 0-100
                required=True,
                widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}) # Atribut untuk styling
            )

    def clean(self):
        cleaned_data = super().clean()
        # Anda bisa menambahkan validasi tambahan di sini jika diperlukan
        # Misalnya, memastikan semua field nilai kriteria diisi dengan benar
        return cleaned_data