from django.contrib import admin
from .models import users, orders

# Register your models here.

admin.site.register(users)
admin.site.register(orders)