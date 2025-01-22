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
    path("place_order", views.place_order, name="place_order"),
    path("min_ko", views.min_ko, name="min_ko"),
    path("thank_you_modal", views.thank_you_modal, name="thank_you_modal"),
    path("cancel_order_modal", views.cancel_order_modal, name="cancel_order_modal"),
    path("cancel_order", views.cancel_order, name="cancel_order"),
    path("admin_dashboard", views.admin_dashboard, name="admin_dashboard"),
    path("admin_login", views.admin_login, name="admin_login"),
    path("admin_login_form_handler", views.admin_login_form_handler, name="admin_login_form_handler"),
    path("kontakt", views.kontakt, name="kontakt")
]