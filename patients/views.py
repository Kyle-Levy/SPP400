from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from patients.forms import NewPatient
from patients.models import Patients


@login_required
def index(request):
    if request.method == 'GET':
        return render(request, 'landing_page.html', {'patients': Patients.objects.all(), 'title': 'Patients'})


@login_required
def new_patient(request):
    if request.method == 'GET':
        return render(request, 'new_patient.html', {'form': NewPatient(), 'title': 'New Patient'})
    if request.method == 'POST':
        form = NewPatient(request.POST)
        if form.is_valid():
            # Clean form data and check that the username password pair is valid
            cd = form.cleaned_data
            patient = Patients.create_patient(cd['first_name'], cd['last_name'], cd['birth_date'])
            patient.save()
            return redirect('/homepage/')
        else:
            return render(request, 'new_patient.html',
                          {'form': NewPatient(), 'failed_creation': True, 'title': 'New Patient'}, status=401)


@login_required
def profile(request):
    if request.method == 'POST':
        try:
            # Get desired patient id from url
            patient = Patients.objects.get(id=request.GET.get('id'))
            request.session['patient_id'] = request.GET.get('id')
            return render(request, 'update_patient.html', {'form': NewPatient(), 'patient': patient,
                                                           'title': 'Update: ' + patient.last_name + ', ' + patient.first_name})
        except Patients.DoesNotExist:
            # TODO: add in error message here
            return redirect('/patients/')

    if request.method == 'GET':
        try:
            # Get desired patient id from url
            patient = Patients.objects.get(id=request.GET.get('id'))
            return render(request, 'patient.html',
                          {"patient": patient, 'title': 'Profile: ' + patient.last_name + ', ' + patient.first_name})
        except Patients.DoesNotExist:
            # TODO: add in error message here
            return redirect('/patients/')


@login_required
def update(request):
    if request.method == 'POST':
        form = NewPatient(request.POST)
        if form.is_valid():
            # Clean form data and check that the username password pair is valid
            cd = form.cleaned_data
            try:
                # Get desired patient id from url
                patient = Patients.objects.get(id=request.session['patient_id'])
                patient.first_name = cd['first_name']
                patient.last_name = cd['last_name']
                patient.bday = cd['birth_date']
                patient.save()
                return redirect("/patients/profile/?id=" + str(patient.id))
            except Patients.DoesNotExist:
                # TODO: add in error message here
                return redirect('/patients/')
        else:
            return redirect('/patients/')


@login_required
def delete(request):
    # TODO: This method can be dangerous if patient_id isnt properly set i think
    if request.method == 'POST':
        try:
            # Get desired patient id from url
            patient = Patients.objects.get(id=request.session['patient_id'])
            patient.delete()
            return redirect("/patients/")
        except Patients.DoesNotExist:
            # TODO: add in error message here
            return redirect('/patients/')
