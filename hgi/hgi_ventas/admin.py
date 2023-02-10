from django.contrib import admin
from hgi_ventas.models import Presupuesto, OrdenCompra, ProductoOC, TipoOC, UnidadProducto, Partida, Recurso, ProdRecurso, CajaChica, EstadoCajaChica, ItemCajaChica, TipoDocumento, ItemRecurso

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
    list_display = ["id", "codigo", "descripcion", "imputable", "recurso"]
    class meta:
        model = Recurso

class ProdRecursoAdmin(admin.ModelAdmin):
    list_display = ["id", "total", "ingresado"]
    class meta:
        model = ProdRecurso

class ItemCajaChicaAdmin(admin.ModelAdmin):
    list_display = ["id", "detalle", "total"]
    class meta:
        model = ItemCajaChica

class TipoDocumentoAdmin(admin.ModelAdmin):
    list_display = ["id", "descripcion", "operacion"]
    class meta:
        model = TipoDocumento

class CajaChicaAdmin(admin.ModelAdmin):
    list_display = ["id", "total", "creador"]
    class meta:
        model = CajaChica

class EstadoCajaChicaAdmin(admin.ModelAdmin):
    list_display = ["id", "estado", "creador"]
    class meta:
        model = EstadoCajaChica

class ItemRecursoAdmin(admin.ModelAdmin):
    list_display = ["id", "descripcion", "cantidad", "precio"]
    class meta:
        model = ItemRecurso


admin.site.register(Presupuesto, PresupuestoAdmin)
admin.site.register(TipoOC, TipoOCAdmin)
admin.site.register(OrdenCompra, OrdenCompraAdmin)
admin.site.register(UnidadProducto, UnidadProductoAdmin)
admin.site.register(ProductoOC, ProductoOCAdmin)
admin.site.register(Partida, PartidaAdmin)
admin.site.register(Recurso, RecursoAdmin)
admin.site.register(ItemRecurso, ItemRecursoAdmin)
admin.site.register(ProdRecurso, ProdRecursoAdmin)
admin.site.register(ItemCajaChica, ItemCajaChicaAdmin)
admin.site.register(TipoDocumento, TipoDocumentoAdmin)
admin.site.register(CajaChica, CajaChicaAdmin)
admin.site.register(EstadoCajaChica, EstadoCajaChicaAdmin)