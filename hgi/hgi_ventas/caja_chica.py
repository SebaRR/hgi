
from hgi_ventas.models import CajaChica
from hgi_ventas.serializer import CajaChicaSerializer
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


class CajaChicaViewSet(viewsets.ModelViewSet):
    queryset = CajaChica.objects.all()
    authentication_classes = ()
    permission_classes = [permissions.AllowAny,]
    serializer_class = CajaChicaSerializer
    http_method_names = ["get", "patch", "delete", "post"]

    def retrieve(self, request, pk):
        self.queryset = CajaChica.objects.all()
        recurso = self.get_object()
        data_recurso = self.serializer_class(recurso).data
        return JsonResponse({"recurso":data_recurso}, status=200)