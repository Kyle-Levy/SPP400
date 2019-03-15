from django.shortcuts import render, redirect
from django import forms
from django.utils import timezone
from roadmaps.forms import RoadmapForm
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
        #Handle searching for roadmaps
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
