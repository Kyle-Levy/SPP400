from django.shortcuts import render
from homepage.forms import LoginForm, NewKeyForm, AuthenticateForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

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
                request.session['username'] = cd['username']
                request.session['password'] = cd['password']
                if user.profile.expired():
                    return render(request, 'authenticate.html', {'form': AuthenticateForm()}, status=401)
                else:
                    login(request, user)
                    return render(request, 'homepage.html', {'form': LoginForm(), 'failed_login': False}, status=200)
            else:
                return render(request, 'login.html', {'form': LoginForm(), 'failed_login': True}, status=401)


def log_out(request):
    logout(request)
    return render(request, 'login.html', {'form': LoginForm(), 'logged_out': True})


def new_code(request):
    if request.method == 'GET':
        return render(request, 'new_key.html', {'form': NewKeyForm(), 'failed_login': False, 'two_factor': True}, status=200)
    if request.method == 'POST':
        form = NewKeyForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            try:
                user = User.objects.get(username=cd['username'])
                user.profile.new_key()
                return render(request, 'login.html', {'form': LoginForm(), 'failed_login': False, 'two_factor': True}, status=200)

            except ObjectDoesNotExist:
                return render(request, 'new_key.html', {'form': NewKeyForm(), 'failed_login': False, 'two_factor': True}, status=200)


def authenticator(request):
    if request.method == 'POST':
        user = authenticate(username=request.session['username'], password=request.session['password'])
        form = AuthenticateForm(request.POST)
        if form.is_valid():
            key = form.cleaned_data['key']
            if user.profile.check_key(key):
                login(request, user)
                return render(request, 'homepage.html', status=200)
            return render(request, 'authenticate.html', {'form': AuthenticateForm()}, status=401)
