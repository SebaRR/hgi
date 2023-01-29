from hgi_static.serializer import TipoPresupuestoSerializer
from hgi_ventas.serializer import PresupuestoSerializer
from hgi_static.models import TipoPresupuesto
from hgi_ventas.models import Presupuesto
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


class PresupuestoViewSet(viewsets.ModelViewSet):
    queryset = Presupuesto.objects.all()
    authentication_classes = ()
    permission_classes = [permissions.AllowAny,]
    serializer_class = PresupuestoSerializer
    http_method_names = ["get", "patch", "delete", "post"]

    def retrieve(self, request, pk):
        self.queryset = Presupuesto.objects.all()
        ppto = self.get_object()
        data_ppto = self.serializer_class(ppto).data
        tipo = TipoPresupuesto.objects.get(id=data_ppto['tipo'])
        data_ppto['tipo'] = TipoPresupuestoSerializer(tipo).data
        return JsonResponse({"presupuesto":data_ppto}, status=200)