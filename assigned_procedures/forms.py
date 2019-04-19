from django import forms


class AssignedProcedureForm(forms.Form):
    assigned_date = forms.DateField(
        label='Assigned Date',
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'id': 'assignedDate',
                'placeholder': 'YYYY-MM-DD',
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
                'placeholder': 'YYYY-MM-DD',
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
                'placeholder': 'YYYY-MM-DD',
            }
        )
    )

    completion_goal = forms.DateField(
        label='Completion Goal',
        required=False,
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'id': 'completionGoal',
                'placeholder': 'YYYY-MM-DD',
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

