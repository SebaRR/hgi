
from hgi_ventas.models import TipoDocumento
from hgi_ventas.serializer import TipoDocumentoSerializer
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


class TipoDocumentoViewSet(viewsets.ModelViewSet):
    queryset = TipoDocumento.objects.all()
    authentication_classes = ()
    permission_classes = [permissions.AllowAny,]
    serializer_class = TipoDocumentoSerializer
    http_method_names = ["get", "patch", "delete", "post"]

    def retrieve(self, request, pk):
        self.queryset = TipoDocumento.objects.all()
        tipo = self.get_object()
        data_tipo = self.serializer_class(tipo).data
        return JsonResponse({"tipo":data_tipo}, status=200)