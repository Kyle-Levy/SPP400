from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from homepage.forms import VerifyActionForm
from patients.forms import NewPatient, SearchPatients, FlagForm
from procedures.models import Procedure
from roadmaps.forms import SelectFromRoadmap, RoadmapProcedureLinkForm
from patients.models import Patients
from assigned_procedures.models import AssignedProcedures
from roadmaps.models import RoadmapProcedureLink
from django.contrib import messages
import collections

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
            patient = Patients.create_patient(cd['first_name'], cd['last_name'], cd['birth_date'], cd['record_number'],
                                              cd['referring_physician'], cd['date_of_referral'])
            patient.save()
            return redirect('/patients/')
        else:
            messages.error(request, 'Invalid Form!')
            return redirect('/patients/create/')


# TODO This post currently takes you to the update patient page. Instead, this should be a seperate method that use request.GET
@login_required
def profile(request):
    if request.method == 'GET':
        try:
            # Get desired patient id from url
            patient = Patients.objects.get(id=request.GET.get('id'))
            breadcrumbs = [('/patients/', 'Patients'),
                           ('#', patient.last_name + ', ' + patient.first_name)]
            roadmap_pairs = AssignedProcedures.get_all_procedures(patient)

            all_assigned_procedures = RoadmapProcedureLink.seperate_by_phase(roadmap_pairs)
            ordered = collections.OrderedDict()
            phase_order = sorted(all_assigned_procedures.keys())
            for phase in phase_order:
                ordered[phase] = all_assigned_procedures[phase]
            all_assigned_procedures = ordered
            bool_goals = True
            try:
                goals = all_assigned_procedures[phase_order[-1]]
            except IndexError:
                goals = []
                bool_goals = False
            return render(request, 'patient.html',
                          {"patient": patient, 'title': 'Profile: ' + patient.last_name + ', ' + patient.first_name,
                           'breadcrumbs': breadcrumbs, 'assigned_procedures': all_assigned_procedures,
                           'flag_form': FlagForm(), 'goals': goals, 'bool_goals': bool_goals})
        except Patients.DoesNotExist:
            messages.warning(request, "The patient you tried to reach doesn't exist!")
            return redirect('/patients/')


@login_required
def update(request):
    if request.method == 'GET':
        try:
            # Get desired patient id from url
            patient = Patients.objects.get(id=request.GET.get('id'))

            breadcrumbs = [('/patients/', 'Patients'),
                           ('/patients/profile/?id=' + str(patient.id), patient.last_name + ', ' + patient.first_name),
                           ('#', 'Update: ' + patient.last_name + ', ' + patient.first_name)]

            initial_form_dict = {'first_name': patient.first_name, 'last_name': patient.last_name,
                                 'record_number': patient.record_number,
                                 'birth_date': patient.bday, 'referring_physician': patient.referring_physician,
                                 'date_of_referral': patient.date_of_referral}

            page_title = 'Update: ' + patient.last_name + ', ' + patient.first_name

            return render(request, 'update_patient.html',
                          {'form': NewPatient(initial=initial_form_dict), 'patient': patient, 'title': page_title,
                           'breadcrumbs': breadcrumbs, 'verification_form': VerifyActionForm()})

        except Patients.DoesNotExist:
            messages.warning(request, "The patient you tried to reach doesn't exist!")
            return redirect('/patients/')
    if request.method == 'POST':
        form = NewPatient(request.POST)
        try:
            patient = Patients.objects.get(id=request.GET.get('id'))
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
                messages.error(request, 'Invalid Form!')
                return redirect('/patients/profile/update/?id=' + str(patient.id))
        except Patients.DoesNotExist:
            messages.warning(request, "The patient you tried to reach doesn't exist!")
            return redirect('/patients/')


@login_required
def delete(request):
    if request.method == 'POST':
        form = VerifyActionForm(request.POST)
        try:
            # Get desired patient id from url
            patient = Patients.objects.get(id=request.GET.get('id'))
            if form.is_valid():
                cd = form.cleaned_data
                if patient.record_number == cd['item_name']:
                    patient.delete()
                    return redirect('/patients/')
                else:
                    messages.error(request, 'Incorrect patient MRN!')
                    return redirect('/patients/profile/update/?id=' + str(patient.id))
            else:
                messages.error(request, 'Invalid Form!2')
                return redirect('/patients/profile/update/?id=' + str(patient.id))
        except Patients.DoesNotExist:
            messages.warning(request, "The patient you tried to reach doesn't exist!")
            return redirect('/patients/')


