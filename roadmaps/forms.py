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
    procedure_phase_pairs = forms.MultipleChoiceField(required=True, widget=forms.SelectMultiple(attrs={
        'id': 'procedurePairs'
    }))


class RoadmapProcedureLinkForm(forms.Form):
    procedures = forms.MultipleChoiceField(
        required=True,
        widget=forms.SelectMultiple(attrs={
            'id': 'procedures'
        })
    )
    phases = forms.ChoiceField(
        required=True,
        widget=forms.Select(attrs={
            'id': 'phases'
        })
    )
    roadmaps = forms.ChoiceField(
        required=True,
        widget=forms.Select(attrs={
            'id': 'roadmaps'
        })
    )
