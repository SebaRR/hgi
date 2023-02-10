
from hgi_ventas.models import Presupuesto, OrdenCompra, ProductoOC, TipoOC, UnidadProducto, Partida, Recurso, ProdRecurso, CajaChica, EstadoCajaChica, ItemCajaChica, TipoDocumento
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
        productos = ProductoOC.objects.filter(oc=instance.id)
        for producto in productos:
            total += producto.precio * producto.cantidad
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


class PartidaSerializer(serializers.ModelSerializer):
    productos = serializers.SerializerMethodField()

    class Meta:
        model = Partida
        fields = '__all__'
    
    def get_productos(self, instance):
        productos = ProductoOC.objects.filter(partida=instance.id)
        return ProductoOCSerializer(productos, many=True).data


class PresupuestoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Presupuesto
        fields = '__all__'


class ProdRecursoSerializer(serializers.ModelSerializer):
    disponible = serializers.SerializerMethodField()

    class Meta:
        model = ProdRecurso
        fields = '__all__'

    def get_disponible(self, instance):
        total = instance.total - instance.ingresado
        return total
    

class EstadoCajaChicaSerializer(serializers.ModelSerializer):
    disponible = serializers.SerializerMethodField()

    class Meta:
        model = EstadoCajaChica
        fields = '__all__'


class CajaChicaSerializer(serializers.ModelSerializer):
    disponible = serializers.SerializerMethodField()

    class Meta:
        model = CajaChica
        fields = '__all__'


class TipoDocumentoSerializer(serializers.ModelSerializer):
    disponible = serializers.SerializerMethodField()

    class Meta:
        model = TipoDocumento
        fields = '__all__'

    
class ItemCajaChicaSerializer(serializers.ModelSerializer):
    disponible = serializers.SerializerMethodField()

    class Meta:
        model = ItemCajaChica
        fields = '__all__'