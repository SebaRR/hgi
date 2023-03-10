
from hgi.utils import get_user_from_usertoken
from hgi_ventas.models import ProductoOC
from hgi_ventas.serializer import ProductoOCSerializer
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


class ProductoOCViewSet(viewsets.ModelViewSet):
    queryset = ProductoOC.objects.all()
    authentication_classes = ()
    permission_classes = [permissions.AllowAny,]
    serializer_class = ProductoOCSerializer
    http_method_names = ["get", "patch", "delete", "post"]

    def retrieve(self, request, pk):
        self.queryset = ProductoOC.objects.all()
        ppto = self.get_object()
        data_ppto = self.serializer_class(ppto).data
        return JsonResponse({"producto_oc":data_ppto}, status=200)

    def get_queryset(self):
        self.get_queryset = ProductoOC.objects.all()
        products = self.queryset

        if 'partida' in self.request.query_params.keys():
            partida = self.request.query_params['partida']
            products = products.filter(partida = partida)

        if 'oc' in self.request.query_params.keys():
            oc = self.request.query_params['oc']
            products = products.filter(oc = oc)
        
        if 'contrato' in self.request.query_params.keys():
            contrato = self.request.query_params['contrato']
            products = products.filter(partida__contrato = contrato)

        if "search" in self.request.query_params.keys():
            text_query = Q(producto__contains=self.request.query_params["search"])
            products = products.filter(text_query)
            
        return products

    def list(self, request):
        productos = self.get_queryset()
        pages = Paginator(productos.order_by('fecha_ingreso').reverse(), 25)
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
            
        serializer = self.serializer_class(data = data)
        if serializer.is_valid():
            serializer.save()
            producto_data = serializer.data
            response = {'producto_oc': producto_data}
            return JsonResponse(response, status=201)
        return JsonResponse({'status_text': str(serializer.errors)}, status=400)
    
    def partial_update(self, request, pk, *args, **kwargs):
        self.queryset = ProductoOC.objects.all()
        producto = self.get_object()
        serializer = self.serializer_class(producto, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data_producto = serializer.data
            return JsonResponse({"status_text": "ProductoOC editado con exito.", "producto_oc": data_producto,},status=202)
        else:
            return JsonResponse({"status_text": str(serializer.errors)}, status=400) 