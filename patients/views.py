from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from patients.forms import NewPatient
from patients.models import Patients


def index(request):
    if request.method == 'GET':
        return render(request, 'landing_page.html', {'patients': Patients.objects.all()})


@login_required
def new_patient(request):
    if request.method == 'GET':
        return render(request, 'new_patient.html', {'form': NewPatient()})
    if request.method == 'POST':
        form = NewPatient(request.POST)
        if form.is_valid():
            # Clean form data and check that the username password pair is valid
            cd = form.cleaned_data
            patient = Patients.create_patient(cd['first_name'], cd['last_name'], cd['birth_date'])
            patient.save()
            return redirect('/homepage/')
        else:
            return render(request, 'new_patient.html', {'form': NewPatient(), 'failed_creation': True}, status=401)


@login_required
def profile(request):
    if request.method == 'GET':
        try:
            # Get desired patient id from url
            patient = Patients.objects.get(id=request.GET.get('id'))#request.session['patient_id'])
            return render(request, 'patient.html', {"patient": patient})
        except Patients.DoesNotExist:
            # TODO: add in error message here
            return redirect('/patients/')
