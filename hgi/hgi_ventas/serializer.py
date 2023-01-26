
from hgi_ventas.models import Presupuesto, OrdenCompra, ProductoOC, TipoOC, UnidadProducto
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
    class Meta:
        model = OrdenCompra
        fields = '__all__'


class UnidadProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadProducto
        fields = '__all__'

    
class ProductoOCSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductoOC
        fields = '__all__'