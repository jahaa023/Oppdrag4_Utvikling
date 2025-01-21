from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse, HttpResponseRedirect
from .forms import LoginForm, CreateAccountForm, OrderForm
from .models import users
from django.contrib.auth.hashers import make_password, check_password
import os
import json

# Create your views here.

# Function for loading in static js and css files
def importStaticFiles(name):
    context = {}
    static_dir = os.getcwd() + '\\torgersen_website\\static'
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

# Handles login form
def login_form_handler(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            # Get data
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            # Check if account exists
            if not users.objects.filter(username=username).exists():
                return JsonResponse({"error" : "wrong"})

            # Check if password is correct
            user = users.objects.get(username=username)
            if not check_password(password, user.password):
                return JsonResponse({"error" : "wrong"})

            # Set session variable
            uuid_str = str(user.user_id)
            request.session['user_id'] = uuid_str

            # Redirect
            return JsonResponse({"redirect" : 1})
        else:
            return JsonResponse({"error" : "invalid"})
    else:
        return HttpResponseForbidden("Method not Allowed")

# Renders template for account creation page
def lag_konto(request):
    context = importStaticFiles("lag_konto")
    context["form"] = CreateAccountForm()
    return render(request, "lag_konto.html", context)

# Handles create account form
def create_account_form_handler(request):
    if request.method == "POST":
        form = CreateAccountForm(request.POST)
        if form.is_valid():
            # Get data
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            full_name = form.cleaned_data["full_name"]
            email = form.cleaned_data["email"]

            # Check if username has non english characters
            whitelist = "abcdefghijklmnopqrstuvwxyz1234567890"
            username_lower = username.lower()
            for c in username_lower:
                if c not in whitelist:
                    return JsonResponse({"error" : "ascii"})

            # Check if username is taken
            if users.objects.filter(username=username).exists():
                return JsonResponse({"error" : "username_taken"})

            # Check if email is already registered
            if users.objects.filter(email=email).exists():
                return JsonResponse({"error" : "email_registered"})

            # Check if username is only numbers
            if username.isdigit():
                return JsonResponse({"error" : "numeric"})

            # Hash password
            password_hash = make_password(password)

            # Register user to database
            user = users(
                username=username,
                password=password_hash,
                full_name=full_name,
                email=email,
            )
            user.save()

            # Set session variables
            user = users.objects.get(username=username)
            uuid_str = str(user.user_id)
            request.session['user_id'] = uuid_str

            return JsonResponse({"redirect" : 1})
        else:
            return JsonResponse({"error" : "invalid"})
    else:
        return HttpResponseForbidden("Method not Allowed")

# Validates username as its being typed
def username_validate(request):
    if request.method == "POST":
        # Convert post data to dict from json
        data = json.loads(request.body)
        username = data.get("username")

        # Set the response
        json_response = {
            "ascii" : 0,
            "whitespace" : 0,
            "numeric" : 0,
            "between" : 0,
            "taken" : 0
        }

        # Check if username contains any non english chars
        whitelist = "abcdefghijklmnopqrstuvwxyz1234567890 "
        username_lower = username.lower()
        for c in username_lower:
            if c not in whitelist:
                json_response["ascii"] = 1
        
        # Check if username contains whitespace
        if " " in username:
            json_response["whitespace"] = 1
        
        # Check if username is only numbers
        if username.isdigit():
            json_response["numeric"] = 1
        
        # Check if username is between 5 to 30 letters
        if len(username) > 32 or len(username) < 5:
            json_response["between"] = 1

        # Check if username is taken
        if users.objects.filter(username=username).exists():
            json_response["taken"] = 1

        return JsonResponse(json_response)
    else:
        return HttpResponseForbidden("Method not Allowed")

# Renders template for main page
def hovedside(request):
    # If user is not logged in, redirect
    if 'user_id' not in request.session:
        return HttpResponseRedirect("/")

    # Get static files
    context = importStaticFiles("hovedside")

    # Get user information for context
    user_id = request.session.get("user_id")
    user = users.objects.get(user_id=user_id)
    context["user"] = user

    return render(request, "hovedside.html", context)

# Logs user out
def logout(request):
    # Flush session variables
    request.session.flush()
    return HttpResponseRedirect("/")

# renders page for ordering translation of books
def bestill(request):
    # If user is not logged in, redirect
    if 'user_id' not in request.session:
        return HttpResponseRedirect("/")

    # Get static files
    context = importStaticFiles("bestill")

    # Get form for placing order
    context["form"] = OrderForm()

    return render(request, "bestill.html", context)