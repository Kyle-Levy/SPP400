from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from homepage.forms import VerifyActionForm
from assigned_procedures.forms import AssignedProcedureForm

from assigned_procedures.models import AssignedProcedures
from django.contrib import messages
import collections
# Create your views here.

@login_required
def update(request):
    if request.method == 'GET':
        try:
            # Get desired id from url
            procedure = AssignedProcedures.objects.get(id=request.GET.get('id'))
            # Build form
            form = AssignedProcedureForm(initial={'assigned_date': procedure.created_at, 'scheduled': procedure.scheduled, 'completed': procedure.completed, 'notes': procedure.notes})
            form.initial['scheduled_date'] = procedure.date_scheduled
            form.initial['completed_date'] = procedure.date_completed

            patient = None
            name = ""
            proc_name = ""
            for pat in procedure.patient.all():
                name = pat.first_name + " " + pat.last_name
                patient = pat
            for proc in procedure.procedure.all():
                proc_name = proc.procedure_name

            breadcrumbs = [('#', 'Assigned')]
            return render(request, 'assigned_procedure.html',
                          {'procedure': proc_name, 'form': form, 'patient': name,
                           'title': 'Assigned', 'breadcrumbs': breadcrumbs})

        except AssignedProcedures.DoesNotExist:
            messages.warning(request, "The procedure you tried to reach doesn't exist!")
            return redirect('/patients/')

    if request.method == 'POST':
        form = AssignedProcedureForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            try:
                # Get desired id from url
                procedure = AssignedProcedures.objects.get(id=request.GET.get('id'))
                procedure.created_at = cd['assigned_date']
                procedure.date_scheduled = cd['scheduled_date']
                procedure.scheduled = cd['scheduled']
                procedure.date_completed = cd['completed_date']
                procedure.completed = cd['completed']
                procedure.notes = cd['notes']
                procedure.save()
            except AssignedProcedures.DoesNotExist:
                messages.warning(request, "The procedure you tried to reach doesn't exist!")
                return redirect('/patients/')

            form = AssignedProcedureForm(initial={'assigned_date': procedure.created_at, 'scheduled': procedure.scheduled, 'completed': procedure.completed, 'notes': procedure.notes})
            form.initial['scheduled_date'] = procedure.date_scheduled
            form.initial['completed_date'] = procedure.date_completed

            breadcrumbs = [('#', 'Assigned')]

            return render(request, 'assigned_procedure.html',
                          {'procedure': procedure, 'form': form,
                           'title': 'Assigned', 'breadcrumbs': breadcrumbs})
        else:
            messages.error(request, 'Invalid Form!')
            return redirect('/assigned/?id=1/')


