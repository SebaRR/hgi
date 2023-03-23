

from hgi_users.models import Empresa
from hgi_users.serializer import EmpresaSerializer
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


class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.all()
    authentication_classes = ()
    permission_classes = [permissions.AllowAny,]
    serializer_class = EmpresaSerializer
    http_method_names = ["get", "patch", "post"]

    def retrieve(self, request, pk):
        self.queryset = Empresa.objects.all()
        empresa = self.get_object()
        data_empresa = self.serializer_class(empresa).data
        return JsonResponse({"empresa":data_empresa}, status=200)
    
    def get_queryset(self):
        self.get_queryset = Empresa.objects.all().order_by("-fecha_creado")
        empresas = self.queryset

        if "search" in self.request.query_params.keys():
            nombre_query = Q(nombre__contains=self.request.query_params["search"])
            empresas = empresas.filter(nombre_query)
            
        return empresas
    
    def list(self, request):
        empresas = self.get_queryset()
        pages = Paginator(empresas, 99999)
        out_pag = 1
        total_pages = pages.num_pages
        count_objects = pages.count
        if self.request.query_params.keys():
            if 'page' in self.request.query_params.keys():
                page_asked = int(self.request.query_params['page'])
                if page_asked in pages.page_range:
                    out_pag = page_asked
        empresas_all = pages.page(out_pag).object_list
        serializer = self.serializer_class(empresas_all, many=True)
        response_data = serializer.data
        return JsonResponse({'total_pages': total_pages, 'total_objects':count_objects, 'actual_page': out_pag, 'objects': response_data}, status=200)