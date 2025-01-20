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