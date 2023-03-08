
from hgi_static.models import PermisoContratoUser
from hgi_ventas.models import ProductoOC
from hgi_ventas.models import Presupuesto, Partida
from hgi_static.models import Contrato, Obra, TipoPresupuesto, ClasiContrato, EstadoContrato, EstadoOC, Moneda, TipoContrato, TipoPago
from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer


class ContratoSerializer(serializers.ModelSerializer):
    total_pro = serializers.SerializerMethodField()
    total_prm = serializers.SerializerMethodField()
    total_partidas = serializers.SerializerMethodField()
    n_partidas = serializers.SerializerMethodField()
    total_apu = serializers.SerializerMethodField()

    class Meta:
        model = Contrato
        fields = '__all__'
    
    def get_total_pro(self, instance):
        total = 0
        try:
            pres = Presupuesto.objects.filter(contrato=instance.id)
            for pre in pres:
                total += pre.pro * pre.tipo.operacion
        except Presupuesto.DoesNotExist:
            return total
        return total

    def get_total_prm(self, instance):
        total = 0
        try:
            pres = Presupuesto.objects.filter(contrato=instance.id)
            for pre in pres:
                total += pre.prm * pre.tipo.operacion
        except Presupuesto.DoesNotExist:
            return total
        return total
    
    def get_total_partidas(self, instance):
        total = 0
        try:
            partidas = Partida.objects.filter(contrato=instance.id)
            for partida in partidas:
                total += partida.ingresado
        except Presupuesto.DoesNotExist:
            return total
        return total

    def get_n_partidas(self, instance):
        try:
            partidas = Partida.objects.filter(contrato=instance.id)
            return partidas.count()
        except Partida.DoesNotExist:
            return 0
    
    def get_total_apu(self, instance):
        total = 0
        try:
            productos = ProductoOC.objects.filter(partida__contrato=instance.id)
            for producto in productos:
                total += producto.total_precio()
        except ProductoOC.DoesNotExist:
            return total
        return total
        


class ObraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Obra
        fields = '__all__'
    

class TipoPresupuestoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoPresupuesto
        fields = '__all__'


class ClasiContratoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClasiContrato
        fields = '__all__'


class TipoContratoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoContrato
        fields = '__all__'


class EstadoContratoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoContrato
        fields = '__all__'


class TipoPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoPago
        fields = '__all__'


class MonedaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Moneda
        fields = '__all__'

        
class EstadoOCSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoOC
        fields = '__all__'


class PermisoContratoUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermisoContratoUser
        fields = '__all__'