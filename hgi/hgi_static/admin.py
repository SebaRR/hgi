from django.contrib import admin
from hgi_static.models import Contrato, Obra, TipoPresupuesto, ClasiContrato, EstadoContrato, EstadoOC, Moneda, TipoContrato, TipoPago



admin.site.register(Contrato)
admin.site.register(Obra)
admin.site.register(TipoPresupuesto)
admin.site.register(ClasiContrato)
admin.site.register(TipoContrato)
admin.site.register(EstadoContrato)
admin.site.register(TipoPago)
admin.site.register(Moneda)
admin.site.register(EstadoOC)



