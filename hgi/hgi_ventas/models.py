from django.db import models
from hgi_static.models import Contrato, TipoPresupuesto, TipoPago, Moneda, EstadoOC
from hgi_users.models import User, Proveedor


class Presupuesto(models.Model):

    glosa = models.CharField(max_length=50, null=False)
    pre = models.IntegerField(null=False)
    prm = models.IntegerField(null=False) #Cobrar
    pro = models.IntegerField(null=False) #Gastar - rige ordenes de compra
    ing = models.IntegerField(null=False)
    ccp = models.CharField(max_length=10, null=False)

    tipo = models.ForeignKey(TipoPresupuesto, on_delete=models.SET_NULL, null=True)
    
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    contrato = models.ForeignKey(Contrato, on_delete=models.SET_NULL, null=True)


class TipoOC(models.Model):

    descripcion = models.CharField(max_length=50, null=False)
    texto = models.CharField(max_length=1000, null=False)
    codigo = models.IntegerField()
    sub = models.BooleanField(null=True, blank=True)
    rem = models.BooleanField(null=True, blank=True)
    pro = models.IntegerField(null=True, blank=True)
    pag = models.IntegerField(null=True, blank=True)
    arr = models.BooleanField(null=True, blank=True)
    rah = models.BooleanField(null=True, blank=True)
    cch = models.BooleanField(null=True, blank=True)
    man = models.BooleanField(null=True, blank=True)
    ope = models.IntegerField(null=True, blank=True)
    nco = models.CharField(max_length=3, null=True, blank=True)
    col = models.CharField(max_length=6, null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)



class OrdenCompra(models.Model):

    glosa = models.CharField(max_length=500, null=False)
    descuento_general = models.IntegerField()
    observacion = models.CharField(max_length=500, null=False)
    ref_oc = models.CharField(max_length=20, null=False)

    direccion_despacho = models.CharField(max_length=60, null=False) #parte del contrato - editable
    
    ate_oc = models.CharField(max_length=50, null=False) #parte del proveedor
    mail = models.CharField(max_length=40, null=False) #parte del proveedor - editable
    mail2 = models.CharField(max_length=40, null=False) #parte del proveedor - editable

    autorizacion_adm = models.BooleanField(default=False) #user A
    autorizacion_res = models.BooleanField(default=False) #user R

    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True)
    estado = models.ForeignKey(EstadoOC, on_delete=models.SET_NULL, null=True) 
    forma_pago = models.ForeignKey(TipoPago, on_delete=models.SET_NULL, null=True)
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE, null=False)
    emisor = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="emisor_oc", null=True)  # emisor -> la necesita
    creador = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="creador_oc", null=True) # quien la hizo
    tipo = models.ForeignKey(TipoOC, on_delete=models.SET_NULL, null=True, default=6)
    moneda = models.ForeignKey(Moneda, on_delete=models.SET_NULL, null=True)

    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    fecha_despacho = models.DateTimeField(auto_now_add=True) # fecha creacion - editable
    fecha = models.DateTimeField(auto_now_add=True) # fecha creacion - editable


class UnidadProducto(models.Model):

    nombre = models.CharField(max_length=10, null=False)
    tiempo = models.CharField(max_length=5, null=True, blank=True)
    rfa = models.CharField(max_length=10, null=True, blank=True)


class Partida(models.Model):

    codigo = models.CharField(max_length=10, null=True, blank=True)
    descripcion = models.CharField(max_length=90, null=True, blank=True)
    total = models.IntegerField()
    ingresado = models.IntegerField()

    creador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    contrato = models.ForeignKey(Contrato, on_delete=models.SET_NULL, null=True)

    inicio = models.DateTimeField(auto_now_add=True)
    termino = models.DateTimeField(null=True)


class Recurso(models.Model):

    codigo = models.CharField(max_length=5, null=False)
    descripcion = models.CharField(max_length=50, null=False)
    imputable = models.BooleanField(default=True)
    es_principal = models.BooleanField(default=False)
    recurso = models.ForeignKey('self', related_name="recurso_padre", on_delete=models.SET_NULL, null=True)


class ProdRecurso(models.Model):

    total = models.IntegerField()
    ingresado = models.IntegerField()

    partida = models.ForeignKey(Partida, on_delete=models.SET_NULL, null=True)
    recurso = models.ForeignKey(Recurso, on_delete=models.SET_NULL, null=True)
    creador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    inicio = models.DateTimeField(auto_now_add=True)
    termino = models.DateTimeField(null=True)


