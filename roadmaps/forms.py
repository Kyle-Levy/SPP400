from django import forms
from django.forms import ModelForm
from roadmaps.models import RoadmapProcedureLink


class RoadmapForm(forms.Form):
    roadmap_name = forms.CharField(
        label='Roadmap Name',
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'roadmapName',
                'placeholder': "Enter Roadmap Name"
            }
        )
    )

#Going to need to do this to assign classes to these elements
# https://stackoverflow.com/questions/3679431/how-do-i-set-default-widget-attributes-for-a-django-modelform
class RoadmapProcedureLinkForm(ModelForm):
    class Meta:
        model = RoadmapProcedureLink
        fields = ['procedure', 'phase']
