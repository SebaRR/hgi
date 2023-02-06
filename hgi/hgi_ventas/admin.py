from django.contrib import admin
from hgi_ventas.models import Presupuesto, OrdenCompra, ProductoOC, TipoOC, UnidadProducto, Partida, Recurso

class PresupuestoAdmin(admin.ModelAdmin):
    list_display = ["id","glosa", "prm", "pro", "tipo", "usuario", "contrato"]
    class meta:
        model = Presupuesto

class TipoOCAdmin(admin.ModelAdmin):
    list_display = ["id", "descripcion", "codigo", "usuario"]
    class meta:
        model = TipoOC

class OrdenCompraAdmin(admin.ModelAdmin):
    list_display = ["id", "autorizacion_adm", "autorizacion_res", "estado", "tipo", "creador", "emisor"]
    class meta:
        model = OrdenCompra

class UnidadProductoAdmin(admin.ModelAdmin):
    list_display = ["id", "nombre", "tiempo", "rfa"]
    class meta:
        model = UnidadProducto

class ProductoOCAdmin(admin.ModelAdmin):
    list_display = ["id", "producto", "cantidad", "precio", "descuento", "unidad", "recurso", "partida", "oc", "creador"]
    class meta:
        model = ProductoOC

class PartidaAdmin(admin.ModelAdmin):
    list_display = ["id", "codigo", "total", "ingresado", "creador", "contrato", "inicio", "termino"]
    class meta:
        model = Partida

class RecursoAdmin(admin.ModelAdmin):
    list_display = ["id", "codigo", "imputable", "asociado"]
    class meta:
        model = Recurso

admin.site.register(Presupuesto, PresupuestoAdmin)
admin.site.register(TipoOC, TipoOCAdmin)
admin.site.register(OrdenCompra, OrdenCompraAdmin)
admin.site.register(UnidadProducto, UnidadProductoAdmin)
admin.site.register(ProductoOC, ProductoOCAdmin)
admin.site.register(Partida, PartidaAdmin)
admin.site.register(Recurso, RecursoAdmin)