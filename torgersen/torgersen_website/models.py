from django.db import models
import uuid

# Create your models here.

# Model to create users table
class users(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
    username = models.CharField(max_length=30)
    full_name = models.CharField(max_length=128)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=40)

# Table for orders
class orders(models.Model):
    user_id = models.UUIDField()
    book = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    translate_from = models.CharField(max_length=64)
    translate_to = models.CharField(max_length=64)
    description = models.CharField(max_length=500)
    timestamp = models.CharField(max_length=64)
    cancelled = models.BooleanField(default=False)