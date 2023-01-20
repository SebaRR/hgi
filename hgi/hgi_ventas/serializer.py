from hgi_ventas.models import Presupuesto
from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer

class PresupuestoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Presupuesto
        fields = '__all__'