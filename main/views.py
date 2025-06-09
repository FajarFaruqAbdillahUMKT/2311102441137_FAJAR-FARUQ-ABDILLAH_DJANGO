from django.shortcuts import render



def home(request):
    template_name = 'main/index.html'
    context = {}
    return render(request, template_name, context)

def teamfrl(request):
    template_name = 'main/team-frl.html'
    context = {}
    return render(request, template_name, context)

# def login(request):
#     template_name = 'dashboard/login.html'
#     context = {}
#     return render(request, template_name, context)

