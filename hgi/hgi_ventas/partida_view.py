
from hgi_ventas.serializer import PartidaSerializer
from hgi_ventas.models import Partida
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
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator


class PartidaViewSet(viewsets.ModelViewSet):
    queryset = Partida.objects.all()
    authentication_classes = ()
    permission_classes = [permissions.AllowAny,]
    serializer_class = PartidaSerializer
    http_method_names = ["get", "patch", "delete", "post"]

    def retrieve(self, request, pk):
        self.queryset = Partida.objects.all()
        partida = self.get_object()
        data_partida = self.serializer_class(partida).data
        return JsonResponse({"partida":data_partida}, status=200)

    def get_queryset(self):
        self.get_queryset = Partida.objects.all()
        partidas = self.queryset

        if 'contrato' in self.request.query_params.keys():
            contrato = self.request.query_params['contrato']
            partidas = partidas.filter(contrato = contrato)
            
        return partidas

    def list(self, request):
        partidas = self.get_queryset()
        pages = Paginator(partidas.order_by('inicio').reverse(), 25)
        out_pag = 1
        total_pages = pages.num_pages
        count_objects = pages.count
        if self.request.query_params.keys():
            if 'page' in self.request.query_params.keys():
                page_asked = int(self.request.query_params['page'])
                if page_asked in pages.page_range:
                    out_pag = page_asked
        partidas_all = pages.page(out_pag).object_list
        serializer = self.serializer_class(partidas_all, many=True)
        response_data = serializer.data

        return JsonResponse({'total_pages': total_pages, 'total_objects':count_objects, 'actual_page': out_pag, 'objects': response_data}, status=200)