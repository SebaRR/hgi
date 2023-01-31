
from hgi_ventas.serializer import PartidaSerializer
from hgi_ventas.models import Partida
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
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator


class PartidaViewSet(viewsets.ModelViewSet):
    queryset = Partida.objects.all()
    authentication_classes = ()
    permission_classes = [permissions.AllowAny,]
    serializer_class = PartidaSerializer
    http_method_names = ["get", "patch", "delete", "post"]

    def retrieve(self, request, pk):
        self.queryset = Partida.objects.all()
        ppto = self.get_object()
        data_ppto = self.serializer_class(ppto).data
        return JsonResponse({"partida":data_ppto}, status=200)

    