class ItemRecurso(models.Model):
    
    descripcion = models.CharField(max_length=80, null=True, blank=True)
    sca = models.CharField(max_length=25, null=True, blank=True)
    unidad = models.CharField(max_length=10, null=True, blank=True)
    cantidad = models.FloatField()
    precio = models.IntegerField()
    observacion = models.CharField(max_length=500, null=True, blank=True)
    activo = models.BooleanField(default=False)
    ing = models.IntegerField()

    fecha = models.DateTimeField(auto_now_add=True)
    recurso = models.ForeignKey(ProdRecurso, on_delete=models.SET_NULL, null=True)
    partida = models.ForeignKey(Partida, on_delete=models.SET_NULL, null=True)
    contrato = models.ForeignKey(Contrato, on_delete=models.SET_NULL, null=True)
    creador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    def total_precio(self):
        total = self.cantidad * self.precio    
        return total


class ProductoOC(models.Model):

    producto = models.CharField(max_length=150, null=False)
    cantidad = models.FloatField()
    precio = models.FloatField()
    descuento = models.FloatField()
    mat = models.IntegerField(null=True, blank=True) # si tiene "partida" tiene mat -> material?
    afe = models.IntegerField(null=True, blank=True) 
    ing = models.IntegerField(null=True, blank=True) #ingreso?
    cpp = models.CharField(max_length=15, null=True, blank=True)
    lso = models.IntegerField(null=True, blank=True) #si no tiene ing tiene esto
    doc = models.IntegerField(null=True, blank=True) # 0
    car = models.IntegerField(null=True, blank=True) # 0
    moc = models.IntegerField(null=True, blank=True) # 0 
    ant = models.IntegerField(null=True, blank=True) # 0

    recurso = models.ForeignKey(ProdRecurso, on_delete=models.SET_NULL, null=True)
    partida = models.ForeignKey(Partida, on_delete=models.SET_NULL, null=True)
    creador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    unidad = models.ForeignKey(UnidadProducto, on_delete=models.SET_NULL, null=True)
    oc = models.ForeignKey(OrdenCompra, on_delete=models.CASCADE, null=False)

    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    fecha_termino = models.DateTimeField(null=True)

    def total_precio(self):
        total = self.cantidad * self.precio
        descuento = (self.descuento * total)/100        
        return (total - descuento)


class EstadoCajaChica(models.Model):

    estado = models.CharField(max_length=20, null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    oba = models.CharField(max_length=15, null=True, blank=True)

    creador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class CajaChica(models.Model):

    fecha = models.DateTimeField(auto_now_add=True) 
    aut = models.IntegerField()
    total = models.IntegerField() #total de los productos que contiene
    estado = models.ForeignKey(EstadoCajaChica, on_delete=models.SET_NULL, null=True)
    creador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    contrato = models.ForeignKey(Contrato, on_delete=models.SET_NULL, null=True)
    oc = models.ForeignKey(OrdenCompra, on_delete=models.CASCADE, null=True)


class TipoDocumento(models.Model):

    descripcion = models.CharField(max_length=30, null=True, blank=True)
    operacion = models.IntegerField(null=True, blank=True)
    nco = models.CharField(max_length=3, null=True, blank=True)
    orden_1 = models.IntegerField(null=True, blank=True)
    orden_2 = models.IntegerField(null=True, blank=True)
    orden_3 = models.IntegerField(null=True, blank=True)
    iva = models.BooleanField(default=True)
    ret = models.IntegerField(null=True, blank=True)
    referencia = models.ForeignKey('self', related_name="doc_referencia", on_delete=models.SET_NULL, null=True)
    fim = models.CharField(max_length=2, null=True, blank=True)
    lve = models.IntegerField(null=True, blank=True)
    olv = models.IntegerField(null=True, blank=True)



class ItemCajaChica(models.Model):

    detalle = models.CharField(max_length=70, null=True, blank=True)
    orden = models.IntegerField()
    total = models.IntegerField()
    ie = models.IntegerField(null=True, blank=True) #gasto en caso de petroleo - bencina

    tipo = models.ForeignKey(TipoDocumento, on_delete=models.SET_NULL, null=True)
    contrato = models.ForeignKey(Contrato, on_delete=models.SET_NULL, null=True)
    partida = models.ForeignKey(Partida, on_delete=models.SET_NULL, null=True)
    creador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    caja_chica = models.ForeignKey(CajaChica, on_delete=models.SET_NULL, null=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True)
    recurso = models.ForeignKey(ProdRecurso, on_delete=models.SET_NULL, null=True)

    fecha = models.DateTimeField(auto_now_add=True) 
