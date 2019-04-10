from django.shortcuts import render, redirect

from assigned_procedures.models import AssignedProcedures
from homepage.forms import LoginForm, NewKeyForm, AuthenticateForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from patients.models import Patients
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


@login_required()
def homepage(request):
    if request.method == 'GET':
        return render(request, 'homepage.html', {'title':'Home', 'patients' : Patients.objects.all(), 'alert_patients': AssignedProcedures.update_and_return_all_patient_goal_flags()})


def log_in(request):
    # Login session cookies cleared for login, 'request.session.modified = True' saves it
    request.session['username'] = {}
    request.session['password'] = {}
    request.session.modified = True

    if request.method == 'GET':
        return render(request, 'login.html', {'form': LoginForm()})
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # Clean form data and check that the username password pair is valid
            cd = form.cleaned_data
            cd['username'] = cd['username'].lower()
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.profile.expired():
                    # Store username and password as cookies temporarily for two-factor
                    request.session['username'] = cd['username']
                    request.session['password'] = cd['password']
                    user.profile.new_key()
                    return render(request, 'authenticate.html', {'form': AuthenticateForm()}, status=200)
                else:
                    login(request, user)
                    return redirect('/homepage/')
            else:
                return render(request, 'login.html', {'form': LoginForm(), 'failed_login': True}, status=401)


def log_out(request):
    logout(request)
    return render(request, 'login.html', {'form': LoginForm(), 'logged_out': True})


'''
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
'''


def authenticator(request):
    if request.method == 'POST':
        user = authenticate(username=request.session['username'], password=request.session['password'])
        form = AuthenticateForm(request.POST)
        if form.is_valid():
            key = form.cleaned_data['key']
            if user.profile.check_key(key):
                login(request, user)
                request.session['username'] = {}
                request.session['password'] = {}
                request.session.modified = True
                return redirect('/homepage/')
            # this should cause an error to show up
            return render(request, 'authenticate.html', {'form': AuthenticateForm(), 'bad_code': True}, status=401)
