from datetime import datetime
from django.db import models

from hgi_users.models import Client, User
from django.contrib.postgres.fields import ArrayField

"""
class Banco(models.Model):

    codigo = models.CharField(max_length=5)
    nombre = models.CharField(max_length=50)
    logo = models.CharField(max_length=50, null=True, blank=True)
"""
class EstadoObra(models.Model):

    nombre = models.CharField(max_length=20, null=False)


class Obra(models.Model):

    codigo = models.CharField(max_length=6, null=False)
    nombre = models.CharField(max_length=50, null=False)
    activo = models.BooleanField(default=True)
    creador = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1, null=False)
    cliente = models.ForeignKey(Client, on_delete=models.CASCADE, null=False)
    #estado = models.ForeignKey(EstadoObra, on_delete=models.CASCADE, null=False)
    fecha = models.DateTimeField(auto_now_add=True, null=True)



class ClasiContrato(models.Model):

    nombre = models.CharField(max_length=20, null=False)
    abreviatura = models.CharField(max_length=5, null=True)


class TipoContrato(models.Model):

    nombre = models.CharField(max_length=20, null=False)
    abreviatura = models.CharField(max_length=5, null=True)


class EstadoContrato(models.Model):

    nombre = models.CharField(max_length=20, null=False)
    abreviatura = models.CharField(max_length=5, null=True)


class Contrato(models.Model):

    codigo = models.CharField(max_length=9, null=False)
    nombre = models.CharField(max_length=50, null=False)
    direccion = models.CharField(max_length=50, null=False)
    activo =  models.BooleanField(default=True)

    par = models.BooleanField(default=False) #cargo por partida
    mat = models.BooleanField(default=False) #cargo por recurso
    mau = models.IntegerField(default=0) #autorizacion oc
    auo = models.BooleanField(default=False) #autorizar dcs de obra, no aplica (doctos = factura)
    proa = models.BooleanField(default=False) #controlar disponible
    oc = models.BooleanField(default=False) #oc obligatorio (factura) doctos con oc
    vis = models.BooleanField(default=False) #visado doctos (factura)
    uf = models.FloatField(null=False)
    sa = models.IntegerField(default=0) #controla sa (no aun)
    m2 = models.IntegerField(null=True) #dato
    peso = models.IntegerField(null=True) #dato
    ccp = models.BooleanField(default=False)
    
    estado = models.ForeignKey(EstadoContrato, on_delete=models.CASCADE, null=False)
    tipo = models.ForeignKey(TipoContrato, on_delete=models.CASCADE, null=False, default=6) 
    clasificacion = models.ForeignKey(ClasiContrato, on_delete=models.CASCADE, null=False)
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE, null=False)
    responsable = models.ForeignKey(User, related_name='user_responsable', on_delete=models.CASCADE, null=False)
    administrador = models.ForeignKey(User, related_name='user_administrador', on_delete=models.CASCADE, null=False)
    visitador = models.ForeignKey(User, related_name='user_visitador', on_delete=models.CASCADE, null=False)
    of_tecnica = models.ForeignKey(User, related_name='user_of_tecnica', on_delete=models.CASCADE, null=False)
    compras = models.ForeignKey(User, related_name='user_compras', on_delete=models.CASCADE, null=False)
    administrativo = models.ForeignKey(User, related_name='user_administrativo', on_delete=models.CASCADE, null=False)
    prevencionista = models.ForeignKey(User, related_name='user_prevencionista', on_delete=models.CASCADE, null=False)
    creador = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1, null=False)

    inicio = models.DateTimeField(auto_now_add=True, null=False)
    termino = models.DateTimeField(null=True)
    

class TipoPresupuesto(models.Model):

    descripcion = models.CharField(max_length=30, null=False)
    diminutivo = models.CharField(max_length=3, null=False)
    operacion = models.IntegerField(null=False)
    orden = models.IntegerField(null=False)
    creador = models.ForeignKey(User, related_name='user', on_delete=models.SET_DEFAULT, default=1, null=False)


class TipoPago(models.Model):

    descripcion = models.CharField(max_length=50)
    dias = models.IntegerField()
    orden = models.IntegerField()

    creador = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1, null=False) 


class Moneda(models.Model):

    descripcion = models.CharField(max_length=20, null=False)
    simbolo = models.CharField(max_length=3, null=False)
    dec = models.IntegerField()


class EstadoOC(models.Model):

    nombre = models.CharField(max_length=20, null=False)
    orden = models.IntegerField()

class PermisoContratoUser(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1, null=False)
    contrato = models.ForeignKey(Contrato, on_delete=models.SET_NULL, null=True)
    permisos = ArrayField(models.IntegerField(null=True), default=list)

#tabla de registro de cambios de estado en un contrato 

