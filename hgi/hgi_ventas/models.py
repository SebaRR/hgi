from django.db import models
from hgi_static.models import Contrato, TipoPresupuesto
from hgi_users.models import User


class Presupuesto(models.Model):

    glosa = models.CharField(max_length=50, null=False)
    pre = models.BigIntegerField(null=False)
    prm = models.BigIntegerField(null=False) #Cobrar
    pro = models.BigIntegerField(null=False) #Gastar - rige ordenes de compra
    ing = models.IntegerField(null=False)
    ccp = models.CharField(max_length=10, null=False)

    tipo = models.ForeignKey(TipoPresupuesto, on_delete=models.SET_NULL, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    contrato = models.ForeignKey(Contrato, on_delete=models.SET_NULL, null=True)