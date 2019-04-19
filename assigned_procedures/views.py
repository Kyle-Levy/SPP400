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

            breadcrumbs = [('#', 'Assigned')]
            return render(request, 'assigned_procedure.html',
                          {'patients': None, 'form': form,
                           'title': 'Assigned', 'breadcrumbs': breadcrumbs})

        except AssignedProcedures.DoesNotExist:
            messages.warning(request, "The procedure you tried to reach doesn't exist!")
            return redirect('/procedures/')

    if request.method == 'POST':
        1+1
