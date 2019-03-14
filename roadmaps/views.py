from django.shortcuts import render, redirect
from django import forms
from django.utils import timezone
from roadmaps.forms import RoadmapForm


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

def create_roadmap(request):
    if request.method == "GET":
        form = RoadmapForm()
        return render(request, "create_roadmap.html", {'form':form, 'title' : 'Create Roadmap'})
    if request.method == "POST":
        form = RoadmapForm()
        return render(request, "create_roadmap.html", {'form': form, 'title': 'Create Roadmap'})