from django.shortcuts import render, redirect
from roadmaps.forms import RoadmapForm, RoadmapProcedureLinkForm
from roadmaps.models import Roadmap, RoadmapProcedureLink


def roadmaps_index(request):
    if request.method == 'POST':
        # Handle searching for roadmaps
        return redirect('/roadmaps/')
    if request.method == 'GET':
        breadcrumbs = [('#', 'Roadmaps')]
        return render(request, 'roadmaps_main.html',
                      {'roadmaps': Roadmap.objects.all(), 'title': 'Roadmaps', 'breadcrumbs': breadcrumbs})


def create_roadmap(request):
    if request.method == "POST":
        form = RoadmapForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            roadmap = Roadmap(roadmap_name=cd['roadmap_name'])
            roadmap.save()
            return redirect('/roadmaps/')
        else:
            breadcrumbs = [('/roadmaps/', 'Roadmaps'), ('#', 'Create Roadmap')]
            return render(request, "create_roadmap.html",
                          {'form': RoadmapForm(), 'title': 'Create Roadmap', 'failed_creation': True,
                           'breadcrumbs': breadcrumbs}, status=401)
    if request.method == "GET":
        breadcrumbs = [('/roadmaps/', 'Roadmaps'), ('#', 'Create Roadmap')]
        return render(request, "create_roadmap.html",
                      {'form': RoadmapForm(), 'title': 'Create Roadmap', 'breadcrumbs': breadcrumbs})


def view_roadmap(request):
    # User wants to update the roadmap currently being viewed
    if request.method == 'POST':
        try:
            # Get the roadmap and place its id into the session
            roadmap = Roadmap.objects.get(id=request.GET.get('id'))
            roadmap_pairs = RoadmapProcedureLink.get_procedures_from_roadmap(roadmap)
            request.session['roadmap_id'] = request.GET.get('id')
            breadcrumbs = [('/roadmaps/', 'Roadmaps'),
                           ('/roadmaps/view_roadmap/?id=' + request.GET.get('id'), roadmap.roadmap_name),
                           ('#', 'Modifying: ' + roadmap.roadmap_name)]
            return render(request, 'modify_roadmap.html',
{'form': RoadmapProcedureLinkForm(), 'roadmap_pairs': roadmap_pairs, 'roadmap': roadmap,
                           'title': 'Modifying: ' + roadmap.roadmap_name, 'breadcrumbs': breadcrumbs})
        except Roadmap.DoesNotExist:
            return redirect('/roadmaps/')

    if request.method == 'GET':
        try:
            roadmap = Roadmap.objects.get(id=request.GET.get('id'))
            roadmap_pairs = RoadmapProcedureLink.get_procedures_from_roadmap(roadmap)
            seperated_by_phase = RoadmapProcedureLink.seperate_by_phase(roadmap_pairs)

            breadcrumbs = [('/roadmaps/', 'Roadmaps'), ('#', roadmap.roadmap_name)]
            return render(request, 'view_roadmap.html',
                          {'roadmap': roadmap, 'title': 'View: ' + roadmap.roadmap_name,
                           'seperated_by_phase': seperated_by_phase, 'breadcrumbs': breadcrumbs})
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
                # If the item doesn't exist, add it
                if not RoadmapProcedureLink.objects.filter(roadmap=roadmap_id, procedure=procedure_item.id,
                                                           phase=cd['phase']):
                    RoadmapProcedureLink.link_procedure_to_roadmap(procedure_item.id, roadmap_id, cd['phase'])
            try:
                roadmap = Roadmap.objects.get(id=roadmap_id)
                roadmap_pairs = RoadmapProcedureLink.get_procedures_from_roadmap(roadmap)
                breadcrumbs = [('/roadmaps/', 'Roadmaps'),
                              ('/roadmaps/view_roadmap/?id=' + roadmap_id, roadmap.roadmap_name),
                              ('#', 'Modifying: ' + roadmap.roadmap_name)]
                return render(request, 'modify_roadmap.html',
                              {'form': RoadmapProcedureLinkForm(), 'roadmap_pairs': roadmap_pairs, 'roadmap': roadmap,
                               'title': 'Modifying: ' + roadmap.roadmap_name, 'breadcrumbs': breadcrumbs})
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
            breadcrumbs = [('/roadmaps/', 'Roadmaps'),
                          ('/roadmaps/view_roadmap/?id=' + roadmap_id, roadmap.roadmap_name),
                          ('#', 'Modifying: ' + roadmap.roadmap_name)]
            return render(request, 'modify_roadmap.html',
                          {'form': RoadmapProcedureLinkForm(), 'roadmap_pairs': roadmap_pairs, 'roadmap': roadmap,
                           'title': 'Modifying: ' + roadmap.roadmap_name})
        except Roadmap.DoesNotExist:
            return redirect('/roadmaps')


def delete_roadmap(request):
    if request.method == 'POST':
        roadmap_id = request.session['roadmap_id']
        try:
            roadmap = Roadmap.objects.get(id=roadmap_id)
            RoadmapProcedureLink.remove_all_pairs_from_roadmap(roadmap_id)
            roadmap.delete()
        except Roadmap.DoesNotExist:
            return redirect('/homepage')
        return redirect('/roadmaps')
