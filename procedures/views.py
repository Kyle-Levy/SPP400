from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from procedures.forms import NewProcedure, SearchProcedures
from procedures.models import Procedure
from django.http import HttpResponse


@login_required
def index(request):
    if request.method == 'POST':
        form = SearchProcedures(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            search = cd['search_terms']
            procedures = []
            for procedure in Procedure.objects.all():
                if search in procedure.procedure_name or procedure.procedure_name in search:
                    procedures.append(procedure)
            return render(request, 'procedure_main.html', {'procedures': procedures, 'form': SearchProcedures(), 'filter': cd['search_terms'], 'title': 'Procedures'})

    if request.method == 'GET':
        return render(request, 'procedure_main.html', {'procedures': Procedure.objects.all(), 'form': SearchProcedures(), 'title': 'Procedures'})


@login_required
def new_procedure(request):
    if request.method == 'POST':
        form = NewProcedure(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            procedure = Procedure(procedure_name=cd['procedure_name'], procedure_info=cd['notes'])
            procedure.save()
            return redirect('/procedures/')
        else:
            return render(request, 'new_procedure.html',
                          {'form': NewProcedure(), 'failed_creation': True, 'title': 'New Procedure'}, status=401)
    else:
        return render(request, 'new_procedure.html', {'form': NewProcedure(), 'title': 'New Procedure'})


@login_required
def view_procedure(request):
    if request.method == 'POST':
        try:
            # Get desired procedure id from url and store into session for when page is updated
            procedure = Procedure.objects.get(id=request.GET.get('id'))
            request.session['procedure_id'] = request.GET.get('id')
            return render(request, 'update_procedure.html', {'form': NewProcedure(
                initial={'procedure_name': procedure.procedure_name, 'notes': procedure.procedure_info}),
                'procedure': procedure, 'title': 'Update: ' + procedure.procedure_name})
        except Procedure.DoesNotExist:
            return redirect('/procedures/')

    if request.method == 'GET':
        try:
            # Get desired patient id from url
            procedure = Procedure.objects.get(id=request.GET.get('id'))
            return render(request, 'view_procedure.html',
                          {'procedure': procedure, 'title': 'View: ' + procedure.procedure_name})
        except Procedure.DoesNotExist:
            # TODO: add in error message here
            return redirect('/procedures/')


@login_required
def update_procedure(request):
    if request.method == 'POST':
        form = NewProcedure(request.POST)
        try:
            procedure = Procedure.objects.get(id=request.session['procedure_id'])
            if form.is_valid():
                # Clean form data and check that the username password pair is valid
                cd = form.cleaned_data
                # Get desired patient id from url
                procedure.procedure_name = cd['procedure_name']
                procedure.procedure_info = cd['notes']
                procedure.save()
                return redirect("/procedures/view_procedure/?id=" + str(procedure.id))
            else:
                return render(request, 'view_procedure.html',
                              {'procedure': procedure, 'title': 'View: ' + procedure.procedure_name,
                               'failed_update': True}, status=401)
        except Procedure.DoesNotExist:
            # TODO: add in error message here
            return redirect('/procedures/')


@login_required
def delete_this_procedure(request):
    if request.method == 'POST':
        try:
            # Get desired patient id from url
            procedure = Procedure.objects.get(id=request.session['procedure_id'])
            procedure.delete()
            return redirect("/procedures/")
        except Procedure.DoesNotExist:
            # TODO: add in error message here
            return redirect('/procedures/')
