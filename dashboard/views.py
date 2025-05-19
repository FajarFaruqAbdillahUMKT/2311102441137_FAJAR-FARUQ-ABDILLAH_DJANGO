from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404

from dashboard.models import Mahasiswa
from dashboard.forms import MahasiswaForm



# Create your views here.
def dashboard(request):
    template_name = 'dashboard/index.html'
    context = {}
    return render(request, template_name, context)


def login(request):
    template_name = 'dashboard/authentication/login.html'
    context = {}
    return render(request, template_name, context)


def daftar(request):
    template_name = 'dashboard/authentication/daftar.html'
    context = {}
    return render(request, template_name, context)

def list_mahasiswa(request):
    mahasiswas = Mahasiswa.objects.all()
    return render(request, 'dashboard/mahasiswa/list_mahasiswa.html', {'mahasiswas': mahasiswas})

def create_mahasiswa(request):
    if request.method == 'POST':
        form = MahasiswaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_mahasiswa')
    else:
        form = MahasiswaForm()
    return render(request, 'dashboard/mahasiswa/form_mahasiswa.html', {'form': form})

def update_mahasiswa(request, id):
    mahasiswa = get_object_or_404(Mahasiswa, id=id)
    if request.method == 'POST':
        form = MahasiswaForm(request.POST, instance=mahasiswa)
        if form.is_valid():
            form.save()
            return redirect('list_mahasiswa')
    else:
        form = MahasiswaForm(instance=mahasiswa)
    return render(request, 'dashboard/mahasiswa/form_mahasiswa.html', {'form': form})

def delete_mahasiswa(request, id):
    mahasiswa = get_object_or_404(Mahasiswa, id=id)
    if request.method == 'POST':
        mahasiswa.delete()
        return redirect('list_mahasiswa')
    return render(request, 'dashboard/mahasiswa/confirm_delete.html', {'mahasiswa': mahasiswa})
