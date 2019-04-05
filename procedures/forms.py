from django import forms


class SearchProcedures(forms.Form):
    search_terms = forms.CharField(
        label='Name',
        required=False,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'searchTerms',
                'placeholder': "Enter search terms"
            }
        )
    )


class NewProcedure(forms.Form):
    procedure_name = forms.CharField(
        label='Procedure Name',
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'procedureName',
                'placeholder': 'Enter Procedure Name'
            }
        )
    )

    notes = forms.CharField(
        label='Notes',
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'id': 'notes',
            }
        )
    )

    time = forms.IntegerField(
        label='Projected Timeline',
        widget=forms.NumberInput(
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
