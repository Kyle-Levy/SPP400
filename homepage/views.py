from django.shortcuts import render
from homepage.forms import LoginForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
# Create your views here.


def home(request):
    return render(request, 'login.html', {'form': LoginForm()})
    #  return HttpResponse('<h1> Homepage </h1>')


def about(request):
    return HttpResponse('<h1> Testerooni </h1>')


def log_in(request):
    if request.method == 'GET':
        return render(request, 'login.html', {'form': LoginForm()})
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                return render(request, 'login.html', {'form': LoginForm()})
            else:
                return render(request, 'login.html', {'form': LoginForm()})
