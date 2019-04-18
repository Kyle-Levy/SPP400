from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from homepage.forms import VerifyActionForm
from django.contrib import messages
from assigned_procedures.models import AssignedProcedures
from procedures.models import Procedure
from analytics.models import Analytics

@login_required
def index(request):
    if request.method == 'GET':
        breadcrumbs = [('/analytics/', 'Analytics')]
        return render(request, 'analytics_main.html', {'title': 'Analytics', 'breadcrumbs': breadcrumbs, 'procedures': Procedure.objects.all(), 'percent_behind': Analytics.calculate_behind_procedure_prec()})
