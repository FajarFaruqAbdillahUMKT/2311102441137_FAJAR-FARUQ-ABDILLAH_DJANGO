# rekomendasi_jurusan/models.py

from django.db import models

class Kriteria(models.Model):
    nama_kriteria = models.CharField(max_length=100, unique=True, help_text="Nama mata kuliah")
    bobot_jrs = models.FloatField(help_text="Bobot kriteria untuk fokus JRS (misal: 0.03, 0.08)")
    bobot_kc = models.FloatField(help_text="Bobot kriteria untuk fokus KC (misal: 0.03, 0.08)")

    def __str__(self):
        return self.nama_kriteria

    class Meta:
        verbose_name_plural = "Kriteria"

class Alternatif(models.Model):
    kode_alternatif = models.CharField(max_length=10, unique=True, help_text="Contoh: JRS atau KC")
    nama_alternatif = models.CharField(max_length=100)
    deskripsi = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nama_alternatif

    class Meta:
        verbose_name_plural = "Alternatif"

class Mahasiswa(models.Model):
    # Field yang sudah ada
    nama_mahasiswa = models.CharField(max_length=150, blank=True, null=True, help_text="Nama (opsional)")
    nim = models.CharField(max_length=20, blank=True, null=True, help_text="NIM (opsional)")

    # == PERUBAHAN DI SINI ==
    # Field tambahan untuk menyimpan rekomendasi final agar mudah diakses
    rekomendasi_final = models.ForeignKey(Alternatif, on_delete=models.SET_NULL, null=True, blank=True)
    skor_final = models.FloatField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True) # Untuk melacak waktu perhitungan

    def __str__(self):
        if self.nama_mahasiswa:
            return f"{self.nama_mahasiswa} ({self.id})"
        return f"Sesi Penilaian ID: {self.id}"

    class Meta:
        verbose_name_plural = "Data Sesi Mahasiswa (SPK)"
        ordering = ['-timestamp'] # Urutkan dari yang terbaru

# Model ini sudah benar, tidak perlu diubah
class NilaiMataKuliah(models.Model):
    mahasiswa = models.ForeignKey(Mahasiswa, on_delete=models.CASCADE, related_name='nilai_matakuliah_spk')
    kriteria = models.ForeignKey(Kriteria, on_delete=models.CASCADE, related_name='penilaian_matakuliah_spk')
    nilai_mentah = models.FloatField(help_text="Nilai asli mahasiswa untuk mata kuliah ini (0-100)")

    def __str__(self):
        return f"Input oleh '{self.mahasiswa}' - {self.kriteria.nama_kriteria}: {self.nilai_mentah}"

    class Meta:
        verbose_name_plural = "Nilai Mata Kuliah (SPK)"
        unique_together = ('mahasiswa', 'kriteria')

# == MODEL BARU UNTUK MENYIMPAN SEMUA HASIL PERHITUNGAN ==
class HasilRekomendasi(models.Model):
    mahasiswa = models.ForeignKey(Mahasiswa, on_delete=models.CASCADE, related_name='hasil_rekomendasi')
    alternatif = models.ForeignKey(Alternatif, on_delete=models.CASCADE)
    skor = models.FloatField()

    def __str__(self):
        return f"Hasil untuk {self.mahasiswa} -> {self.alternatif.nama_alternatif}: {self.skor:.4f}"

    class Meta:
        verbose_name_plural = "Hasil Perhitungan TOPSIS"
        unique_together = ('mahasiswa', 'alternatif')