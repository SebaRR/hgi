

from hgi_ventas.serializer import ProdRecursoSerializer
from hgi_ventas.models import ProdRecurso
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


class ProdRecursoViewSet(viewsets.ModelViewSet):
    queryset = ProdRecurso.objects.all()
    authentication_classes = ()
    permission_classes = [permissions.AllowAny,]
    serializer_class = ProdRecursoSerializer
    http_method_names = ["get", "patch", "delete", "post"]

    def retrieve(self, request, pk):
        self.queryset = ProdRecurso.objects.all()
        prod_recurso = self.get_object()
        data_prod_recurso = self.serializer_class(prod_recurso).data
        return JsonResponse({"prod_recurso":data_prod_recurso}, status=200)