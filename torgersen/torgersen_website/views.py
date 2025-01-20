from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import LoginForm, CreateAccountForm
import os

# Create your views here.

# Function for loading in static js and css files
def importStaticFiles(name):
    context = {}
    static_dir = os.getcwd() + '\\torgersen_website\\static'
    print(static_dir)
    # universal files
    with open(static_dir + '\\css\\universal.css', 'r') as file:
        context["universal_css"] = file.read()
    with open(static_dir + '\\js\\universal.js', 'r') as file:
        context["universal_js"] = file.read()

    # Specific files
    with open(static_dir + '\\css\\' + name + '.css', 'r') as file:
        context[f"{name}_css"] = file.read()
    with open(static_dir + '\\js\\' + name + '.js', 'r') as file:
        context[f"{name}_js"] = file.read()

    return context


# Renders template for login page
def index(request):
    context = importStaticFiles("index")
    context["form"] = LoginForm()
    return render(request, "index.html", context)

# Renders template for account creation page
def lag_konto(request):
    context = importStaticFiles("lag_konto")
    context["form"] = CreateAccountForm()
    return render(request, "lag_konto.html", context)