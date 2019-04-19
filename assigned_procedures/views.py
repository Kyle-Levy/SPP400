from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from homepage.forms import VerifyActionForm
from patients.forms import NewPatient, SearchPatients, FlagForm
from procedures.models import Procedure
from roadmaps.forms import SelectFromRoadmap, RoadmapProcedureLinkForm
from patients.models import Patients
from assigned_procedures.models import AssignedProcedures
from roadmaps.models import RoadmapProcedureLink
from django.contrib import messages
import collections
# Create your views here.

@login_required
def update(request):
    if request.method == 'GET':
        breadcrumbs = [('#', 'Assigned')]
        return render(request, 'assigned_procedure.html',
                      {'patients': None, 'form': SearchPatients(), 'filter': None,
                       'title': 'Patients', 'breadcrumbs': breadcrumbs})
    if request.method == 'POST':
        1+1
