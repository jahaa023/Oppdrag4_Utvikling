# Forms for the website
from django import forms

# Form for logging in
class LoginForm(forms.Form):
    username = forms.CharField(label="", max_length=32, min_length=5, widget=forms.TextInput(attrs={'placeholder': 'Brukernavn'}))
    password = forms.CharField(label='', max_length=32, widget=forms.PasswordInput(attrs={'placeholder': 'Passord'}))

# Form for creating account
class CreateAccountForm(forms.Form):
    username = forms.CharField(label='', max_length=32, min_length=5, widget=forms.TextInput(attrs={'placeholder': 'Brukernavn'}))
    email = forms.CharField(label='', max_length=40, widget=forms.EmailInput(attrs={'placeholder': 'E-post'}))
    full_name = forms.CharField(label='', max_length=128, widget=forms.TextInput(attrs={'placeholder': 'Full navn'}))
    password = forms.CharField(label='', max_length=32, widget=forms.PasswordInput(attrs={'placeholder': 'Passord'}))