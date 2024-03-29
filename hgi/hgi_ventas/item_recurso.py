

from hgi_ventas.models import ProdRecurso
from hgi.utils import get_user_from_usertoken
from hgi_ventas.models import ItemRecurso
from hgi_ventas.serializer import ItemRecursoSerializer
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

class ItemRecursoViewSet(viewsets.ModelViewSet):
    queryset = ItemRecurso.objects.all()
    authentication_classes = ()
    permission_classes = [permissions.AllowAny,]
    serializer_class = ItemRecursoSerializer
    http_method_names = ["get", "patch", "delete", "post"]

    def retrieve(self, request, pk):
        self.queryset = ItemRecurso.objects.all()
        item = self.get_object()
        data_item = self.serializer_class(item).data
        return JsonResponse({"item_rec":data_item}, status=200)
    
    def get_queryset(self):
        self.get_queryset = ItemRecurso.objects.all()
        items = self.queryset

        if 'partida' in self.request.query_params.keys():
            partida = self.request.query_params['partida']
            items = items.filter(partida = partida)

        if 'prodrecurso' in self.request.query_params.keys():
            prodrecurso = self.request.query_params['prodrecurso']
            items = items.filter(recurso = prodrecurso)
            
        return items

    def list(self, request):
        items = self.get_queryset()
        pages = Paginator(items.order_by('fecha').reverse(), 99999)
        out_pag = 1
        total_pages = pages.num_pages
        count_objects = pages.count
        if self.request.query_params.keys():
            if 'page' in self.request.query_params.keys():
                page_asked = int(self.request.query_params['page'])
                if page_asked in pages.page_range:
                    out_pag = page_asked
        items_all = pages.page(out_pag).object_list
        serializer = self.serializer_class(items_all, many=True)
        response_data = serializer.data
        
        return JsonResponse({'total_pages': total_pages, 'total_objects':count_objects, 'actual_page': out_pag, 'objects': response_data}, status=200)
    
    def partial_update(self, request, pk, *args, **kwargs):
        self.queryset = ItemRecurso.objects.all()
        item = self.get_object()
        serializer = self.serializer_class(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data_item = serializer.data
            return JsonResponse({"status_text": "ItemRecurso editado con exito.", "item_rec": data_item,},status=202)
        else:
            return JsonResponse({"status_text": str(serializer.errors)}, status=400) 
        
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

        prod_recurso = ProdRecurso.objects.get(id=data['recurso'])
        if "partida" not in data.keys():
            data['partida'] = prod_recurso.partida.id
        if "contrato" not in data.keys():
            data['contrato'] = prod_recurso.partida.contrato.id
            
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            item_rec_data = serializer.data
            return JsonResponse({"item_rec":item_rec_data}, status=201)
        return JsonResponse({'status_text':str(serializer.errors)}, status=201)