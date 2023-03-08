
from hgi_static.serializer import PermisoContratoUserSerializer
from hgi_static.models import PermisoContratoUser
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


class PermisoContratoUserViewSet(viewsets.ModelViewSet):
    queryset = PermisoContratoUser.objects.all()
    authentication_classes = ()
    permission_classes = [permissions.AllowAny,]
    serializer_class = PermisoContratoUserSerializer
    http_method_names = ["get", "patch", "delete", "post"]

    def retrieve(self, request, pk):
        self.queryset = PermisoContratoUser.objects.all()
        permiso_user = self.get_object()
        data_permiso_user = self.serializer_class(permiso_user).data
        return JsonResponse({"permiso_user":data_permiso_user}, status=200)
    
    def get_queryset(self):
        self.get_queryset = PermisoContratoUser.objects.all()
        permisos = self.queryset

        if 'user' in self.request.query_params.keys():
            user = self.request.query_params['user']
            permisos = permisos.filter(contrato = user)
            
        return permisos

    def list(self, request):
        permisos = self.get_queryset()
        pages = Paginator(permisos.reverse(), 25)
        out_pag = 1
        total_pages = pages.num_pages
        count_objects = pages.count
        if self.request.query_params.keys():
            if 'page' in self.request.query_params.keys():
                page_asked = int(self.request.query_params['page'])
                if page_asked in pages.page_range:
                    out_pag = page_asked
        permisos_all = pages.page(out_pag).object_list
        serializer = self.serializer_class(permisos_all, many=True)
        response_data = serializer.data

        return JsonResponse({'total_pages': total_pages, 'total_objects':count_objects, 'actual_page': out_pag, 'objects': response_data}, status=200)