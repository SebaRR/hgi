
from hgi_ventas.models import Presupuesto, OrdenCompra, ProductoOC, TipoOC, UnidadProducto, Partida, Recurso
from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer


class TipoOCSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoOC
        fields = '__all__'


class OrdenCompraSerializer(serializers.ModelSerializer):
    total_oc = serializers.SerializerMethodField()

    class Meta:
        model = OrdenCompra
        fields = '__all__'
    
    def get_total_oc(self, instance):
        total = 0
        productos = ProductoOC.objects.filter(oc=instance.id)
        for producto in productos:
            total += producto.precio * producto.cantidad
        return total


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
    n_partidas = serializers.SerializerMethodField()
    total_partidas = serializers.SerializerMethodField()
    total_APU = serializers.SerializerMethodField()

    class Meta:
        model = Presupuesto
        fields = '__all__'

    def get_productos(self, instance):
        total = 0
        productos = ProductoOC.objects.filter(partida=instance.id)
        return ProductoOCSerializer(productos, many=True).data