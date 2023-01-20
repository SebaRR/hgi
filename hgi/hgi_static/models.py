from django.db import models

from hgi_users.models import City, Region, User
"""
class Proveedor(models.Model):
    
    rut = models.CharField(max_length=20)
    rs = models.CharField(max_length=50)
    direccion = models.CharField(max_length=60)
    ciudad = models.ForeignKey(City, null=True, blank=True)
    region = models.ForeignKey(Region, null=True, blank=True)
    pais = models.ForeignKey(Pais, null=False)
    telefono = models.CharField(max_length=10)
    web = models.CharField(max_length=25)
    contacto = models.CharField(max_length=50)
    mail_contacto = models.CharField(max_length=40)
    usuario = models.CharField(max_length=50)
    mail2_contacto = models.CharField(max_length=40)
    nombre = models.CharField(max_length=50)
    credito = models.IntegerField()
    cuenta = models.CharField(max_length=20)
    activo = models.BooleanField(default=True)

    fecha_creado = models.DateTimeField(auto_now_add=True)
    fecha_editado = models.DateTimeField(null=True, blank=True)


class Banco(models.Model):

    codigo = models.CharField(max_length=5)
    nombre = models.CharField(max_length=50)
    logo = models.CharField(max_length=50, null=True, blank=True)
"""


class Obra(models.Model):

    codigo = models.CharField(max_length=6, null=False)
    nombre = models.CharField(max_length=50, null=False)
    act = models.CharField(max_length=2, null=False, default='Si')
    asu = models.CharField(max_length=25, null=False)


class Contrato(models.Model):

    codigo = models.CharField(max_length=9, null=False)
    estado = models.IntegerField(null=False)
    nombre = models.CharField(max_length=50, null=False)
    direccion = models.CharField(max_length=50, null=False)
    act =  models.CharField(max_length=2, null=False, default='Si')
    usu = models.CharField(max_length=25, null=False)
    par = models.BooleanField(null=False, default=0)
    mat = models.BooleanField(null=False, default=0)
    mau = models.IntegerField(null=False, default=0)
    auo = models.BooleanField(null=False, default=0)
    mon = models.BigIntegerField(null=False)
    proa = models.BooleanField(null=False, default=0)
    oc = models.BooleanField(null=False, default=0)
    pro = models.BigIntegerField(null=False)
    vis = models.BooleanField(null=False, default=0)
    uf = models.FloatField(null=False)
    sa = models.IntegerField(default=0)
    m2 = models.IntegerField()
    peso = models.IntegerField()
    clasificacion = models.IntegerField()
    tipo = models.CharField(max_length=100, null=False)
    ccp = models.IntegerField(default=0)
    
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE, null=True)
    responsable = models.ForeignKey(User, related_name='user_responsable', on_delete=models.SET_NULL, null=True)
    administrador = models.ForeignKey(User, related_name='user_administrador', on_delete=models.SET_NULL, null=True)
    of_tecnica = models.ForeignKey(User, related_name='user_of_tecnica', on_delete=models.SET_NULL, null=True)
    compras = models.ForeignKey(User, related_name='user_compras', on_delete=models.SET_NULL, null=True)
    administrativo = models.ForeignKey(User, related_name='user_administrativo', on_delete=models.SET_NULL, null=True)
    visitador = models.ForeignKey(User, related_name='user_visitador', on_delete=models.SET_NULL, null=True)
    prevencionista = models.ForeignKey(User, related_name='user_prevencionista', on_delete=models.SET_NULL, null=True)
    inicio = models.DateTimeField(auto_now_add=True, null=False)
    termino = models.DateTimeField(null=True)


class TipoPresupuesto(models.Model):

    descripcion = models.CharField(max_length=30, null=False)
    diminutivo = models.CharField(max_length=3, null=False)
    operacion = models.IntegerField(null=False)
    orden = models.IntegerField(null=False)
    usuario = models.ForeignKey(User, related_name='user', on_delete=models.SET_NULL, null=True)
    
