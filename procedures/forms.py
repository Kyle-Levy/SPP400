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

    expired_time = forms.DateField(
        label= 'Expire Date',
        widget= forms.DateInput(
            attrs={
                'class': 'procedures-group',
                'id': 'expirationDate',
            }
        )
    )

    procedure_date = forms.DateField(
        label= 'Procedure Date',
        widget= forms.DateInput(
            attrs={
                'class': 'procedures-group',
                'id': 'procedureDate',
            }
        )
    )

    notes = forms.CharField(
        label= 'Notes',
        widget= forms.Textarea(
            attrs={
                'class': 'procedures-group',
                'id': 'notes',
            }
        )
    )
