from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from homepage.forms import VerifyActionForm
from assigned_procedures.forms import AssignedProcedureForm
from assigned_procedures.models import AssignedProcedures
from django.contrib import messages

# Create your views here.

@login_required
def update(request):
    if request.method == 'GET':
        try:
            # Get desired id from url
            procedure = AssignedProcedures.objects.get(id=request.GET.get('id'))
            id = procedure.id
            # Build form
            form = AssignedProcedureForm(initial={'assigned_date': procedure.created_at, 'scheduled': procedure.scheduled,'notes': procedure.notes})
            form.initial['scheduled_date'] = procedure.date_scheduled
            form.initial['completed_date'] = procedure.date_completed
            form.initial['completion_goal'] = procedure.est_date_complete

            patient = None
            name = ""
            proc_name = ""
            for pat in procedure.patient.all():
                name = pat.first_name + " " + pat.last_name
                patient = pat
            for proc in procedure.procedure.all():
                proc_name = proc.procedure_name


            breadcrumbs = [("/patients/profile/?id=" + str(patient.id), name),('#', proc_name)]
            return render(request, 'assigned_procedure.html',
                          {'procedure': proc_name, 'form': form, 'patient': name, 'id': id, 'phase': procedure.phaseNumber,
                           'title': 'Assigned', 'breadcrumbs': breadcrumbs, 'completed': procedure.completed})

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
                procedure.notes = cd['notes']
                procedure.est_date_complete = cd['completion_goal']
                procedure.save()

                patient = None
                for pat in procedure.patient.all():
                    patient = pat
                return redirect("/patients/profile/?id=" + str(patient.id))
            except AssignedProcedures.DoesNotExist:
                messages.warning(request, "The procedure you tried to reach doesn't exist!")
                return redirect('/patients/')
        else:
            messages.error(request, 'Invalid Form!')
            return redirect('/assigned/procedure/?id=' + str(request.GET.get('id')))


