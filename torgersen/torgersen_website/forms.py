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

# Form for placing order
class OrderForm(forms.Form):
    book = forms.CharField(label="", max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Navnet til boken (og serienummer hvis boken er i en serie)'}))
    author = forms.CharField(label="", max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Forfatter til boken'}))
    translate_from = forms.CharField(label="", max_length=64, widget=forms.TextInput(attrs={'placeholder': 'Språket boken er i'}))
    translate_to = forms.CharField(label="", max_length=64, widget=forms.TextInput(attrs={'placeholder': 'Språket du vil oversette til'}))
    description = forms.CharField(label='', max_length=500, widget=forms.Textarea(attrs={'placeholder': 'Beskrivelse eller informasjon som du syntes kan være viktig'}))