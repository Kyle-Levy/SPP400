from django.shortcuts import render, redirect
from django import forms
from django.utils import timezone
from roadmaps.forms import RoadmapForm, RoadmapProcedureLinkForm
from roadmaps.models import Roadmap


def add_model(request):
    if request.method == "POST":
        form = RoadmapForm(request.POST)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.timestamp = timezone.now()
            model_instance.save()
            return redirect('/')

    else:
        form = RoadmapForm()
        return render(request, "roadmap_template.html", {'form': form})


def index(request):
    if request.method == 'POST':
        # Handle searching for roadmaps
        return redirect('/roadmaps/')
    if request.method == 'GET':
        return render(request, 'roadmaps_main.html', {'roadmaps': Roadmap.objects.all(), 'title': 'Roadmaps'})


def create_roadmap(request):
    if request.method == "POST":
        form = RoadmapForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            roadmap = Roadmap(roadmap_name=cd['roadmap_name'])
            roadmap.save()
            return redirect('/roadmaps/')
        else:
            return render(request, "create_roadmap.html",
                          {'form': RoadmapForm(), 'title': 'Create Roadmap', 'failed_creation': True})
    if request.method == "GET":
        return render(request, "create_roadmap.html", {'form': RoadmapForm(), 'title': 'Create Roadmap'})


def view_roadmap(request):
    # User wants to update the roadmap currently being viewed
    if request.method == 'POST':
        try:
            # Get the roadmap and place its id into the session
            roadmap = Roadmap.objects.get(id=request.GET.get('id'))
            request.session['roadmap_id'] = request.GET.get('id')
            return render(request, 'modify_roadmap.html', {'form': RoadmapProcedureLinkForm(), 'roadmap': roadmap, 'title':'Modifying: ' + roadmap.roadmap_name})
        except Roadmap.DoesNotExist:
            return redirect('/roadmaps/')

    if request.method == 'GET':
        try:
            roadmap = Roadmap.objects.get(id=request.GET.get('id'))
            return render(request, 'view_roadmap.html', {'roadmap': roadmap, 'title': 'View: ' + roadmap.roadmap_name,})
        except Roadmap.DoesNotExist:
            # Roadmap object doesn't exist
            return redirect('/roadmaps/')

def add_to_roadmap(request):
    if request.method == 'POST':
        form = RoadmapProcedureLinkForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            print(request.session['roadmap_id'])
            print(cd)
            return redirect('/homepage/')