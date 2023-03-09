
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
from django.core.paginator import Paginator
from django.db.models import Q


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
    
    def get_queryset(self):
        self.get_queryset = Recurso.objects.filter(es_principal=True)
        recursos = self.queryset

        if "search" in self.request.query_params.keys():
            descripcion_query = Q(descripcion__contains=self.request.query_params["search"])
            recursos = recursos.filter(descripcion_query)
            
        return recursos
    
    def list(self, request):
        recursos = self.get_queryset()
        pages = Paginator(recursos.order_by('created_at').reverse(), 99999)
        out_pag = 1
        total_pages = pages.num_pages
        count_objects = pages.count
        if self.request.query_params.keys():
            if 'page' in self.request.query_params.keys():
                page_asked = int(self.request.query_params['page'])
                if page_asked in pages.page_range:
                    out_pag = page_asked
        recursos_all = pages.page(out_pag).object_list
        serializer = self.serializer_class(recursos_all, many=True)
        response_data = serializer.data
        for recurso in response_data:
            sub_recursos = Recurso.objects.filter(recurso=recurso['id'])
            sub_recursos_data = RecursoSerializer(sub_recursos, many=True).data
            recurso["sub_recursos"] = sub_recursos_data
        return JsonResponse({'total_pages': total_pages, 'total_objects':count_objects, 'actual_page': out_pag, 'objects': response_data}, status=200)