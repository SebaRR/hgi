
from django.contrib import admin
from hgi_users.models import Client
from hgi_users.models import User

# Register your models here.

admin.site.register(User)
admin.site.register(Client)