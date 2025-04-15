from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    template_name = 'home-1.html'
    context = {
        'title': 'Fajar Faruq',
        'description': 'Developer Newbie',
        'body': 'Halaman Utama'
    }
    return render(request, template_name, context)

def service(request):
    template_name = 'service-frl.html'
    context = {

    }
    return render(request, template_name, context)

def contact(request):
    template_name = 'contact-frl.html'
    context = {

        }


    return render(request, template_name, context)