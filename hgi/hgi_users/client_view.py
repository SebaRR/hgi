from django.utils import timezone
from django.shortcuts import render
from hgi_users.serializer import ClientsSerializer
from hgi_users.models import Client
from hgi_users.serializer import UserSerializer
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
from rest_framework import viewsets




class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    authentication_classes = ()
    permission_classes = []
    serializer_class = ClientsSerializer
    http_method_names = ["get", "patch", "delete", "post"]


    def retrieve(self, request, pk):
        self.queryset = Client.objects.all()
        client = self.get_object()
        data_client = self.serializer_class(client).data
        return JsonResponse({"client":data_client}, status=200)


    def partial_update(self, request, pk, *args, **kwargs):
        self.queryset = Client.objects.all()
        client = self.get_object()
        edited = timezone.now()
        client.updated_at = edited
        client.save()
        serializer = self.serializer_class(client, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data_client = serializer.data
            return JsonResponse({"status_text": "Cliente editado con exito.", "client": data_client,},status=202)
        else:
            return JsonResponse({"status_text": str(serializer.errors)}, status=400)