
from django.contrib import admin
from hgi_users.models import City, UserToken, Region, Client, User, Country

# Register your models here.

admin.site.register(User)
admin.site.register(Client)
admin.site.register(Region)
admin.site.register(City)
admin.site.register(UserToken)
admin.site.register(Country)