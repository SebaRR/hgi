
from django.contrib import admin
from hgi_users.models import PermisoContrato
from hgi_users.models import City, UserToken, Region, Client, User, Country, CargoUser, Proveedor

class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "username", "email", "phone_number", "codigo", "position"]
    class meta:
        model = User

class ClientAdmin(admin.ModelAdmin):
    list_display = ["id", "business_name", "address", "rut", "activity", "phone", "contact"]
    class meta:
        model = Client

class CargoUserAdmin(admin.ModelAdmin):
    list_display = ["nombre", "por_contrato", "ver_oc", "modificar_oc", "ver_vb", "modificar_vb"]
    class meta:
        model = CargoUser

class ProveedorAdmin(admin.ModelAdmin):
    list_display = ["id", "rut", "rs", "telefono", "web", "creador"]
    class meta:
        model = Proveedor

class PermisoContratoAdmin(admin.ModelAdmin):
    list_display = ["id", "nombre", "ver_vb", "modificar_vb", "ver_contrato", "modificar_contrato", "ver_ppto", "modificar_ppto", "ver_oc", "modificar_oc", "mano_obra", "ver_cch", "modificar_cch", "ver_ccr", "modificar_ccr"; "ver_ccp", "modificar_ccp"]
    class meta:
        model = PermisoContrato 

admin.site.register(User, UserAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Region)
admin.site.register(City)
admin.site.register(UserToken)
admin.site.register(Country)
admin.site.register(CargoUser, CargoUserAdmin)
admin.site.register(Proveedor, ProveedorAdmin)
admin.site.register(PermisoContrato, PermisoContratoAdmin)
