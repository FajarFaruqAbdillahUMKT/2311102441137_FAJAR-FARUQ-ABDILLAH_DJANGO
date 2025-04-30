from django.shortcuts import render
from django.http import HttpResponse


def home1(request):
    template_name = 'home-1.html'
    context = {
        'title': 'Fajar Faruq',
        'description': 'Developer Newbie',
        'body': 'Halaman Utama'
    }
    return render(request, template_name, context)

def home2(request):
    template_name = 'home-2.html'
    context = {
        'title': 'Fajar Faruq',
        'description': 'Developer Newbie',
        'body': 'Halaman Utama'
    }
    return render(request, template_name, context)

def home3(request):
    template_name = 'home-3.html'
    context = {
        'title': 'Fajar Faruq',
        'description': 'Developer Newbie',
        'body': 'Halaman Utama'
    }
    return render(request, template_name, context)

def home4(request):
    template_name = 'home-4.html'
    context = {
        'title': 'Fajar Faruq',
        'description': 'Developer Newbie',
        'body': 'Halaman Utama'
    }
    return render(request, template_name, context)

def home5(request):
    template_name = 'home-5.html'
    context = {
        'title': 'Fajar Faruq',
        'description': 'Developer Newbie',
        'body': 'Halaman Utama'
    }
    return render(request, template_name, context)

def home6(request):
    template_name = 'home-6.html'
    context = {
        'title': 'Fajar Faruq',
        'description': 'Developer Newbie',
        'body': 'Halaman Utama'
    }
    return render(request, template_name, context)

def portfolio1frl (request):
    template_name = 'portfolio-1-frl.html'
    context = {


    }
    return render(request, template_name, context)

def portfolio1stl (request):
    template_name = 'portfolio-1-stl.html'
    context = {

    }
    return render(request, template_name, context)


def portfolio2frl(request):
    template_name = 'portfolio-2-frl.html'
    context = {

    }
    return render(request, template_name, context)


def portfolio2stl(request):
    template_name = 'portfolio-2-stl.html'
    context = {

    }
    return render(request, template_name, context)


def portfolio3frl(request):
    template_name = 'portfolio-3-frl.html'
    context = {

    }
    return render(request, template_name, context)


def portfolio3stl(request):
    template_name = 'portfolio-3-stl.html'
    context = {

    }
    return render(request, template_name, context)




def servicefrl(request):
    template_name = 'service-frl.html'
    context = {

    }
    return render(request, template_name, context)

def servicestl(request):
    template_name = 'service-stl.html'
    context = {

    }
    return render(request, template_name, context)

def contactfrl(request):
    template_name = 'contact-frl.html'
    context = {


    }
    return render(request, template_name, context)

def contactstl(request):
    template_name = 'contact-stl.html'
    context = {


    }
    return render(request, template_name, context)

def teamfrl(request):
    template_name = 'team-frl.html'
    context = {

    }
    return render(request, template_name, context)

def teamstl(request):
    template_name = 'team-stl.html'
    context = {

    }
    return render(request, template_name, context)

