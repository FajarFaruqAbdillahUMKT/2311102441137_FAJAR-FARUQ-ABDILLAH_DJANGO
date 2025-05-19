# Dalam rekomendasi_jurusan/models.py

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
    # Nama mahasiswa, boleh kosong jika pengguna tidak ingin mengisinya
    nama_mahasiswa = models.CharField(max_length=150, blank=True, null=True, help_text="Nama (opsional)")
    # NIM mahasiswa, boleh kosong dan tidak harus unik secara global
    nim = models.CharField(max_length=20, blank=True, null=True, help_text="NIM (opsional)")

    def __str__(self):
        if self.nama_mahasiswa and self.nim:
            return f"{self.nama_mahasiswa} ({self.nim})"
        elif self.nama_mahasiswa:
            return self.nama_mahasiswa
        elif self.nim:
            return f"NIM: {self.nim}"
        return f"Sesi Penilaian ID: {self.id}" # Jika nama dan NIM tidak diisi

    class Meta:
        verbose_name_plural = "Data Input Mahasiswa (SPK)"


class NilaiMataKuliah(models.Model):
    # Menghubungkan ke Mahasiswa (atau sesi input) dalam aplikasi ini
    mahasiswa = models.ForeignKey(Mahasiswa, on_delete=models.CASCADE, related_name='nilai_matakuliah_spk')
    kriteria = models.ForeignKey(Kriteria, on_delete=models.CASCADE, related_name='penilaian_matakuliah_spk')
    nilai_mentah = models.FloatField(help_text="Nilai asli mahasiswa untuk mata kuliah ini (0-100)")

    def __str__(self):
        return f"Input oleh '{self.mahasiswa}' - {self.kriteria.nama_kriteria}: {self.nilai_mentah}"

    class Meta:
        verbose_name_plural = "Nilai Mata Kuliah (SPK)"
        # unique_together bisa tetap ada untuk memastikan dalam satu sesi input,
        # satu kriteria hanya punya satu nilai.
        unique_together = ('mahasiswa', 'kriteria')