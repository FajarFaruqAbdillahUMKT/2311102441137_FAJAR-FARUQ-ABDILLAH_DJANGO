# rekomendasi_jurusan/views.py

from django.shortcuts import render
from .forms import InputNilaiForm
from .models import Kriteria, Alternatif, Mahasiswa, NilaiMataKuliah, HasilRekomendasi
import numpy as np
import pandas as pd
import json


def input_nilai_dan_rekomendasi(request):
    # Bagian form GET dan validasi POST tetap sama
    if request.method != 'POST':
        form = InputNilaiForm()
        return render(request, 'rekomendasi_jurusan/form_input_nilai.html', {'form': form})

    form = InputNilaiForm(request.POST)
    if not form.is_valid():
        return render(request, 'rekomendasi_jurusan/form_input_nilai.html', {'form': form})

    # Bagian 1: Simpan Mahasiswa dan Nilai (Tidak berubah)
    mahasiswa_baru_instance = Mahasiswa.objects.create(
        nama_mahasiswa=form.cleaned_data.get('nama_mahasiswa'),
        nim=form.cleaned_data.get('nim')
    )
    daftar_kriteria_obj = Kriteria.objects.order_by('id')
    for kriteria_obj in daftar_kriteria_obj:
        nilai = form.cleaned_data[f'nilai_{kriteria_obj.id}']
        NilaiMataKuliah.objects.create(
            mahasiswa=mahasiswa_baru_instance, kriteria=kriteria_obj, nilai_mentah=nilai
        )

    # Bagian 2 & 3: Proses TOPSIS (Tidak berubah)
    semua_nilai_qs = NilaiMataKuliah.objects.all().values('mahasiswa_id', 'kriteria_id', 'nilai_mentah')
    if not semua_nilai_qs.exists():
        return render(request, 'rekomendasi_jurusan/hasil_rekomendasi.html', {'error': 'Tidak ada data nilai.'})
    df = pd.DataFrame(list(semua_nilai_qs))

    def konversi_nilai_ke_skala_1_5(nilai_0_100):
        if nilai_0_100 >= 80: return 5.0;
        if nilai_0_100 >= 70: return 4.0;
        if nilai_0_100 >= 60: return 3.0;
        if nilai_0_100 >= 50: return 2.0;
        return 1.0

    df['nilai_konversi'] = df['nilai_mentah'].apply(konversi_nilai_ke_skala_1_5)
    matriks_keputusan_df = df.pivot_table(index='mahasiswa_id', columns='kriteria_id', values='nilai_konversi').fillna(
        0)
    matriks_keputusan_df = matriks_keputusan_df.reindex(columns=[k.id for k in daftar_kriteria_obj])
    urutan_mahasiswa_id = matriks_keputusan_df.index.tolist()
    matriks_X_lengkap = matriks_keputusan_df.to_numpy()
    for alt_obj in Alternatif.objects.all():
        bobot_kriteria = np.array(
            [k.bobot_jrs for k in daftar_kriteria_obj]) if alt_obj.kode_alternatif.upper() == 'JRS' else np.array(
            [k.bobot_kc for k in daftar_kriteria_obj])
        pembagi = np.sqrt(np.sum(matriks_X_lengkap ** 2, axis=0));
        pembagi[pembagi == 0] = 1e-9
        matriks_ternormalisasi = matriks_X_lengkap / pembagi
        matriks_terbobot = matriks_ternormalisasi * bobot_kriteria
        A_plus = np.max(matriks_terbobot, axis=0);
        A_minus = np.min(matriks_terbobot, axis=0)
        D_plus = np.sqrt(np.sum((matriks_terbobot - A_plus) ** 2, axis=1));
        D_minus = np.sqrt(np.sum((matriks_terbobot - A_minus) ** 2, axis=1))
        V_all = D_minus / (D_plus + D_minus + 1e-9)
        for i, mhs_id in enumerate(urutan_mahasiswa_id):
            HasilRekomendasi.objects.update_or_create(
                mahasiswa_id=mhs_id, alternatif=alt_obj, defaults={'skor': V_all[i]}
            )

    # =======================================================================
    # BAGIAN 4: LOGIKA PENENTUAN 4 KONDISI REKOMENDASI (BARU)
    # =======================================================================
    hasil_user_qs = HasilRekomendasi.objects.filter(mahasiswa=mahasiswa_baru_instance).select_related(
        'alternatif').order_by('-skor')

    # Definisikan ambang batas
    LOW_SCORE_THRESHOLD = 0.3333  # Ambang batas skor rendah
    TIE_TOLERANCE = 1e-7  # Toleransi untuk perbandingan angka imbang

    # Inisialisasi variabel kontrol
    jenis_rekomendasi = None
    konteks_tambahan = {}
    skor_jrs, skor_kc = 0, 0

    if hasil_user_qs.count() == 2:
        try:
            hasil_jrs = hasil_user_qs.get(alternatif__kode_alternatif='JRS')
            hasil_kc = hasil_user_qs.get(alternatif__kode_alternatif='KC')
            skor_jrs = hasil_jrs.skor
            skor_kc = hasil_kc.skor

            # ==========================================================
            # ===== TAMBAHKAN PRINT UNTUK DEBUGGING DI SINI =====
            # ==========================================================
            print("--- MEMULAI DEBUGGING SKOR ---")
            print(f"SKOR JRS (mentah): {skor_jrs}")
            print(f"SKOR KC (mentah): {skor_kc}")
            selisih_skor = abs(skor_jrs - skor_kc)
            print(f"SELISIH ABSOLUT: {selisih_skor}")
            print(f"APAKAH SELISIH < TOLERANSI ({TIE_TOLERANCE})? {selisih_skor < TIE_TOLERANCE}")
            # ==========================================================

            skor_tertinggi = max(skor_jrs, skor_kc)

            # 1. Prioritas utama: Cek jika skor terlalu rendah
            if skor_tertinggi < LOW_SCORE_THRESHOLD:
                jenis_rekomendasi = 'rendah'
                konteks_tambahan[
                    'pesan'] = f"Skor tertinggi Anda ({skor_tertinggi:.2f}) di bawah ambang batas kelayakan ({LOW_SCORE_THRESHOLD}). Kami sarankan untuk meningkatkan nilai Anda sebelum memilih fokus penjurusan."

            # 2. Cek jika skor imbang (dan tidak rendah)
            elif abs(skor_jrs - skor_kc) < TIE_TOLERANCE:
                jenis_rekomendasi = 'imbang'
                kriteria_all = Kriteria.objects.order_by('id')
                konteks_tambahan['pembeda_jurusan'] = [{
                    'nama': k.nama_kriteria, 'bobot_jrs': k.bobot_jrs, 'bobot_kc': k.bobot_kc,
                    'highlight': 'jrs' if k.bobot_jrs > k.bobot_kc else ('kc' if k.bobot_kc > k.bobot_jrs else 'sama')
                } for k in kriteria_all]

            # 3. Cek jika KC lebih tinggi
            elif skor_kc > skor_jrs:
                jenis_rekomendasi = 'kc'

            # 4. Sisanya, pasti JRS lebih tinggi
            else:
                jenis_rekomendasi = 'jrs'

        except HasilRekomendasi.DoesNotExist:
            # Jika salah satu alternatif tidak ada, anggap sebagai error/kondisi normal
            jenis_rekomendasi = 'normal'

    # Menyiapkan data yang akan dikirim ke template
    nilai_mentah_user = NilaiMataKuliah.objects.filter(mahasiswa=mahasiswa_baru_instance).order_by('kriteria__id')
    chart_data = {
        'labels': [n.kriteria.nama_kriteria for n in nilai_mentah_user],
        'nilai': [n.nilai_mentah for n in nilai_mentah_user]
    }

    # Simpan rekomendasi final HANYA JIKA ada pemenang yang jelas dan tidak rendah
    if jenis_rekomendasi in ['jrs', 'kc']:
        rekomendasi_terbaik = hasil_user_qs.first()  # .first() akan mengambil skor tertinggi
        mahasiswa_baru_instance.rekomendasi_final = rekomendasi_terbaik.alternatif
        mahasiswa_baru_instance.skor_final = rekomendasi_terbaik.skor
        mahasiswa_baru_instance.save()

    return render(request, 'rekomendasi_jurusan/hasil_rekomendasi.html', {
        'hasil': hasil_user_qs,
        'form_data': form.cleaned_data,
        'nilai_mentah': nilai_mentah_user,
        'chart_data_json': json.dumps(chart_data),
        'jenis_rekomendasi': jenis_rekomendasi,  # Sinyal penentu tampilan
        'konteks_tambahan': konteks_tambahan,
        'skor_jrs': skor_jrs,
        'skor_kc': skor_kc
    })
