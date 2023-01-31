
from hgi_ventas.models import Presupuesto, OrdenCompra, ProductoOC, TipoOC, UnidadProducto, Partida
from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer


class PresupuestoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Presupuesto
        fields = '__all__'


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


class PartidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partida
        fields = '__all__'