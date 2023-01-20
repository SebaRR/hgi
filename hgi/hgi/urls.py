from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
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

slashless_router = routers.SimpleRouter(trailing_slash=False)
slashless_router.registry = router.registry[:]

urlpatterns = [
    
    re_path(r"^", include(router.urls)),
    path('admin/', admin.site.urls),
    path('create_user', user_view.register, name='register'),
    path('login', user_view.login, name='login'),
    path('logout', user_view.logout, name='logout'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
