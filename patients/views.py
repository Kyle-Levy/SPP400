from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from patients.forms import NewPatient, SearchPatients
from roadmaps.forms import SelectFromRoadmap
from patients.models import Patients
from assigned_procedures.models import AssignedProcedures
from roadmaps.models import RoadmapProcedureLink
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
            breadcrumbs = [('#', 'Patients')]
            return render(request, 'landing_page.html',
                          {'patients': patients, 'form': SearchPatients(), 'filter': cd['search_terms'],
                           'title': 'Patients', 'breadcrumbs': breadcrumbs})

    if request.method == 'GET':
        breadcrumbs = [('#', 'Patients')]
        return render(request, 'landing_page.html',
                      {'patients': Patients.objects.all(), 'form': SearchPatients(), 'title': 'Patients',
                       'breadcrumbs': breadcrumbs})


'''breadcrumbs = [('/roadmaps/', 'Roadmaps'),
                          ('/roadmaps/view_roadmap/?id=' + roadmap_id, roadmap.roadmap_name),
                          ('#', 'Modifying: ' + roadmap.roadmap_name)]'''


@login_required
def new_patient(request):
    if request.method == 'GET':
        breadcrumbs = [('/patients/', 'Patients'), ('#', 'New Patient')]
        return render(request, 'new_patient.html',
                      {'form': NewPatient(), 'title': 'New Patient', 'breadcrumbs': breadcrumbs})
    if request.method == 'POST':
        form = NewPatient(request.POST)
        if form.is_valid():
            # Clean form data and check that the username password pair is valid
            cd = form.cleaned_data
            patient = Patients.create_patient(cd['first_name'], cd['last_name'], cd['birth_date'], cd['record_number'], cd['referring_physician'], cd['date_of_referral'])
            patient.save()
            return redirect('/homepage/')
        else:
            breadcrumbs = [('/patients/', 'Patients'), ('#', 'New Patient')]
            return render(request, 'new_patient.html',
                          {'form': NewPatient(), 'failed_creation': True, 'title': 'New Patient',
                           'breadcrumbs': breadcrumbs}, status=401)


@login_required
def profile(request):
    if request.method == 'POST':
        try:
            # Get desired patient id from url
            patient = Patients.objects.get(id=request.GET.get('id'))
            request.session['patient_id'] = patient.id

            breadcrumbs = [('/patients/', 'Patients'),
                           ('/patients/profile/?id=' + str(patient.id), patient.last_name + ', ' + patient.first_name),
                           ('#', 'Update: ' + patient.last_name + ', ' + patient.first_name)]
            return render(request, 'update_patient.html', {'form': NewPatient(
                initial={'first_name': patient.first_name, 'last_name': patient.last_name,
                         'record_number': patient.record_number,
                         'birth_date': patient.bday, 'referring_physician': patient.referring_physician, 'date_of_referral': patient.date_of_referral}), 'patient': patient,
                'title': 'Update: ' + patient.last_name + ', ' + patient.first_name, 'breadcrumbs': breadcrumbs})
          
        except Patients.DoesNotExist:
            # TODO: add in error message here
            return redirect('/patients/')

    if request.method == 'GET':
        try:
            # Get desired patient id from url
            patient = Patients.objects.get(id=request.GET.get('id'))
            breadcrumbs = [('/patients/', 'Patients'),
                           ('#', patient.last_name + ', ' + patient.first_name)]
            roadmap_pairs = AssignedProcedures.get_all_procedures(patient)


            all_assigned_procedures = RoadmapProcedureLink.seperate_by_phase(roadmap_pairs)


            return render(request, 'patient.html',
                          {"patient": patient, 'title': 'Profile: ' + patient.last_name + ', ' + patient.first_name,
                           'breadcrumbs': breadcrumbs, 'assigned_procedures': all_assigned_procedures})
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
                breadcrumbs = [('/patients/', 'Patients'),
                               ('/patients/profile/?id=' + str(patient.id),
                                patient.last_name + ', ' + patient.first_name),
                               ('#', 'Update: ' + patient.last_name + ', ' + patient.first_name)]
                return render(request, 'patient.html', {"patient": patient,
                                                        'title': 'Profile: ' + patient.last_name + ', ' + patient.first_name,
                                                        'failed_update': True, 'breadcrumbs': breadcrumbs}, status=401)
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


@login_required
def procedures(request):
    if request.method == 'GET':
        try:
            # Get desired patient id from url
            patient = Patients.objects.get(id=request.GET.get('id'))
            request.session['patient_id'] = patient.id
            roadmap_pairs = AssignedProcedures.get_all_procedures(patient)
            breadcrumbs = [('/patients/', 'Patients'),
                           ('/patients/profile/?id=' + str(patient.id), patient.last_name + ', ' + patient.first_name),
                           ('#', patient.first_name + " " + patient.last_name + "'s  Procedures")]
            return render(request, 'patient_procedures.html', {'form': SelectFromRoadmap(), 'breadcrumbs': breadcrumbs,
                                                               'title': patient.first_name + " " + patient.last_name + "'s  Procedures",
                                                               'roadmap_pairs': roadmap_pairs})
        except Patients.DoesNotExist:
            # TODO: add in error message here
            return redirect('/patients/')

@login_required
def add_roadmap(request):
    if request.method == 'POST':
        try:
            patient = Patients.objects.get(id=request.session['patient_id'])

            form = SelectFromRoadmap(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                roadmap = cd['roadmap']
                AssignedProcedures.add_roadmap_to_patient(roadmap, patient)
                return redirect('/patients/profile/?id=' + str(patient.id))
            else:
                return redirect('/homepage/')
        except Patients.DoesNotExist:
            return redirect('/patients/')

@login_required
def add_procedure(request):
    return redirect('/homepage/')


@login_required
def remove_pairs_from_patient(request):
    if request.method == 'POST':
        checked_boxes = request.POST.getlist('selection[]')
        try:
            patient = Patients.objects.get(id=request.session['patient_id'])
            for pair in checked_boxes:
                cleaned_pair = tuple(pair.split(','))
                AssignedProcedures.remove_assigned_procedure(patient, cleaned_pair[0],
                                                             cleaned_pair[1])
            return redirect('/patients/profile/?id=' + str(patient.id))
        except Patients.DoesNotExist:
            return redirect('/patients/')
