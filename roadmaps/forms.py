from django import forms
from django.forms import ModelForm
from roadmaps.models import RoadmapProcedureLink, Roadmap


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


# Followed this to assign classes to these elements
# https://stackoverflow.com/questions/3679431/how-do-i-set-default-widget-attributes-for-a-django-modelform
class RoadmapProcedureLinkForm(ModelForm):
    # Add classes to the fields on initialization of the form
    def __init__(self, *args, **kwargs):
        super(RoadmapProcedureLinkForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if 'class' in field.widget.attrs:
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = RoadmapProcedureLink
        fields = ['procedure', 'phase']


class SelectFromRoadmap(forms.Form):
    roadmap = forms.ModelChoiceField(queryset=Roadmap.objects.all(),
                                     label='Roadmaps',
                                     widget=forms.Select(
                                         attrs={
                                             'class': 'form-control'
                                         }
                                     ))


class UpdateRoadmapInfo(forms.Form):
    roadmap_name = forms.CharField(
        label='Roadmap Name',
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'roadmapName',
                'placeholder': 'Enter Roadmap Name'
            }
        )
    )

    time = forms.CharField(
        label='Projected Timeline',
        max_length=10,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'procedureName',
                'placeholder': 'Enter Projected Completion Time'
            }
        )
    )

    CHOICES = [('days', 'Days'),
               ('weeks', 'Weeks')]

    time_frame = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
