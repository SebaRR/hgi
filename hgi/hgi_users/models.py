from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    type_choices = [
        ('Empleado', 'Empleado'),
        ('Usuario', 'Usuario'),
    ]
    username = models.CharField(max_length=30, null=True, unique=True)
    email = models.EmailField(blank=False, unique=True)
    first_name = models.CharField(max_length=30)
    first_last_name = models.CharField(max_length=30, null=True)
    second_last_name = models.CharField(max_length=30, null=True)

    position = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    rut = models.CharField(max_length=15, null=False)
    active = models.BooleanField(default=True)

    #Datos de empleado
    codigo = models.CharField(max_length=20, null=True, blank=True)


    updated_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def short_name(self):
        if self.first_last_name is not None:
            return self.first_name + " " + self.first_last_name
        else:
            return self.first_name


class UserToken(models.Model):
    
    token = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    validation = models.BooleanField(default=False)
    recovery = models.BooleanField(default=False)


class Region(models.Model):
    name = models.CharField(max_length=60, default="")
    roman_number = models.CharField(max_length=5, default="")
    number = models.IntegerField(default=1)
    abbreviation = models.CharField(max_length=2, default="")
    
    class Meta:
        managed = True
        verbose_name = "Región"
        verbose_name_plural = "Regiones"

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=60)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    
    class Meta:
        managed = True
        verbose_name = "Ciudad"
        verbose_name_plural = "Ciudades"
        order_with_respect_to = 'region'

    def __str__(self):
        return self.name


class Country(models.Model):

    name = models.CharField(max_length=80)
    iso = models.SmallIntegerField()
    iso2 = models.CharField(max_length=2)
    iso3 = models.CharField(max_length=3)

    def __str__(self):
        return self.name



class Client(models.Model):
    country_choices = [('Chile', 'Chile'),
        ('Argentina', 'Argentina'),]

    business_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    commune = models.CharField(max_length=100)
    
    activity = models.CharField(max_length=100)
    rut = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    country = models.CharField(max_length=20,choices=country_choices, default='Chile',)
    active = models.BooleanField(default=True)

    contact = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)

    updated_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

