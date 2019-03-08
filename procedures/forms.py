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
