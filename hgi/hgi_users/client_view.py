from django.utils import timezone
from django.shortcuts import render
from hgi_users.models import User
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
from django.core.paginator import Paginator



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
        contact = User.objects.get(id=data_client['contact'])
        data_client['contact_name'] = contact.short_name()
        return JsonResponse({"client":data_client}, status=200)
        
    def list(self, request):
        clients = self.get_queryset()
        pages = Paginator(clients.order_by('created_at').reverse(), 25)
        out_pag = 1
        total_pages = pages.num_pages
        count_objects = pages.count
        if self.request.query_params.keys():
            if 'page' in self.request.query_params.keys():
                page_asked = int(self.request.query_params['page'])
                if page_asked in pages.page_range:
                    out_pag = page_asked
        clients_all = pages.page(out_pag).object_list
        serializer = self.serializer_class(clients_all, many=True)
        response_data = serializer.data
        for client in response_data:
            contact = User.objects.get(id=client['contact'])
            client['contact_name'] = contact.short_name()
        return JsonResponse({'total_pages': total_pages, 'total_objects':count_objects, 'actual_page': out_pag, 'objects': response_data}, status=200)

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

    def destroy(self, request, *args, **kwargs):
        self.queryset = Client.objects.all()
        cliente = self.get_object()
        if cliente is not None:
            cliente.delete()
            return JsonResponse({'status_text': 'Cliente eliminado correctamente'}, status=200) 