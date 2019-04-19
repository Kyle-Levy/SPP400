from django import forms


class AssignedProcedureForm(forms.Form):
    assigned_date = forms.DateField(
        label='Assigned Date',
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'id': 'assignedDate',
                'placeholder': 'MM/DD/YYYY',
            }
        )
    )

    scheduled_date = forms.DateField(
        label='Scheduled Date',
        required=False,
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'id': 'scheduledDate',
                'placeholder': 'MM/DD/YYYY',
            }
        )
    )

    completed_date = forms.DateField(
        label='Date Completed',
        required=False,
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'id': 'completedDate',
                'placeholder': 'MM/DD/YYYY',
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

    CHOICES = [(True, 'Scheduled'), (False, 'Not Scheduled')]
    CHOICES1 = [(True, 'Complete'), (False, 'Incomplete')]

    scheduled = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    completed = forms.ChoiceField(choices=CHOICES1, widget=forms.RadioSelect)

