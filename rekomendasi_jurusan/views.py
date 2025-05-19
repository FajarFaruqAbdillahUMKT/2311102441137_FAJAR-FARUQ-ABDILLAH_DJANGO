# dalam rekomendasi_jurusan/views.py

from django.shortcuts import render, redirect
from .forms import InputNilaiForm
from .models import Kriteria, Alternatif, Mahasiswa
import numpy as np


def input_nilai_dan_rekomendasi(request):
    hasil_akhir_rekomendasi_sorted = []  # Inisialisasi di awal
    form_data_for_template = {}

    if request.method == 'POST':
        form = InputNilaiForm(request.POST)
        if form.is_valid():
            form_data_for_template = form.cleaned_data

            mahasiswa_instance = Mahasiswa()
            if form_data_for_template.get('nama_mahasiswa'):
                mahasiswa_instance.nama_mahasiswa = form_data_for_template.get('nama_mahasiswa')
            if form_data_for_template.get('nim'):
                mahasiswa_instance.nim = form_data_for_template.get('nim')

            if mahasiswa_instance.nama_mahasiswa or mahasiswa_instance.nim:
                mahasiswa_instance.save()

            nilai_input_user = []
            daftar_kriteria_obj = Kriteria.objects.all().order_by('id')

            for kriteria_obj in daftar_kriteria_obj:
                nilai_input_user.append(form_data_for_template[f'nilai_{kriteria_obj.id}'])

            print(f"Nilai Input User (mentah): {nilai_input_user}")

            # --- MULAI BLOK LOGIKA TOPSIS ---
            alternatif_list = Alternatif.objects.all()

            # Fungsi konversi nilai (pastikan ini sesuai kebutuhan Anda)
            def konversi_nilai_ke_skala_1_5(nilai_0_100):
                if nilai_0_100 >= 80: return 5.0
                if nilai_0_100 >= 70: return 4.0  # Contoh penyesuaian skala, atau gunakan skala Anda
                if nilai_0_100 >= 60: return 3.0
                if nilai_0_100 >= 40: return 2.0
                return 1.0

            matriks_X_user = np.array([[konversi_nilai_ke_skala_1_5(n) for n in nilai_input_user]])
            print(f"Matriks X User (setelah konversi 1-5): {matriks_X_user}")

            hasil_akhir_rekomendasi = []  # Inisialisasi list untuk hasil per alternatif

            if not alternatif_list.exists() or not daftar_kriteria_obj.exists():
                print("Tidak ada data Alternatif atau Kriteria di database.")
                # hasil_akhir_rekomendasi_sorted akan tetap []
            else:
                for alt_obj in alternatif_list:
                    print(f"\n--- Menghitung untuk Alternatif: {alt_obj.nama_alternatif} ---")
                    if alt_obj.kode_alternatif.upper() == 'JRS':
                        bobot_kriteria = np.array([k.bobot_jrs for k in daftar_kriteria_obj])
                    elif alt_obj.kode_alternatif.upper() == 'KC':
                        bobot_kriteria = np.array([k.bobot_kc for k in daftar_kriteria_obj])
                    else:
                        print(f"Bobot untuk {alt_obj.nama_alternatif} tidak terdefinisi, dilewati.")
                        continue

                    # Pastikan jumlah bobot sesuai dengan jumlah kriteria di matriks_X_user
                    if len(bobot_kriteria) != matriks_X_user.shape[1]:
                        print(
                            f"ERROR: Jumlah bobot ({len(bobot_kriteria)}) tidak sama dengan jumlah kriteria di matriks X ({matriks_X_user.shape[1]}) untuk {alt_obj.nama_alternatif}.")
                        continue

                    print(f"Bobot Kriteria ({alt_obj.kode_alternatif}): {bobot_kriteria}")

                    sum_squared_X = np.sum(matriks_X_user ** 2)
                    print(f"Sum Squared X: {sum_squared_X}")

                    if sum_squared_X == 0:
                        print("Sum Squared X adalah 0, normalisasi mungkin tidak ideal.")
                        norm_X_user_row = np.zeros_like(matriks_X_user, dtype=float)  # Handle pembagian dengan nol
                    else:
                        norm_X_user_row = matriks_X_user / np.sqrt(sum_squared_X)

                    print(f"Norm X User Row: {norm_X_user_row}")

                    Y_user_row = norm_X_user_row * bobot_kriteria
                    print(f"Y User Row (ternormalisasi terbobot): {Y_user_row}")

                    # Definisi A+ dan A- (ini mungkin perlu direvisi lebih lanjut untuk akurasi)
                    A_plus_ideal = bobot_kriteria
                    A_minus_ideal = np.zeros_like(bobot_kriteria)
                    print(f"A+ Ideal: {A_plus_ideal}")
                    print(f"A- Ideal: {A_minus_ideal}")

                    D_plus_user = np.sqrt(np.sum((Y_user_row - A_plus_ideal) ** 2))
                    D_minus_user = np.sqrt(np.sum((Y_user_row - A_minus_ideal) ** 2))
                    print(f"D+ User: {D_plus_user}")
                    print(f"D- User: {D_minus_user}")

                    epsilon = 1e-9
                    pembagi_V = D_plus_user + D_minus_user + epsilon
                    print(f"Pembagi V (D+ + D- + epsilon): {pembagi_V}")

                    V_user = 0.0  # Default value
                    if pembagi_V != 0:  # Atau if abs(pembagi_V) > epsilon:
                        V_user = D_minus_user / pembagi_V
                    else:  # Jika D+ dan D- keduanya 0
                        if D_plus_user == 0 and D_minus_user == 0:  # Sempurna cocok dengan A+ dan A- (jarang terjadi dengan A- = 0)
                            V_user = 0.5  # Atau nilai lain yang menunjukkan ambiguitas/kecocokan merata
                        print("Pembagi V adalah 0 atau sangat kecil, V_user diatur berdasarkan kondisi D+/D-.")

                    print(f"Nilai V User: {V_user}")

                    hasil_akhir_rekomendasi.append({
                        'alternatif': alt_obj.nama_alternatif,
                        'kode': alt_obj.kode_alternatif,
                        'nilai_v': V_user
                    })

                print(f"\nHasil Rekomendasi (sebelum sortir): {hasil_akhir_rekomendasi}")
                if not hasil_akhir_rekomendasi:
                    hasil_akhir_rekomendasi_sorted = []
                else:
                    hasil_akhir_rekomendasi_sorted = sorted(hasil_akhir_rekomendasi, key=lambda k: k['nilai_v'],
                                                            reverse=True)
            # --- AKHIR BLOK LOGIKA TOPSIS ---

            print(f"Hasil Rekomendasi (sesudah sortir): {hasil_akhir_rekomendasi_sorted}")

            return render(request, 'rekomendasi_jurusan/hasil_rekomendasi.html', {
                'hasil': hasil_akhir_rekomendasi_sorted,
                'form_data': form_data_for_template
            })
        else:
            return render(request, 'rekomendasi_jurusan/form_input_nilai.html', {'form': form})
    else:
        form = InputNilaiForm()
        return render(request, 'rekomendasi_jurusan/form_input_nilai.html', {'form': form})