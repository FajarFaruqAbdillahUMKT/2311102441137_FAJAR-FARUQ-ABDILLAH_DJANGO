# rekomendasi_jurusan/views.py

from django.shortcuts import render
from .forms import InputNilaiForm
from .models import Kriteria, Alternatif, Mahasiswa, NilaiMataKuliah, HasilRekomendasi
import numpy as np
import pandas as pd  # Impor library pandas


def input_nilai_dan_rekomendasi(request):
    # Logika untuk menampilkan form (request GET) tetap sama
    if request.method != 'POST':
        form = InputNilaiForm()
        return render(request, 'rekomendasi_jurusan/form_input_nilai.html', {'form': form})

    # Logika saat form di-submit (request POST)
    form = InputNilaiForm(request.POST)
    if not form.is_valid():
        # Jika form tidak valid, tampilkan kembali dengan error
        return render(request, 'rekomendasi_jurusan/form_input_nilai.html', {'form': form})

    # =======================================================================
    # BAGIAN 1: SIMPAN DATA MAHASISWA BARU (Logika ini tetap dipertahankan)
    # =======================================================================
    mahasiswa_baru_instance = Mahasiswa.objects.create(
        nama_mahasiswa=form.cleaned_data.get('nama_mahasiswa'),
        nim=form.cleaned_data.get('nim')
    )

    daftar_kriteria_obj = Kriteria.objects.order_by('id')

    for kriteria_obj in daftar_kriteria_obj:
        nilai = form.cleaned_data[f'nilai_{kriteria_obj.id}']
        NilaiMataKuliah.objects.create(
            mahasiswa=mahasiswa_baru_instance,
            kriteria=kriteria_obj,
            nilai_mentah=nilai
        )

    # =======================================================================
    # BAGIAN 2: PERSIAPAN MATRIKS KEPUTUSAN LENGKAP (Logika Baru)
    # =======================================================================

    # Ambil semua data nilai dari database (termasuk data yang baru dimasukkan)
    semua_nilai_qs = NilaiMataKuliah.objects.all().values(
        'mahasiswa_id', 'kriteria_id', 'nilai_mentah'
    )

    # Jika tidak ada data sama sekali, hentikan proses
    if not semua_nilai_qs.exists():
        # Anda bisa menampilkan pesan error di sini
        return render(request, 'rekomendasi_jurusan/hasil_rekomendasi.html',
                      {'error': 'Tidak ada data nilai di database.'})

    # Gunakan Pandas untuk mengubah data menjadi matriks (pivot table)
    df = pd.DataFrame(list(semua_nilai_qs))

    def konversi_nilai_ke_skala_1_5(nilai_0_100):
        if nilai_0_100 >= 80: return 5.0
        if nilai_0_100 >= 70: return 4.0
        if nilai_0_100 >= 60: return 3.0
        if nilai_0_100 >= 50: return 2.0
        return 1.0

    # Terapkan fungsi konversi ke semua nilai
    df['nilai_konversi'] = df['nilai_mentah'].apply(konversi_nilai_ke_skala_1_5)

    # Buat matriks: baris adalah mahasiswa_id, kolom adalah kriteria_id
    matriks_keputusan_df = df.pivot_table(
        index='mahasiswa_id',
        columns='kriteria_id',
        values='nilai_konversi'
    ).fillna(0)  # Ganti nilai kosong (jika ada) dengan 0

    # Urutkan kolom berdasarkan ID kriteria agar konsisten
    matriks_keputusan_df = matriks_keputusan_df.reindex(
        columns=[k.id for k in daftar_kriteria_obj]
    )

    # Simpan urutan ID mahasiswa untuk referensi nanti
    urutan_mahasiswa_id = matriks_keputusan_df.index.tolist()

    # Konversi DataFrame ke NumPy array untuk perhitungan
    matriks_X_lengkap = matriks_keputusan_df.to_numpy()

    # =======================================================================
    # BAGIAN 3: LOGIKA TOPSIS PADA MATRIKS LENGKAP
    # =======================================================================
    alternatif_list = Alternatif.objects.all()

    for alt_obj in alternatif_list:
        if alt_obj.kode_alternatif.upper() == 'JRS':
            bobot_kriteria = np.array([k.bobot_jrs for k in daftar_kriteria_obj])
        elif alt_obj.kode_alternatif.upper() == 'KC':
            bobot_kriteria = np.array([k.bobot_kc for k in daftar_kriteria_obj])
        else:
            continue

        # 1. Normalisasi (pembagi dihitung per kolom, axis=0 sekarang sudah BENAR)
        pembagi = np.sqrt(np.sum(matriks_X_lengkap ** 2, axis=0))
        pembagi[pembagi == 0] = 1e-9  # Hindari pembagian dengan nol
        matriks_ternormalisasi = matriks_X_lengkap / pembagi

        # 2. Normalisasi Terbobot
        matriks_terbobot = matriks_ternormalisasi * bobot_kriteria

        # 3. Solusi Ideal Positif (A+) dan Negatif (A-)
        # Asumsi semua kriteria adalah benefit (nilai lebih tinggi lebih baik)
        A_plus = np.max(matriks_terbobot, axis=0)
        A_minus = np.min(matriks_terbobot, axis=0)

        # 4. Jarak ke Solusi Ideal (menghasilkan array untuk semua mahasiswa)
        D_plus = np.sqrt(np.sum((matriks_terbobot - A_plus) ** 2, axis=1))
        D_minus = np.sqrt(np.sum((matriks_terbobot - A_minus) ** 2, axis=1))

        # 5. Nilai Preferensi (V) (menghasilkan array untuk semua mahasiswa)
        V_all = D_minus / (D_plus + D_minus + 1e-9)

        # Simpan atau perbarui hasil untuk semua mahasiswa
        for i, mhs_id in enumerate(urutan_mahasiswa_id):
            HasilRekomendasi.objects.update_or_create(
                mahasiswa_id=mhs_id,
                alternatif=alt_obj,
                defaults={'skor': V_all[i]}
            )

    # =======================================================================
    # BAGIAN 4: AMBIL & TAMPILKAN HASIL UNTUK MAHASISWA BARU
    # =======================================================================

    # Ambil kembali hasil yang sudah dihitung untuk mahasiswa yang baru input
    hasil_untuk_user = HasilRekomendasi.objects.filter(mahasiswa=mahasiswa_baru_instance).order_by('-skor')

    hasil_untuk_ditampilkan = [{
        'alternatif': h.alternatif.nama_alternatif,
        'kode': h.alternatif.kode_alternatif,
        'nilai_v': h.skor
    } for h in hasil_untuk_user]

    # Simpan rekomendasi final ke record mahasiswa baru
    if hasil_untuk_user:
        rekomendasi_terbaik = hasil_untuk_user.first()
        mahasiswa_baru_instance.rekomendasi_final = rekomendasi_terbaik.alternatif
        mahasiswa_baru_instance.skor_final = rekomendasi_terbaik.skor
        mahasiswa_baru_instance.save()

    return render(request, 'rekomendasi_jurusan/hasil_rekomendasi.html', {
        'hasil': hasil_untuk_ditampilkan,
        'form_data': form.cleaned_data
    })
