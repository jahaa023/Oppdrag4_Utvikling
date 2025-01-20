from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("lag_konto", views.lag_konto, name="lag_konto")
]