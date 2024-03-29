
from hgi_users.models import Empresa
from hgi_static.serializer import PermisoContratoUserSerializer
from hgi_static.models import PermisoContratoUser
from hgi_users.models import PermisoContrato
from hgi_users.models import Country, City, Proveedor, Region, Client, User, UserToken, CargoUser
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_flex_fields import FlexFieldsModelSerializer
from django.core.exceptions import ObjectDoesNotExist


class PermisoContratoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermisoContrato
        fields = '__all__'

class CreateUserSerializer(FlexFieldsModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_superuser', 'position',
                  'first_name', 'first_last_name', 'second_last_name','active',
                  'password', 'created_at', 'updated_at', 'phone_number', 'rut', 'codigo','empresa')
        read_only_fields = ('created_at', 'updated_at',)

    def create(self, validated_data):
        user = super(CreateUserSerializer, self).create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


    def save(self, *args, **kwargs):
        instance = super(CreateUserSerializer, self).save(*args, **kwargs)
        token = Token.objects.get_or_create(user=self.instance)
        return instance, token

    def get_token(self):
        try:
            token = Token.objects.get(user=self.instance)
        except ObjectDoesNotExist:
            token = Token.objects.create(user=self.instance)
        return token

    def new_token(self):
        Token.objects.filter(user=self.instance).delete()
   

class CargoUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CargoUser
        fields = '__all__'


class UserSerializer(FlexFieldsModelSerializer):
    password = serializers.CharField(write_only=True)
    permiso_contrato = serializers.SerializerMethodField()
    name_empresa = serializers.SerializerMethodField()
    cargo_user = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_superuser', 'position',
                  'first_name', 'first_last_name', 'second_last_name','active',
                  'password', 'created_at', 'updated_at', 'phone_number', 'rut', 'codigo', 'permiso_contrato', 'name_empresa', 'cargo_user')
        read_only_fields = ('created_at', 'updated_at',)
    
    def get_token(self):
        try:
            token = Token.objects.get(user=self.instance)
        except ObjectDoesNotExist:
            token = Token.objects.create(user=self.instance)
        return token
    
    def get_permiso_contrato(self, instance):
        permisos = PermisoContratoUser.objects.filter(user=instance.id)
        permisos = PermisoContratoUserSerializer(permisos, many=True).data
        permiso_contrato_user = {}
        for permiso in permisos:
            permiso_contrato = {}
            for id_permiso in permiso["permisos"]:
                permiso_contrato_data = PermisoContratoSerializer(PermisoContrato.objects.get(id=id_permiso)).data
                permiso_contrato[permiso_contrato_data["nombre"]] = permiso_contrato_data
            permiso_contrato_user[permiso["contrato"]] = permiso_contrato
        return permiso_contrato_user

    def get_name_empresa(self, instance):
        if instance.empresa is not None:
            return instance.empresa.nombre
        else:
            return "Empresa Eliminada"
    
    def get_cargo_user(self, instance):
        if instance.position is not None:
            return CargoUserSerializer(instance.position).data
        else:
            return {}



class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserToken
        fields = ('user', 'token', 'validation', 'recovery')


class ClientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id', 'business_name', 'address', 'commune', 'activity', 'rut','phone','country','active','contact','region','city','code','email',)
        read_only_fields = ('created_at', 'updated_at',)
    

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'


class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = '__all__'