from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse, HttpResponseRedirect
from .forms import LoginForm, CreateAccountForm, OrderForm
from .models import users, orders
from django.contrib.auth.hashers import make_password, check_password
import os
import json
from datetime import datetime

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

# Function for handling order form
def place_order(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            # Get data
            book = form.cleaned_data["book"]
            author = form.cleaned_data["author"]
            translate_from = form.cleaned_data["translate_from"]
            translate_to = form.cleaned_data["translate_to"]
            description = form.cleaned_data["description"]

            # Get user id
            if 'user_id' not in request.session:
                return JsonResponse({"error" : "invalid"})
            else:
                user_id = request.session.get("user_id")
            
            # Get timestamp
            now = datetime.now()
            timestamp = now.strftime("%d-%m-%Y %H:%M")

            # Register order to database
            order = orders(
                user_id=user_id,
                book=book,
                author=author,
                translate_from=translate_from,
                translate_to=translate_to,
                description=description,
                timestamp=timestamp
            )

            order.save()

            return JsonResponse({"ok" : 1})
        else:
            return JsonResponse({"error" : "invalid"})
    else:
        return HttpResponseForbidden("Method not Allowed")

# Renders modal that thanks user for order
def thank_you_modal(request):
    if request.method == "POST":
        # If user is not logged in, redirect
        if 'user_id' not in request.session:
            return HttpResponseRedirect("/")

        form = OrderForm(request.POST)
        if form.is_valid():
            context = {}

            # Get data
            book = form.cleaned_data["book"]
            author = form.cleaned_data["author"]

            # Pass into context
            context["book"] = book
            context["author"] = author

            # Get css file
            static_dir = os.getcwd() + '\\torgersen_website\\static'
            with open(static_dir + '\\css\\thank_you.css', 'r') as file:
                context["thank_you_css"] = file.read()

            # Get user information for context
            user_id = request.session.get("user_id")
            user = users.objects.get(user_id=user_id)
            context["user"] = user

            return render(request, "thank_you_modal.html", context)
        else:
            return HttpResponse("error")

# Renders a page where users can see their orders
def min_ko(request):
    # If user is not logged in, redirect
    if 'user_id' not in request.session:
        return HttpResponseRedirect("/")

    # Get static files
    context = importStaticFiles("min_ko")

    # Get user information
    user_id = request.session.get("user_id")
    user = users.objects.get(user_id=user_id)
    context["user"] = user

    # Get the users orders that arent cancelled
    user_orders = orders.objects.filter(user_id=user_id, cancelled=False)
    context["orders"] = user_orders

    return render(request, "min_ko.html", context)

# Renders modal to confirm cancellation of order
def cancel_order_modal(request):
    if request.method == "POST":
        # If user is not logged in, redirect
        if 'user_id' not in request.session:
            return HttpResponseRedirect("/")
        else:
            # Get user id
            user_id = request.session.get("user_id")
        
        context = {}

        # Convert post data to dict from json
        data = json.loads(request.body)
        order_id = data.get("order_id")

        # Check if the order belongs to the logged in user and if order is not already cancelled
        if orders.objects.filter(user_id=user_id, id=order_id, cancelled=False).exists():
            order = orders.objects.get(id=order_id)
            context["book"] = order.book
            context["order_id"] = order_id
        else:
            return HttpResponse("error")
        
        # Get css file
        static_dir = os.getcwd() + '\\torgersen_website\\static'
        with open(static_dir + '\\css\\cancel_order.css', 'r') as file:
            context["cancel_order_css"] = file.read()

        # Return modal
        return render(request, "cancel_order_modal.html", context)
    else:
        return HttpResponse("error")

# Cancels order by putting cancelled column to true
def cancel_order(request):
    if request.method == "POST":
        # If user is not logged in, redirect
        if 'user_id' not in request.session:
            return HttpResponseRedirect("/")
        else:
            # Get user id
            user_id = request.session.get("user_id")
        
        # Get order id
        if "order_id" in request.POST:
            order_id = request.POST.get("order_id")
        else:
            return JsonResponse({"error" : "error"})
        
        # Check if the order belongs to the logged in user and if order is not already cancelled
        if orders.objects.filter(user_id=user_id, id=order_id, cancelled=False).exists():
            order = orders.objects.get(id=order_id)
        else:
            return JsonResponse({"error" : "error"})
        
        # Cancel order
        order.cancelled = True
        order.save()

        # Return name of div to delete
        div_id = "ordercontainer_" + order_id

        return JsonResponse({"div_id" : div_id, "ok" : 1})
    else:
        return HttpResponse("error")

# Renders the admin login page
def admin_login(request):
    # Get static files
    context = importStaticFiles("admin_login")

    context["form"] = LoginForm()

    return render(request, "admin_login.html", context)

# Handles admin login form
def admin_login_form_handler(request):
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
            
            # Check if user is an admin
            if user.role != "admin":
                return JsonResponse({"error" : "forbidden"})

            # Set session variable
            uuid_str = str(user.user_id)
            request.session['user_id'] = uuid_str

            # Redirect
            return JsonResponse({"redirect" : 1})
        else:
            return JsonResponse({"error" : "invalid"})
    else:
        return HttpResponseForbidden("Method not Allowed")

# Renders the admin dashboard
def admin_dashboard(request):
    # If user is not logged in, redirect
    if 'user_id' not in request.session:
        return HttpResponseRedirect("/")
    else:
        # Get user id
        user_id = request.session.get("user_id")

        # Check if user is admin, if not: redirect
        if not users.objects.filter(user_id=user_id, role="admin").exists():
            return HttpResponseRedirect("/")

    # Get static files
    context = importStaticFiles("admin_dashboard")

    # Get users table for context
    users_context = users.objects.all()
    context["users"] = users_context

    # Get orders table for context
    orders_context = orders.objects.all()
    context["orders"] = orders_context

    return render(request, "admin_dashboard.html", context)

# Renders contact page
def kontakt(request):
    # If user is not logged in, redirect
    if 'user_id' not in request.session:
        return HttpResponseRedirect("/")

    # Get static files
    context = importStaticFiles("kontakt")

    return render(request, "kontakt.html", context)

# Changes role of requested user
def admin_change_role(request):
    if request.method == "POST":
        # If user is not logged in, redirect
        if 'user_id' not in request.session:
            return HttpResponseRedirect("/")
        else:
            # Get user id
            user_id = request.session.get("user_id")

            # Check if user is admin, if not: redirect
            if not users.objects.filter(user_id=user_id, role="admin").exists():
                return HttpResponseRedirect("/")
        
        # Get posted user id
        data = json.loads(request.body)

        if "user_id" in data:
            user_id = data.get("user_id")
        else:
            return JsonResponse({"error" : "error"})
        
        # Get users role
        user = users.objects.get(user_id=user_id)

        # If role is user, change to admin and vice versa
        if user.role == "user":
            user.role = "admin"
        else:
            user.role = "user"

        user.save()

        # Return the td tag that the role of the user contains
        div_id = "tabletd_role_" + user_id

        return JsonResponse({"div_id" : div_id, "success" : 1, "newrole" : user.role})
    else :
        return HttpResponseForbidden("Method not allowed")