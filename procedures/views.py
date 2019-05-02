from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from assigned_procedures.models import AssignedProcedures
from homepage.forms import VerifyActionForm
from procedures.forms import NewProcedure, SearchProcedures
from procedures.models import Procedure
from django.contrib import messages

from roadmaps.models import RoadmapProcedureLink


@login_required
def index(request):
    if request.method == 'POST':
        form = SearchProcedures(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            search = cd['search_terms']
            procedures = []
            for procedure in Procedure.objects.all():
                if search.lower() in procedure.procedure_name.lower() or procedure.procedure_name.lower() in search.lower():
                    procedures.append(procedure)
            breadcrumbs = [('/procedures/', 'Procedures')]
            return render(request, 'procedure_main.html',
                          {'procedures': procedures, 'form': SearchProcedures(), 'filter': cd['search_terms'],
                           'title': 'Procedures', 'breadcrumbs': breadcrumbs})

    if request.method == 'GET':
        breadcrumbs = [('/procedures/', 'Procedures')]
        return render(request, 'procedure_main.html',
                      {'procedures': Procedure.objects.all(), 'form': SearchProcedures(), 'title': 'Procedures',
                       'breadcrumbs': breadcrumbs})


@login_required
def new_procedure(request):
    if request.method == 'GET':
        breadcrumbs = [('/procedures/', 'Procedures'),
                       ('#', 'New Procedure')]

        return render(request, 'new_procedure.html',
                      {'form': NewProcedure(initial={'time_frame': 'days'}), 'title': 'New Procedure',
                       'breadcrumbs': breadcrumbs})

    if request.method == 'POST':
        form = NewProcedure(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            procedure = Procedure(procedure_name=cd['procedure_name'], procedure_info=cd['notes'])
            procedure.add_time_estimate(cd['time'], str(request.POST.get('time_frame')))
            procedure.save()
            return redirect('/procedures/')
        else:
            messages.error(request, 'Invalid Form!')
            return redirect('/procedures/create/')



@login_required
def view_procedure(request):
    if request.method == 'GET':
        try:
            # Get desired patient id from url
            procedure = Procedure.objects.get(id=request.GET.get('id'))
            breadcrumbs = [('/procedures/', 'Procedures'),
                           ('#', 'View: ' + procedure.procedure_name)]

            assigned_procedures_query = AssignedProcedures.objects.filter(procedure=procedure)
            all_patients = set([])
            for single_assignment in assigned_procedures_query:
                all_patients.add(single_assignment.patient.all()[0])

            return render(request, 'view_procedure.html',
                          {'procedure': procedure, 'title': 'View: ' + procedure.procedure_name,
                           'breadcrumbs': breadcrumbs, 'all_patients': all_patients, 'number_of_patients': len(all_patients)})
        except Procedure.DoesNotExist:
            messages.warning(request, "The procedure you tried to reach doesn't exist!")
            return redirect('/procedures/')


@login_required
def update_procedure(request):
    if request.method == 'GET':
        try:
            # Get desired procedure id from url and store into session for when page is updated
            procedure = Procedure.objects.get(id=request.GET.get('id'))
            
            breadcrumbs = [('/procedures/', 'Procedures'),
                           ('/procedures/view_procedure/?id=' + str(procedure.id), 'View: ' + procedure.procedure_name),
                           ('#', 'Update: ' + procedure.procedure_name)]
            
            initial_form_data = {'procedure_name': procedure.procedure_name, 'notes': procedure.procedure_info,
                         'time_frame': 'days', 'time': procedure.est_days_to_complete}
            
            return render(request, 'update_procedure.html', {'form': NewProcedure(initial= initial_form_data),
                'procedure': procedure,
                'title': 'Update: ' + procedure.procedure_name,
                'breadcrumbs': breadcrumbs,
                'verification_form': VerifyActionForm()})
        except Procedure.DoesNotExist:
            messages.warning(request, "The procedure you tried to reach doesn't exist!")
            return redirect('/procedures/')

    if request.method == 'POST':
        form = NewProcedure(request.POST)
        try:
            procedure = Procedure.objects.get(id=request.GET.get('id'))
            if form.is_valid():
                # Clean form data and check that the username password pair is valid
                cd = form.cleaned_data
                # Get desired patient id from url
                procedure.procedure_name = cd['procedure_name']
                procedure.procedure_info = cd['notes']
                procedure.add_time_estimate(cd['time'], str(request.POST.get('time_frame')))
                procedure.save()
                return redirect("/procedures/view_procedure/?id=" + str(procedure.id))

            else:
                messages.error(request, 'Invalid Form!')
                return redirect('/procedures/view_procedure/update/?id=' + str(procedure.id))
        except Procedure.DoesNotExist:
            messages.warning(request, "The procedure you tried to reach doesn't exist!")
            return redirect('/procedures/')


@login_required
def delete_this_procedure(request):
    if request.method == 'POST':
        form = VerifyActionForm(request.POST)
        try:
            procedure = Procedure.objects.get(id=request.GET.get('id'))
            # Get desired patient id from url
            if form.is_valid():
                cd = form.cleaned_data
                if procedure.procedure_name == cd['item_name']:
                    procedure_assignments = AssignedProcedures.objects.filter(procedure=procedure)

                    for assignment in procedure_assignments:
                        assignment.delete()

                    procedure_roadmap_links = RoadmapProcedureLink.objects.filter(procedure=procedure)

                    for link in procedure_roadmap_links:
                        link.delete()

                    procedure.delete()
                    return redirect('/procedures/')
                else:
                    messages.error(request, 'Incorrect procedure name!')
                    return redirect('procedures/view_procedure/update/?id=' + str(procedure.id))
            else:
                messages.error(request, 'Invalid Form!')
                return redirect('procedures/view_procedure/update/?id=' + str(procedure.id))

        except Procedure.DoesNotExist:
            messages.warning(request, "The procedure you tried to reach doesn't exist!")
            return redirect('/procedures/')
