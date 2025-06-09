# rekomendasi_jurusan/admin.py

from django.contrib import admin
from .models import Kriteria, Alternatif, Mahasiswa, NilaiMataKuliah, HasilRekomendasi
from import_export.admin import ImportExportModelAdmin


# 1. Tampilan untuk Data Master (Kriteria & Alternatif)
# =======================================================

@admin.register(Kriteria)
class KriteriaAdmin(admin.ModelAdmin):
    list_display = ('id','nama_kriteria', 'bobot_jrs', 'bobot_kc')
    search_fields = ('nama_kriteria',)
    list_per_page = 20


@admin.register(Alternatif)
class AlternatifAdmin(admin.ModelAdmin):
    list_display = ('nama_alternatif', 'kode_alternatif')
    search_fields = ('nama_alternatif', 'kode_alternatif')


# 2. Pengaturan Tampilan Inline untuk Halaman Mahasiswa
# =======================================================
# Ini memungkinkan Anda mengedit nilai dan melihat hasil langsung di halaman Mahasiswa.

class NilaiMataKuliahInline(admin.TabularInline):
    """Tampilan inline untuk menginput nilai mata kuliah."""
    model = NilaiMataKuliah
    extra = 1  # Jumlah baris kosong untuk input baru
    autocomplete_fields = ['kriteria']  # Memudahkan pencarian kriteria/matkul


class HasilRekomendasiInline(admin.TabularInline):
    """Tampilan inline untuk menampilkan hasil skor (tidak bisa diedit)."""
    model = HasilRekomendasi
    extra = 0  # Tidak perlu baris kosong karena ini hasil kalkulasi
    readonly_fields = ('alternatif', 'skor')  # Hasil tidak boleh diubah manual
    can_delete = False  # Hasil tidak boleh dihapus dari sini

    def has_add_permission(self, request, obj=None):
        return False  # Menonaktifkan tombol "Add another..."


# 3. Tampilan Utama untuk Sesi Mahasiswa (SPK)
# ================================================
# Ini adalah tampilan admin yang paling penting.

@admin.register(Mahasiswa)
class MahasiswaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    # Kolom yang ditampilkan di daftar utama
    list_display = ('id', 'nama_mahasiswa', 'nim', 'rekomendasi_final', 'skor_final', 'timestamp')

    # Filter di sisi kanan
    list_filter = ('rekomendasi_final', 'timestamp')

    # Fitur pencarian
    search_fields = ('nama_mahasiswa', 'nim', 'id')

    # Membuat field hasil hanya bisa dibaca (read-only)
    readonly_fields = ('rekomendasi_final', 'skor_final', 'timestamp')

    # Menggabungkan tampilan Nilai dan Hasil ke dalam halaman Mahasiswa
    inlines = [NilaiMataKuliahInline, HasilRekomendasiInline]

    fieldsets = (
        ('Informasi Sesi', {
            'fields': ('nama_mahasiswa', 'nim')
        }),
        ('Hasil Akhir Rekomendasi (Dihitung Otomatis)', {
            'fields': ('rekomendasi_final', 'skor_final', 'timestamp')
        }),
    )


# Catatan: Model NilaiMataKuliah dan HasilRekomendasi tidak perlu didaftarkan
# secara terpisah karena sudah dikelola melalui 'inlines' di MahasiswaAdmin.
# Jika Anda tetap ingin bisa mengaksesnya secara terpisah, Anda bisa uncomment baris di bawah:
# admin.site.register(NilaiMataKuliah)
# admin.site.register(HasilRekomendasi)

class CustomNilaiMataKuliahAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('mahasiswa', 'kriteria', 'nilai_mentah')
    search_fields = ('mahasiswa__nama_mahasiswa', 'kriteria__nama_kriteria')
    list_filter = ('kriteria',)

admin.site.register(NilaiMataKuliah,  CustomNilaiMataKuliahAdmin)
