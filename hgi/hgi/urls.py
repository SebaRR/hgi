from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from hgi_ventas.prodrecurso_view import ProdRecursoViewSet
from hgi_ventas.recurso_view import RecursoViewSet
from hgi_users.cargo_user import CargoUserViewSet
from hgi_ventas.partida_view import PartidaViewSet
from hgi_static.estado_oc_view import EstadoOCViewSet
from hgi_static.moneda_view import MonedaViewSet
from hgi_static.tipo_pago_view import TipoPagoViewSet
from hgi_static.estado_contrato_view import EstadoContratoViewSet
from hgi_static.tipocontrato_view import TipoContratoViewSet
from hgi_static.clasicontrato_view import ClasiContratoViewSet
from hgi_users.city_view import CityViewSet
from hgi_users.region_view import RegionViewSet
from hgi_users.country_view import CountryViewSet
from hgi_users.proveedor_view import ProveedorViewSet
from hgi_ventas.producto_oc_view import ProductoOCViewSet
from hgi_ventas.unidad_producto_view import UnidadProductoViewSet
from hgi_ventas.orden_compra_view import OrdenCompraViewSet
from hgi_ventas.tipooc_view import TipoOCViewSet
from hgi_static.obra_view import ObraViewSet
from hgi_ventas.presupuesto_view import PresupuestoViewSet
from hgi_static.tipoppto_view import TipoPresupuestoViewSet
from hgi_static.contrato_view import ContratoViewSet
from hgi_users import client_view
from hgi_users import user_view
from rest_framework import routers
from django.conf.urls import include

router = routers.SimpleRouter()
router.register(r"users", user_view.UserViewSet)
router.register(r"clients", client_view.ClientViewSet)
router.register(r"contratos", ContratoViewSet)
router.register(r"tipo_pptos", TipoPresupuestoViewSet)
router.register(r"presupuesto", PresupuestoViewSet)
router.register(r"obras", ObraViewSet)
router.register(r"tipo_oc", TipoOCViewSet)
router.register(r"orden_compra", OrdenCompraViewSet)
router.register(r"unidad_producto", UnidadProductoViewSet)
router.register(r"producto_oc", ProductoOCViewSet)
router.register(r"proveedor", ProveedorViewSet)
router.register(r"country", CountryViewSet)
router.register(r"region", RegionViewSet)
router.register(r"city", CityViewSet)
router.register(r"clasi_contrato", ClasiContratoViewSet)
router.register(r"tipo_contrato", TipoContratoViewSet)
router.register(r"estado_contrato", EstadoContratoViewSet)
router.register(r"tipo_pago", TipoPagoViewSet)
router.register(r"moneda", MonedaViewSet)
router.register(r"estado_oc", EstadoOCViewSet)
router.register(r"partida", PartidaViewSet)
router.register(r"cargo_user", CargoUserViewSet)
router.register(r"recursos", RecursoViewSet)
router.register(r"prod_recurso", ProdRecursoViewSet)

slashless_router = routers.SimpleRouter(trailing_slash=False)
slashless_router.registry = router.registry[:]

urlpatterns = [
    
    re_path(r"^", include(router.urls)),
    path('admin/', admin.site.urls),
    path('create_user', user_view.register, name='register'),
    path('login', user_view.login, name='login'),
    path('login_v2', user_view.login_v2, name='login_v2'),
    path('logout', user_view.logout_v1, name='logout'),
    path('load_user', user_view.load_user, name='load_user'),
    

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
