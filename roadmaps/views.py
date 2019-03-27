from django.shortcuts import render, redirect
from roadmaps.forms import RoadmapForm, RoadmapProcedureLinkForm
from roadmaps.models import Roadmap, RoadmapProcedureLink


def roadmaps_index(request):
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
                          {'form': RoadmapForm(), 'title': 'Create Roadmap', 'failed_creation': True}, status=401)
    if request.method == "GET":
        return render(request, "create_roadmap.html", {'form': RoadmapForm(), 'title': 'Create Roadmap'})


def view_roadmap(request):
    # User wants to update the roadmap currently being viewed
    if request.method == 'POST':
        try:
            # Get the roadmap and place its id into the session
            roadmap = Roadmap.objects.get(id=request.GET.get('id'))
            roadmap_pairs = RoadmapProcedureLink.get_procedures_from_roadmap(roadmap)
            request.session['roadmap_id'] = request.GET.get('id')
            return render(request, 'modify_roadmap.html',
                          {'form': RoadmapProcedureLinkForm(), 'roadmap_pairs': roadmap_pairs, 'roadmap': roadmap,
                           'title': 'Modifying: ' + roadmap.roadmap_name})
        except Roadmap.DoesNotExist:
            return redirect('/roadmaps/')

    if request.method == 'GET':
        try:
            roadmap = Roadmap.objects.get(id=request.GET.get('id'))
            roadmap_pairs = RoadmapProcedureLink.get_procedures_from_roadmap(roadmap)
            return render(request, 'view_roadmap.html',
                          {'roadmap': roadmap, 'roadmap_pairs': roadmap_pairs,
                           'title': 'View: ' + roadmap.roadmap_name})
        except Roadmap.DoesNotExist:
            # Roadmap object doesn't exist
            return redirect('/roadmaps/')


def add_to_roadmap(request):
    if request.method == 'POST':
        form = RoadmapProcedureLinkForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            roadmap_id = request.session['roadmap_id']
            for procedure_item in cd['procedure']:
                #If the item doesn't exist, add it
                if not RoadmapProcedureLink.objects.filter(roadmap=roadmap_id, procedure=procedure_item.id, phase=cd['phase']):
                    RoadmapProcedureLink.link_procedure_to_roadmap(procedure_item.id, roadmap_id, cd['phase'])
            try:
                roadmap = Roadmap.objects.get(id=roadmap_id)
                roadmap_pairs = RoadmapProcedureLink.get_procedures_from_roadmap(roadmap)
                return render(request, 'modify_roadmap.html',
                              {'form': RoadmapProcedureLinkForm(), 'roadmap_pairs': roadmap_pairs, 'roadmap': roadmap,
                               'title': 'Modifying: ' + roadmap.roadmap_name})
            except Roadmap.DoesNotExist:
                return redirect('/roadmaps')
        else:
            return redirect('/homepage/')


def remove_selected_pairs(request):
    if request.method == 'POST':
        checked_boxes = request.POST.getlist('selection[]')
        roadmap_id = request.session['roadmap_id']

        for pair in checked_boxes:
            cleaned_pair = tuple(pair.split(','))
            RoadmapProcedureLink.remove_pair_from_roadmap(roadmap_id, cleaned_pair[0],
                                                          cleaned_pair[1])
        try:
            roadmap = Roadmap.objects.get(id=roadmap_id)
            roadmap_pairs = RoadmapProcedureLink.get_procedures_from_roadmap(roadmap)
            return render(request, 'modify_roadmap.html',
                          {'form': RoadmapProcedureLinkForm(), 'roadmap_pairs': roadmap_pairs, 'roadmap': roadmap,
                           'title': 'Modifying: ' + roadmap.roadmap_name})
        except Roadmap.DoesNotExist:
            return redirect('/roadmaps')
