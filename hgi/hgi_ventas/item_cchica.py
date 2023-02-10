
from hgi_ventas.models import ItemCajaChica
from hgi_ventas.serializer import ItemCajaChicaSerializer
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


class ItemCajaChicaViewSet(viewsets.ModelViewSet):
    queryset = ItemCajaChica.objects.all()
    authentication_classes = ()
    permission_classes = [permissions.AllowAny,]
    serializer_class = ItemCajaChicaSerializer
    http_method_names = ["get", "patch", "delete", "post"]

    def retrieve(self, request, pk):
        self.queryset = ItemCajaChica.objects.all()
        item = self.get_object()
        data_item = self.serializer_class(item).data
        return JsonResponse({"item_cch":data_item}, status=200)