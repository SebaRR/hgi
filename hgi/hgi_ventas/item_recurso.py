

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
            
        return items

    def list(self, request):
        items = self.get_queryset()
        pages = Paginator(items.order_by('fecha').reverse(), 25)
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