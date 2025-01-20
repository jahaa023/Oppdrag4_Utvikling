# Forms for the website
from django import forms

# Form for logging in
class LoginForm(forms.Form):
    username = forms.CharField(label="", max_length=32, widget=forms.TextInput(attrs={'placeholder': 'Brukernavn'}))
    password = forms.CharField(label='', max_length=32, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))