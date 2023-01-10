from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):

    username = models.CharField(max_length=30, null=True, unique=True)
    email = models.EmailField(blank=False, unique=True)
    first_name = models.CharField(max_length=30)
    first_last_name = models.CharField(max_length=30, null=True)
    second_last_name = models.CharField(max_length=30, null=True)

    position = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    rut = models.CharField(max_length=15, null=False)
    active = models.BooleanField(default=True)

    updated_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def short_name(self):
        if self.first_last_name is not None:
            return self.first_name + " " + self.first_last_name
        else:
            return self.first_name


class UserToken (models.Model):
    
    token = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    validation = models.BooleanField(default=False)
    recovery = models.BooleanField(default=False)