@login_required
def procedures(request):
    if request.method == 'GET':
        try:
            # Get desired patient id from url
            patient = Patients.objects.get(id=request.GET.get('id'))

            roadmap_pairs = AssignedProcedures.get_all_procedures(patient)

            breadcrumbs = [('/patients/', 'Patients'),
                           ('/patients/profile/?id=' + str(patient.id), patient.last_name + ', ' + patient.first_name),
                           ('#', patient.first_name + " " + patient.last_name + "'s  Procedures")]

            page_title = patient.first_name + " " + patient.last_name + "'s  Procedures"

            return render(request, 'patient_procedures.html',
                          {'roadmap_form': SelectFromRoadmap(),
                           'procedure_phase_form': RoadmapProcedureLinkForm(),
                           'patient': patient,
                           'breadcrumbs': breadcrumbs,
                           'title': page_title,
                           'roadmap_pairs': roadmap_pairs})
        except Patients.DoesNotExist:
            messages.warning(request, "The patient you tried to reach doesn't exist!")
            return redirect('/patients/')


# TODO change request.session to getting the id from the url
@login_required
def add_roadmap(request):
    if request.method == 'POST':
        try:
            patient = Patients.objects.get(id=request.GET.get('id'))

            form = SelectFromRoadmap(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                roadmap = cd['roadmap']
                AssignedProcedures.add_roadmap_to_patient(roadmap, patient)
                return redirect('/patients/profile/procedures/?id=' + str(patient.id))
            else:
                messages.error(request, 'Invalid Form!')
                return redirect('/homepage/')
        except Patients.DoesNotExist:
            messages.warning(request, "The patient you tried to reach doesn't exist!")
            return redirect('/patients/')


# TODO change request.session to getting the id from the url
@login_required
def add_procedure(request):
    if request.method == 'POST':
        try:
            patient = Patients.objects.get(id=request.GET.get('id'))

            form = RoadmapProcedureLinkForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                for procedure_item in cd['procedure']:
                    AssignedProcedures.assign_procedure_to_patient(cd['phase'], patient, procedure_item)
                return redirect('/patients/profile/procedures/?id=' + str(patient.id))
            else:
                messages.error(request, 'Invalid Form!')
                return redirect('/homepage/')
        except Patients.DoesNotExist:
            messages.warning(request, "The patient you tried to reach doesn't exist!")
            return redirect('/patients/')


# TODO change request.session to getting the id from the url
@login_required
def remove_pairs_from_patient(request):
    if request.method == 'POST':
        checked_boxes = request.POST.getlist('selection[]')
        try:
            patient = Patients.objects.get(id=request.GET.get('id'))
            if checked_boxes:
                for pair in checked_boxes:
                    cleaned_pair = tuple(pair.split(','))
                    AssignedProcedures.remove_assigned_procedure(patient, cleaned_pair[0],
                                                                 cleaned_pair[1])
                return redirect('/patients/profile/procedures/?id=' + str(patient.id))
            else:
                #TODO Warning saying "You didn't select any items to be removed"
                return redirect('/patients/profile/procedures/?id=' + str(patient.id))
        except Patients.DoesNotExist:
            messages.warning(request, "The patient you tried to reach doesn't exist!")
            return redirect('/patients/')


# TODO change request.session to getting the id from the url
def flag_patient(request):
    if request.method == 'POST':
        try:
            form = FlagForm(request.POST)

            if form.is_valid():
                patient = Patients.objects.get(id=request.GET.get('id'))

                cd = form.cleaned_data

                if not patient.flagged:
                    patient.toggle_flag()
                    patient.patient_flagged_reason = cd['notes']
                    patient.save()

                return redirect('/patients/profile/?id=' + str(patient.id))

            else:
                messages.error(request, 'Invalid Form!')
                return redirect('/patients/')

        except Patients.DoesNotExist:
            messages.warning(request, "The patient you tried to reach doesn't exist!")
            return redirect('/patients/')


def unflag_patient(request):
    if request.method == 'POST':
        try:
            patient = Patients.objects.get(id=request.GET.get('id'))

            patient.patient_flagged_reason = ""
            if patient.flagged:
                patient.toggle_flag()
            patient.save()

            return redirect('/patients/profile/?id=' + str(patient.id))

        except Patients.DoesNotExist:
            messages.warning(request, "The patient you tried to reach doesn't exist!")
            return redirect('/patients/')
