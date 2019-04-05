from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from homepage.forms import VerifyActionForm
from roadmaps.forms import RoadmapForm, RoadmapProcedureLinkForm, RoadmapForm
from roadmaps.models import Roadmap, RoadmapProcedureLink


@login_required
def roadmaps_index(request):
    if request.method == 'POST':
        # Handle searching for roadmaps
        return redirect('/roadmaps/')
    if request.method == 'GET':
        breadcrumbs = [('#', 'Roadmaps')]
        return render(request, 'roadmaps_main.html',
                      {'roadmaps': Roadmap.objects.all(), 'title': 'Roadmaps', 'breadcrumbs': breadcrumbs})


@login_required
def create_roadmap(request):
    if request.method == "POST":
        form = RoadmapForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            roadmap = Roadmap(roadmap_name=cd['roadmap_name'])
            roadmap.add_time_estimate(cd['time'], str(request.POST.get('time_frame')))
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
                      {'form': RoadmapForm(initial={'time_frame': 'days'}), 'title': 'Create Roadmap',
                       'breadcrumbs': breadcrumbs})


# Todo this method used to set the session
@login_required
def view_roadmap(request):
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


@login_required
def modify_roadmap(request):
    # User wants to update the roadmap currently being viewed
    if request.method == 'GET':
        try:
            # Get the roadmap and place its id into the session
            roadmap = Roadmap.objects.get(id=request.GET.get('id'))
            roadmap_pairs = RoadmapProcedureLink.get_procedures_from_roadmap(roadmap)

            breadcrumbs = [('/roadmaps/', 'Roadmaps'),
                           ('/roadmaps/view_roadmap/?id=' + request.GET.get('id'), roadmap.roadmap_name),
                           ('#', 'Modifying: ' + roadmap.roadmap_name)]

            roadmap_initial_details = {'time': roadmap.est_days_to_complete,
                                       'time_frame': 'days',
                                       'roadmap_name': roadmap.roadmap_name}

            return render(request, 'modify_roadmap.html',
                          {'form': RoadmapProcedureLinkForm(), 'roadmap_pairs': roadmap_pairs, 'roadmap': roadmap,
                           'title': 'Modifying: ' + roadmap.roadmap_name, 'breadcrumbs': breadcrumbs,
                           'update_form': RoadmapForm(initial=roadmap_initial_details),
                           'verification_form': VerifyActionForm()})

        except Roadmap.DoesNotExist:
            # TODO ERROR MESSAGE "Roadmap doesn't exist"
            return redirect('/roadmaps/')


# TODO THIS METHOD USED TO USE THE SESSION
@login_required
def add_to_roadmap(request):
    if request.method == 'POST':
        roadmap_id = request.GET.get('id')
        form = RoadmapProcedureLinkForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            for procedure_item in cd['procedure']:
                # If the item doesn't exist, add it
                if not RoadmapProcedureLink.objects.filter(roadmap=roadmap_id, procedure=procedure_item.id,
                                                           phase=cd['phase']):
                    RoadmapProcedureLink.link_procedure_to_roadmap(procedure_item.id, roadmap_id, cd['phase'])
            return redirect('/roadmaps/view_roadmap/modify/?id=' + str(roadmap_id))
        else:
            #TODO ERROR MESSAGE Invalid Form Submitted
            return redirect('/roadmaps/view_roadmap/modify/?id=' + str(roadmap_id))


# TODO THIS METHOD USED TO USE THE SESSION

@login_required
def remove_selected_pairs(request):
    if request.method == 'POST':
        checked_boxes = request.POST.getlist('selection[]')
        roadmap_id = request.GET.get('id')

        for pair in checked_boxes:
            cleaned_pair = tuple(pair.split(','))
            RoadmapProcedureLink.remove_pair_from_roadmap(roadmap_id, cleaned_pair[0],
                                                          cleaned_pair[1])

        return redirect('/roadmaps/view_roadmap/modify/?id=' + str(roadmap_id))




# TODO THIS METHOD USED TO USE THE SESSION

@login_required
def delete_roadmap(request):
    if request.method == 'POST':
        form = VerifyActionForm(request.POST)
        try:
            roadmap_id = request.GET.get('id')
            print(roadmap_id)
            roadmap = Roadmap.objects.get(id=roadmap_id)
            current_username = request.user.username

            #Text exists in the password box
            if form.is_valid():
                cd = form.cleaned_data
                user = authenticate(username=current_username, password=cd['password'])
                #Password matches
                if user is not None:
                    RoadmapProcedureLink.remove_all_pairs_from_roadmap(roadmap_id)
                    roadmap.delete()
                    return redirect('/roadmaps/')
                #Password doesn't match
                else:
                    #TODO ERROR MESSAGE Wrong Password
                    return redirect('/roadmaps/view_roadmap/modify/?id=' + str(roadmap_id))
            else:

                #TODO Error message INVALID FORM
                return redirect('/roadmaps/view_roadmap/modify/?id=' + str(roadmap_id))
        except Roadmap.DoesNotExist:
            #TODO The roadmap you tried to reach doesn't exist
            return redirect('/roadmaps/')


# TODO THIS METHOD USED TO USE THE SESSION
@login_required
def update_roadmap(request):
    if request.method == 'POST':
        roadmap_id = request.GET.get('id')
        form = RoadmapForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            try:
                roadmap = Roadmap.objects.get(id=roadmap_id)
                roadmap.roadmap_name = cd['roadmap_name']
                roadmap.add_time_estimate(cd['time'], str(request.POST.get('time_frame')))
                roadmap.save()
                return redirect('/roadmaps/view_roadmap/modify/?id=' + str(roadmap_id))
            except Roadmap.DoesNotExist:
                # TODO The roadmap you tried to reach doesn't exist
                return redirect('/homepage')
        else:
            #TODO Error Message INVALID FORM
            return redirect('/roadmaps/view_roadmap/modify/?id=' + str(roadmap_id))
