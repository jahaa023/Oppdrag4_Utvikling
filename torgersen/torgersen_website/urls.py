from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("lag_konto", views.lag_konto, name="lag_konto"),
    path("login_form_handler", views.login_form_handler, name="login_form_handler"),
    path("create_account_form_handler", views.create_account_form_handler, name="create_account_form_handler"),
    path("username_validate", views.username_validate, name="username_validate"),
    path("hovedside", views.hovedside, name="hovedside"),
    path("logout", views.logout, name="logout"),
    path("bestill", views.bestill, name="bestill"),
    path("place_order", views.place_order, name="place_order")
]