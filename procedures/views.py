from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from homepage.forms import VerifyActionForm
from procedures.forms import NewProcedure, SearchProcedures
from procedures.models import Procedure

'''
breadcrumbs = [('/patients/', 'Patients'),
                               ('/patients/profile/?id=' + str(patient.id), patient.last_name + ', ' + patient.first_name),
                               ('#', 'Update: ' + patient.last_name + ', ' + patient.first_name)]
                               
, 'breadcrumbs': breadcrumbs
'''


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
            #TODO Error creating procedure message here
            return redirect('/procedures/create/')



@login_required
def view_procedure(request):
    if request.method == 'GET':
        try:
            # Get desired patient id from url
            procedure = Procedure.objects.get(id=request.GET.get('id'))
            breadcrumbs = [('/procedures/', 'Procedures'),
                           ('#', 'View: ' + procedure.procedure_name)]

            return render(request, 'view_procedure.html',
                          {'procedure': procedure, 'title': 'View: ' + procedure.procedure_name,
                           'breadcrumbs': breadcrumbs})
        except Procedure.DoesNotExist:
            # TODO: add in error message here "Procedure you attempted to reach doesn't exist
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
                'verification-form': VerifyActionForm()})
        except Procedure.DoesNotExist:
            # TODO: add in error message here "Procedure you attempted to reach doesn't exist
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
                # TODO: Error filling out form message
                return redirect('/procedures/view_procedure/update/?id=' + str(procedure.id))
        except Procedure.DoesNotExist:
            # TODO: add in error message here
            return redirect('/procedures/')


@login_required
def delete_this_procedure(request):
    if request.method == 'POST':
        try:
            # Get desired patient id from url
            procedure = Procedure.objects.get(id=request.GET.get('id'))
            procedure.delete()
            return redirect("/procedures/")
        except Procedure.DoesNotExist:
            # TODO: add in error message here
            return redirect('/procedures/')
