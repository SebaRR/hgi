from hgi_users.models import Client
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
from django.core.paginator import Paginator


class ObraViewSet(viewsets.ModelViewSet):
    queryset = Obra.objects.all()
    authentication_classes = ()
    permission_classes = [permissions.AllowAny,]
    serializer_class = ObraSerializer
    http_method_names = ["get", "patch", "delete", "post"]

    def retrieve(self, request, pk):
        self.queryset = Obra.objects.all()
        obra = self.get_object()
        data_obra = self.serializer_class(obra).data
        client = Client.objects.get(id=data_obra['cliente'])
        data_obra['client_name'] = client.business_name
        return JsonResponse({"obra":data_obra}, status=200)
    
    def list(self, request):
        obras = self.get_queryset()
        pages = Paginator(obras.order_by('fecha').reverse(), 25)
        out_pag = 1
        total_pages = pages.num_pages
        count_objects = pages.count
        if self.request.query_params.keys():
            if 'page' in self.request.query_params.keys():
                page_asked = int(self.request.query_params['page'])
                if page_asked in pages.page_range:
                    out_pag = page_asked
        obras_all = pages.page(out_pag).object_list
        serializer = self.serializer_class(obras_all, many=True)
        response_data = serializer.data
        for obra in response_data:
            client = Client.objects.get(id=obra['cliente'])
            obra['client_name'] = client.business_name
        
        return JsonResponse({'total_pages': total_pages, 'total_objects':count_objects, 'actual_page': out_pag, 'objects': response_data}, status=200)
    
    def destroy(self, request, *args, **kwargs):
        self.queryset = Obra.objects.all()
        obra = self.get_object()
        if obra is not None:
            obra.delete()
            return JsonResponse({'status_text': 'Obra eliminada correctamente'}, status=200)

