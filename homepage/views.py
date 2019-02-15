from django.shortcuts import render
from homepage.forms import LoginForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    return HttpResponse('<h1> Homepage </h1>')


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
                return render(request, 'homepage.html', {'form': LoginForm(), 'failed_login': False}, status=200)
            else:
                return render(request, 'login.html', {'form': LoginForm(), 'failed_login': True}, status=401)


def log_out(request):
    logout(request)
    return render(request, 'login.html', {'form': LoginForm(), 'logged_out': True})
