from django.shortcuts import render
from homepage.forms import LoginForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone


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
            print("form is valid")
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                # user.profile.new_key()
                print("expiration: " + str(user.profile.key_expiration))
                print("curre time:" + str(timezone.now()))
                if user.profile.expired():
                    print("2 factor expired")
                    if user.profile.check_key(cd['auth_key']):
                        print("2 factor validated")
                        login(request, user)
                        return render(request, 'homepage.html', {'form': LoginForm(), 'failed_login': False, 'two_factor': True}, status=200)
                    return render(request, 'login.html', {'form': LoginForm(), 'failed_login': True, 'two_factor': True}, status=401)
                else:
                    print("2 factor still valid")
                    login(request, user)
                    return render(request, 'homepage.html', {'form': LoginForm(), 'failed_login': False}, status=200)
            else:
                return render(request, 'homepage.html', {'form': LoginForm(), 'failed_login': False}, status=200)


def log_out(request):
    logout(request)
    return render(request, 'login.html', {'form': LoginForm(), 'logged_out': True})
