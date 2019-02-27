from django.shortcuts import render, redirect
from procedures.forms import NewProcedure
from procedures.models import Procedures
from django.http import HttpResponse


def index(request):
    if request.method == 'GET':
        return render(request, 'procedure_main.html')


def new_procedure(request):
    if request.method == 'POST':
        form = NewProcedure(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            procedure = Procedures(procedure_name=cd['procedure_name'], procedure_info=cd['notes'])
            procedure.save()
            return redirect('/procedures/')
        else:
            return render(request, 'new_procedure.html', {'form': NewProcedure(), 'failed_creation': True}, status=401)
    else:
        return render(request, 'new_procedure.html', {'form': NewProcedure()})
