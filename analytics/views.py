from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from homepage.forms import VerifyActionForm
from django.contrib import messages

@login_required
def index(request):
    if request.method == 'GET':
        breadcrumbs = [('/analytics/', 'Analytics')]
        return render(request, 'analytics_main.html', {'title': 'Analytics', 'breadcrumbs': breadcrumbs})
