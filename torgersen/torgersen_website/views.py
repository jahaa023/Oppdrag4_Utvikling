from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import LoginForm, CreateAccountForm

# Create your views here.

# Renders template for login page
def index(request):
    context = {}
    context["form"] = LoginForm()
    return render(request, "index.html", context)

# Renders template for account creation page
def lag_konto(request):
    context = {}
    context["form"] = CreateAccountForm()
    return render(request, "lag_konto.html", context)