from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from hgi_users import client_view
from hgi_users import user_view
from rest_framework import routers
from django.conf.urls import include

router = routers.SimpleRouter()
router.register(r"users", user_view.UserViewSet)
router.register(r"clients", client_view.ClientViewSet)

slashless_router = routers.SimpleRouter(trailing_slash=False)
slashless_router.registry = router.registry[:]

urlpatterns = [

    re_path(r"^", include(router.urls)),
    path('admin/', admin.site.urls),
    path('create_user', user_view.register, name='register'),
    path('login', user_view.login, name='login'),
    path('logout', user_view.logout, name='logout'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
