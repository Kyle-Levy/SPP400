from django import forms


class SearchPatients(forms.Form):
    search_terms = forms.CharField(
        label='First Name',
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


class NewPatient(forms.Form):
    first_name = forms.CharField(
        label='First Name',
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'firstName',
                'placeholder': "Patient's first name"
            }
        )
    )

    last_name = forms.CharField(
        label='Last Name',
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'lastName',
                'placeholder': "Patient's last name"
            }
        )
    )

    record_number = forms.CharField(
        label='Record Number',
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'recordNumber',
                'placeholder': "Medical record number"
            }
        )
    )

    birth_date = forms.DateField(
        label='Birthday',
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'id': 'birthDate',
                'placeholder': 'MM/DD/YYYY',
            }
        )
    )

    referring_physician = forms.CharField(
        label='Referring Physician',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'referringPhysician',
                'placeholder': 'Referring Physician'
            }
        )
    )

    date_of_referral = forms.DateField(
        label='Date of Referral',
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'id': 'dateOfReferral',
                'placeholder': 'MM/DD/YYYY',
            }
        )
    )


class FlagForm(forms.Form):
    notes = forms.CharField(
        label='Notes',
        required=True,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'id': 'notes',
            }
        )
    )
