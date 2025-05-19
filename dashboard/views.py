from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CustomUserCreationForm, MahasiswaForm
from .models import Mahasiswa


# Create your views here.
def dashboard(request):
    template_name = 'dashboard/index.html'
    context = {}
    return render(request, template_name, context)


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('username')  # Mengambil email dari kolom 'username'
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)  # Gunakan username=email
        if user is not None:
            login(request, user)
            messages.success(request, 'Login berhasil.')
            return redirect('dashboard:list_mahasiswa')
        else:
            messages.error(request, 'Email atau kata sandi salah.')
    return render(request, 'dashboard/authentication/login.html')


def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Akun berhasil dibuat. Silakan login.')
            return redirect('dashboard:login')
        else:
            messages.error(request, 'Terjadi kesalahan. Periksa data yang Anda masukkan.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'dashboard/authentication/daftar.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'Anda telah berhasil keluar.')
    return redirect('dashboard:login')


@login_required
def list_mahasiswa(request):
    mahasiswas = Mahasiswa.objects.all()
    return render(request, 'dashboard/mahasiswa/list_mahasiswa.html', {'mahasiswas': mahasiswas})


@login_required
def create_mahasiswa(request):
    if request.method == 'POST':
        form = MahasiswaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard:list_mahasiswa')
    else:
        form = MahasiswaForm()
    return render(request, 'dashboard/mahasiswa/form_mahasiswa.html', {'form': form})


@login_required
def update_mahasiswa(request, id):
    mahasiswa = get_object_or_404(Mahasiswa, id=id)
    if request.method == 'POST':
        form = MahasiswaForm(request.POST, instance=mahasiswa)
        if form.is_valid():
            form.save()
            return redirect('dashboard:list_mahasiswa')
    else:
        form = MahasiswaForm(instance=mahasiswa)
    return render(request, 'dashboard/mahasiswa/form_mahasiswa.html', {'form': form})


@login_required
def delete_mahasiswa(request, id):
    mahasiswa = get_object_or_404(Mahasiswa, id=id)
    if request.method == 'POST':
        mahasiswa.delete()
        return redirect('dashboard:list_mahasiswa')
    return render(request, 'dashboard/mahasiswa/confirm_delete.html', {'mahasiswa': mahasiswa})

def list_nilai(request):
    nilai = Nilai.objects.all()
    return render(request, 'dashboard/nilai/nilai.html', {'nilai': nilai})

def input_nilai(request):
    if request.method == 'POST':
        form = NilaiForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard/nilai/nilai.html')
    else:
        form = NilaiForm()
    return render(request, 'dashboard/mahasiswa/form_mahasiswa.html', {'form': form})