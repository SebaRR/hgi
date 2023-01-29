from hgi_ventas.serializer import PresupuestoSerializer
from hgi_ventas.models import Presupuesto
from hgi_static.models import Contrato
from hgi_static.serializer import ContratoSerializer
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


class ContratoViewSet(viewsets.ModelViewSet):
    queryset = Contrato.objects.all()
    authentication_classes = ()
    permission_classes = [permissions.AllowAny,]
    serializer_class = ContratoSerializer
    http_method_names = ["get", "patch", "delete", "post"]

    def retrieve(self, request, pk):
        self.queryset = Contrato.objects.all()
        contrato = self.get_object()
        data_contrato = self.serializer_class(contrato).data
        ppto = Presupuesto.objects.filter(contrato=data_contrato['id'])
        data_contrato['presupuestos'] = PresupuestoSerializer(ppto, many=True).data
        return JsonResponse({"contrato":data_contrato}, status=200)