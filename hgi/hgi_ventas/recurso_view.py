
from hgi_ventas.models import Recurso
from hgi_ventas.serializer import RecursoSerializer
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


class RecursoViewSet(viewsets.ModelViewSet):
    queryset = Recurso.objects.all()
    authentication_classes = ()
    permission_classes = [permissions.AllowAny,]
    serializer_class = RecursoSerializer
    http_method_names = ["get", "patch", "delete", "post"]

    def retrieve(self, request, pk):
        self.queryset = Recurso.objects.all()
        recurso = self.get_object()
        data_recurso = self.serializer_class(recurso).data
        return JsonResponse({"recurso":data_recurso}, status=200)