
from hgi_ventas.models import Presupuesto, OrdenCompra, ProductoOC, TipoOC, UnidadProducto, Partida, Recurso, ProdRecurso, CajaChica, EstadoCajaChica, ItemCajaChica, TipoDocumento, ItemRecurso
from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer


class TipoOCSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoOC
        fields = '__all__'


class OrdenCompraSerializer(serializers.ModelSerializer):
    total_oc = serializers.SerializerMethodField()
    n_productos = serializers.SerializerMethodField()

    class Meta:
        model = OrdenCompra
        fields = '__all__'
    
    def get_total_oc(self, instance):
        total = 0
        if instance.tipo != 13:
            productos = ProductoOC.objects.filter(oc=instance.id)
            for producto in productos:
                total += producto.precio * producto.cantidad
        else:
            total = instance.total
        return total

    def get_n_productos(self, instance):
        products = ProductoOC.objects.filter(oc=instance.id)
        return products.count()


class UnidadProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadProducto
        fields = '__all__'

    
class ProductoOCSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductoOC
        fields = '__all__'


class RecursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recurso
        fields = '__all__'


class PresupuestoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Presupuesto
        fields = '__all__'


class ProdRecursoSerializer(serializers.ModelSerializer):
    disponible = serializers.SerializerMethodField()
    n_items = serializers.SerializerMethodField()
    contratado = serializers.SerializerMethodField()
    suma_total = serializers.SerializerMethodField()

    class Meta:
        model = ProdRecurso
        fields = '__all__'

    def get_disponible(self, instance):
        ingresado = 0
        items = ItemRecurso.objects.filter(recurso = instance.id)
        for item in items:
            ingresado += item.total_precio()
        total = instance.total - ingresado
        return total

    def get_n_items(self, instance):
        return (ItemRecurso.objects.filter(recurso=instance.id)).count()
    
    def get_contratado(self, instance):
        productos = ItemRecurso.objects.filter(partida=instance.partida.id).filter(recurso=instance.recurso.id)
        total_contratado = 0
        for producto in productos:
            total_contratado += producto.total_precio()
        return total_contratado
    
    def get_suma_total(self, instance):
        productos = ItemRecurso.objects.filter(recurso=instance.recurso.id)
        total = 0
        for producto in productos:
            total += producto.total_precio()
        return total



class PartidaSerializer(serializers.ModelSerializer):
    prodrecursos = serializers.SerializerMethodField()
    contratado = serializers.SerializerMethodField()
    suma_total = serializers.SerializerMethodField()

    class Meta:
        model = Partida
        fields = '__all__'
    
    def get_prodrecursos(self, instance):
        productos = ProdRecurso.objects.filter(partida=instance.id)
        return ProdRecursoSerializer(productos, many=True).data
    
    def get_contratado(self, instance):
        productos = ProductoOC.objects.filter(partida=instance.id).filter(oc__tipo__id=7)
        total_contratado = 0
        for producto in productos:
            total_contratado += producto.total_precio()
        return total_contratado

    def get_suma_total(self, instance):
        productos = ProductoOC.objects.filter(partida=instance.id)
        total = 0
        for producto in productos:
            total += producto.total_precio()
        return total


class ItemRecursoSerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemRecurso
        fields = '__all__'


class EstadoCajaChicaSerializer(serializers.ModelSerializer):

    class Meta:
        model = EstadoCajaChica
        fields = '__all__'


class CajaChicaSerializer(serializers.ModelSerializer):
    name_empresa = serializers.SerializerMethodField()

    class Meta:
        model = CajaChica
        fields = '__all__'

    def get_name_empresa(self, instance):
        if instance.empresa is not None:
            return instance.empresa.nombre
        else:
            return "Empresa Eliminada"
        
class TipoDocumentoSerializer(serializers.ModelSerializer):

    class Meta:
        model = TipoDocumento
        fields = '__all__'

    
class ItemCajaChicaSerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemCajaChica
        fields = '__all__'