# rekomendasi_jurusan/forms.py
from django import forms
from .models import Kriteria

class InputNilaiForm(forms.Form):
    nama_mahasiswa = forms.CharField(label='Nama Mahasiswa', max_length=150, required=False)
    nim = forms.CharField(label='NIM', max_length=20, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        daftar_kriteria = Kriteria.objects.all().order_by('id')

        for kriteria in daftar_kriteria:
            self.fields[f'nilai_{kriteria.id}'] = forms.FloatField(
                label=f'Nilai {kriteria.nama_kriteria}',
                min_value=0,
                max_value=100,
                required=True,
                widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
            )