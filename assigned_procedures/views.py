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

            breadcrumbs = [('/procedures/', 'Procedures'),
                           ('#', 'View: ' + procedure.procedure_name)]

            return render(request, 'view_procedure.html',
                          {'procedure': procedure, 'title': 'View: ' + procedure.procedure_name,
                           'breadcrumbs': breadcrumbs})
        except AssignedProcedures.DoesNotExist:
            messages.warning(request, "The procedure you tried to reach doesn't exist!")
            return redirect('/procedures/')



        breadcrumbs = [('#', 'Assigned')]
        return render(request, 'assigned_procedure.html',
                      {'patients': None, 'form': AssignedProcedureForm(),
                       'title': 'Assigned', 'breadcrumbs': breadcrumbs})
    if request.method == 'POST':
        1+1
