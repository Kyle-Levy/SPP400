from django.shortcuts import render
from procedures.forms import NewProcedure
from procedures.models import Procedures
from django.http import HttpResponse


def index(request):
    if request.method == 'POST':
        form = NewProcedure(request.POST)
        if form.is_valid():
            return render(request, 'new_procedure.html', {'form': NewProcedure()})
    else:
        form = NewProcedure()
        return render(request, 'new_procedure.html', {'form': NewProcedure()})


def new_procedure(request):
    if request.method == 'POST':
        form = NewProcedure(request.post)

