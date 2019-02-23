from django import forms

class ProceduresTemplate(forms.Form):

    procedure_name = forms.CharField(
        label='Procedure Name',
        max_length = 100,
        widget= forms.TextInput(
            attrs={
                'class': 'procedures-group',
                'id': 'procedureName',
                'placeholder': 'Enter Procedure Name'
            }
        )
    )

    procedure_date = forms.DateField(
        label= 'Procedure Date',
        required=False,
        widget= forms.DateInput(
            attrs={
                'class': 'procedures-group',
                'id': 'procedureDate',
            }
        )
    )

    expired_time = forms.DateField(
        label='Expire Date',
        required=False,
        widget=forms.DateInput(
            attrs={
                'class': 'procedures-group',
                'id': 'expirationDate',
            }
        )
    )

    notes = forms.CharField(
        label= 'Notes',
        required=False,
        widget= forms.Textarea(
            attrs={
                'class': 'procedures-group',
                'id': 'notes',
            }
        )
    )
