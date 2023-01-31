from django.contrib import admin
from hgi_ventas.models import Presupuesto, OrdenCompra, ProductoOC, TipoOC, UnidadProducto, Partida

admin.site.register(Presupuesto)
admin.site.register(TipoOC)
admin.site.register(OrdenCompra)
admin.site.register(UnidadProducto)
admin.site.register(ProductoOC)
admin.site.register(Partida)