from django.contrib import admin
from hgi_static.models import PermisoContratoUser
from hgi_static.models import Contrato, Obra, TipoPresupuesto, ClasiContrato, EstadoContrato, EstadoOC, Moneda, TipoContrato, TipoPago, EstadoObra

class ContratoAdmin(admin.ModelAdmin):
    list_display = ["id", "codigo", "nombre", "tipo", "inicio", "termino"]
    class meta:
        model = Contrato

class ObraAdmin(admin.ModelAdmin):
    list_display = ["id", "codigo", "nombre", "cliente", "creador"]
    class meta:
        model = Obra

class TipoPresupuestoAdmin(admin.ModelAdmin):
    list_display = ["id", "descripcion", "operacion", "creador"]
    class meta:
        model = TipoPresupuesto

class ClasiContratoAdmin(admin.ModelAdmin):
    list_display = ["id", "nombre", "abreviatura"]
    class meta:
        model = ClasiContrato

class TipoContratoAdmin(admin.ModelAdmin):
    list_display = ["id", "nombre", "abreviatura"]
    class meta:
        model = TipoContrato

class EstadoContratoAdmin(admin.ModelAdmin):
    list_display = ["id", "nombre", "abreviatura"]
    class meta:
        model = EstadoContrato

class EstadoOCAdmin(admin.ModelAdmin):
    list_display = ["id", "nombre", "orden"]
    class meta:
        model = EstadoOC

class EstadoObraAdmin(admin.ModelAdmin):
    list_display = ["id", "nombre"]
    class meta:
        model = EstadoObra

class PermisoContratoUserAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "contrato", "permisos"]
    class meta:
        model = PermisoContratoUser


admin.site.register(Contrato, ContratoAdmin)
admin.site.register(Obra, ObraAdmin)
admin.site.register(TipoPresupuesto, TipoPresupuestoAdmin)
admin.site.register(ClasiContrato, ClasiContratoAdmin)
admin.site.register(TipoContrato, TipoContratoAdmin)
admin.site.register(EstadoContrato, EstadoContratoAdmin)
admin.site.register(TipoPago)
admin.site.register(Moneda)
admin.site.register(EstadoOC, EstadoOCAdmin)
admin.site.register(EstadoObra, EstadoObraAdmin)
admin.site.register(PermisoContratoUser, PermisoContratoUserAdmin)

