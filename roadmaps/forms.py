from django.forms import ModelForm
from roadmaps.models import Roadmap


class RoadmapForm(ModelForm):
    class Meta:
        model = Roadmap
        fields = ['roadmap_name', 'procedures', 'phases']
