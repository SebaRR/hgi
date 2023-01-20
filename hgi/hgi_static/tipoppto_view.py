from hgi_static.models import TipoPresupuesto
from hgi_static.serializer import TipoPresupuestoSerializer
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
    action,
)
from django.views.decorators.csrf import csrf_exempt
import json
from json.decoder import JSONDecodeError
from django.http.response import JsonResponse
from rest_framework import viewsets, permissions


class TipoPresupuestoViewSet(viewsets.ModelViewSet):
    queryset = TipoPresupuesto.objects.all()
    authentication_classes = ()
    permission_classes = [permissions.AllowAny,]
    serializer_class = TipoPresupuestoSerializer
    http_method_names = ["get", "patch", "delete", "post"]