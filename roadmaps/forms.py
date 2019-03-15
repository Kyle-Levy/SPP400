from django import forms
from roadmaps.models import Roadmap


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


class RoadmapProcedureLinkForm(forms.Form):
    procedures = forms.MultipleChoiceField(
        label='Procedures',
        required=True,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control',
            'id': 'procedures'
        })
    )
    phases = forms.IntegerField(
        label='Phases',
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'id': 'phase_number'
        })
    )
    roadmaps = forms.ChoiceField(
        label='Roadmaps',
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'roadmaps'
        })
    )
