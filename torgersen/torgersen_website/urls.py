from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("lag_konto", views.lag_konto, name="lag_konto"),
    path("login_form_handler", views.login_form_handler, name="login_form_handler"),
    path("create_account_form_handler", views.create_account_form_handler, name="create_account_form_handler")
]