from django.shortcuts import render
from patients.forms import NewPatient


def index(request):
    if request.method == 'GET':
        return render(request, 'landing_page.html')


def new_patient(request):
    if request.method == 'GET':
        return render(request, 'new_patient.html', {'form': NewPatient()})
