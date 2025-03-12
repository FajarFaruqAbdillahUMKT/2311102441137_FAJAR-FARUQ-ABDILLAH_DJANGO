from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    template_name = 'home.html'
    context = {
        'title': 'Fajar Faruq',
        'description': 'Developer Newbie',
        'body': 'Halaman Utama'
    }
    return render(request, template_name, context)

def about(request):
    template_name = 'about.html'
    context = {
        'title': 'About Me',
        'description': 'Tentang Saya',
        'body': 'Halaman About'
    }
    return render(request, template_name, context)