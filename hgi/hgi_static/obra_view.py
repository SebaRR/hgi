from hgi_static.models import Obra
from hgi_static.serializer import ObraSerializer
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


class ObraViewSet(viewsets.ModelViewSet):
    queryset = Obra.objects.all()
    authentication_classes = ()
    permission_classes = [permissions.AllowAny,]
    serializer_class = ObraSerializer
    http_method_names = ["get", "patch", "delete", "post"]
