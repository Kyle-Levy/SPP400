from django import forms


class LoginForm(forms.Form):

    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'loginUsername',
                'placeholder': 'Enter username'
            }
        ))
    password = forms.CharField(widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id': 'loginPassword',
                'placeholder': 'Password'
            }
    ))



class NewKeyForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'newKeyUsername',
                'placeholder': 'Enter username'
            }
        ))


class AuthenticateForm(forms.Form):
    key = forms.IntegerField()

