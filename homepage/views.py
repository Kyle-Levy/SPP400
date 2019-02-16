from django.shortcuts import render
from homepage.forms import LoginForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage


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
                email = EmailMessage('Hello', 'World', to=['gregory-malicki@uiowa.edu'])
                # email.send()
                login(request, user)
                return render(request, 'login.html', {'form': LoginForm()})
            else:
                return render(request, 'login.html', {'form': LoginForm()})

def log_out(request):
    logout(request)
    return render(request, 'login.html', {'form': LoginForm()})