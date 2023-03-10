

from hgi.utils import get_user_from_usertoken
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
from django.core.paginator import Paginator

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
    
    def get_queryset(self):
        self.get_queryset = ProdRecurso.objects.all()
        products = self.queryset

        if 'partida' in self.request.query_params.keys():
            partida = self.request.query_params['partida']
            products = products.filter(partida = partida)
            
        return products

    def list(self, request):
        productos = self.get_queryset()
        pages = Paginator(productos.order_by('inicio').reverse(), 99999)
        out_pag = 1
        total_pages = pages.num_pages
        count_objects = pages.count
        if self.request.query_params.keys():
            if 'page' in self.request.query_params.keys():
                page_asked = int(self.request.query_params['page'])
                if page_asked in pages.page_range:
                    out_pag = page_asked
        productos_all = pages.page(out_pag).object_list
        serializer = self.serializer_class(productos_all, many=True)
        response_data = serializer.data
        
        return JsonResponse({'total_pages': total_pages, 'total_objects':count_objects, 'actual_page': out_pag, 'objects': response_data}, status=200)
    
    def create(self, request):

        try:
            data = json.loads(request.body)
        except JSONDecodeError as error:
            return JsonResponse({'Request error': str(error)},status=400)
        
        if 'Authorization' in request.headers:
            user = get_user_from_usertoken(request.headers['Authorization'])
        else:
            return JsonResponse ({'status_text':'No usaste token'}, status=403)
        
        if "creador" not in data.keys():
            data['creador'] = user.id
        
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            prod_recurso_data= serializer.data
            return JsonResponse({"prod_recurso":prod_recurso_data}, status=201)
        return JsonResponse({'status_text':str(serializer.errors)}, status=201)