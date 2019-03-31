from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from patients.forms import NewPatient, SearchPatients
from patients.models import Patients
import re


@login_required
def index(request):
    if request.method == 'POST':
        form = SearchPatients(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            search = cd['search_terms']
            patients = []
            for patient in Patients.objects.all():
                if search.lower() in patient.first_name.lower() or search.lower() in patient.last_name.lower() or search.lower() in patient.record_number.lower() or patient.first_name.lower() in search.lower() or patient.last_name.lower() in search.lower() or patient.record_number.lower() in search.lower():
                    patients.append(patient)
            return render(request, 'landing_page.html',
                          {'patients': patients, 'form': SearchPatients(), 'filter': cd['search_terms'],
                           'title': 'Patients'})

    if request.method == 'GET':
        return render(request, 'landing_page.html',
                      {'patients': Patients.objects.all(), 'form': SearchPatients(), 'title': 'Patients'})


@login_required
def new_patient(request):
    if request.method == 'GET':
        return render(request, 'new_patient.html', {'form': NewPatient(), 'title': 'New Patient'})
    if request.method == 'POST':
        form = NewPatient(request.POST)
        if form.is_valid():
            # Clean form data and check that the username password pair is valid
            cd = form.cleaned_data
            patient = Patients.create_patient(cd['first_name'], cd['last_name'], cd['birth_date'], cd['record_number'], cd['referring_physician'], cd['referral_date'])
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
            return render(request, 'update_patient.html', {'form': NewPatient(
                initial={'first_name': patient.first_name, 'last_name': patient.last_name,
                         'record_number': patient.record_number,
                         'birth_date': patient.bday}), 'patient': patient,
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
        try:
            patient = Patients.objects.get(id=request.session['patient_id'])
            if form.is_valid():
                # Clean form data and check that the username password pair is valid
                cd = form.cleaned_data
                # Get desired patient id from url
                patient.first_name = cd['first_name']
                patient.last_name = cd['last_name']
                patient.record_number = cd['record_number']
                patient.bday = cd['birth_date']
                patient.referring_physician = cd['referring_physician']
                patient.date_of_referral = cd['date_of_referral']
                patient.save()
                return redirect("/patients/profile/?id=" + str(patient.id))
            else:
                return render(request, 'patient.html', {"patient": patient,
                                                        'title': 'Profile: ' + patient.last_name + ', ' + patient.first_name,
                                                        'failed_update': True}, status=401)
        except Patients.DoesNotExist:
            # TODO: add in error message here
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
