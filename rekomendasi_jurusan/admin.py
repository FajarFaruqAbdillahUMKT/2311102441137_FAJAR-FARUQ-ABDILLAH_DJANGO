# dalam rekomendasi_jurusan/admin.py

from django.contrib import admin
from .models import Kriteria, Alternatif, Mahasiswa, NilaiMataKuliah

admin.site.register(Kriteria)
admin.site.register(Alternatif)
admin.site.register(Mahasiswa)
admin.site.register(NilaiMataKuliah)