
from hgi.utils import get_total_partidas
from hgi_ventas.models import Partida
from hgi_static.serializer import TipoPresupuestoSerializer
from hgi_ventas.serializer import PresupuestoSerializer
from hgi_static.models import TipoPresupuesto, Contrato
from hgi_ventas.models import Presupuesto
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
from django.db.models import Q
from django.core.paginator import Paginator


class PresupuestoViewSet(viewsets.ModelViewSet):
    queryset = Presupuesto.objects.all()
    authentication_classes = ()
    permission_classes = [permissions.AllowAny,]
    serializer_class = PresupuestoSerializer
    http_method_names = ["get", "patch", "delete", "post"]

    def retrieve(self, request, pk):
        self.queryset = Presupuesto.objects.all()
        ppto = self.get_object()
        data_ppto = self.serializer_class(ppto).data
        tipo = TipoPresupuesto.objects.get(id=data_ppto['tipo'])
        data_ppto['tipo'] = TipoPresupuestoSerializer(tipo).data
        return JsonResponse({"presupuesto":data_ppto}, status=200)

    def get_queryset(self):
        self.get_queryset = Presupuesto.objects.all()
        presupuestos = self.queryset

        if 'contrato' in self.request.query_params.keys():
            contrato = self.request.query_params['contrato']
            presupuestos = presupuestos.filter(contrato = contrato)

        if 'tipo' in self.request.query_params.keys():
            tipo = self.request.query_params['tipo']
            presupuestos = presupuestos.filter(tipo = tipo)
        
        if "search" in self.request.query_params.keys():
            text_query = Q(description__contains=self.request.query_params["glosa"])
            presupuestos = presupuestos.filter(text_query)
            
        return presupuestos

    def list(self, request):
        presupuestos = self.get_queryset()
        pages = Paginator(presupuestos.reverse(), 25)
        out_pag = 1
        total_pages = pages.num_pages
        count_objects = pages.count
        if self.request.query_params.keys():
            if 'page' in self.request.query_params.keys():
                page_asked = int(self.request.query_params['page'])
                if page_asked in pages.page_range:
                    out_pag = page_asked
        presupuestos_all = pages.page(out_pag).object_list
        serializer = self.serializer_class(presupuestos_all, many=True)
        response_data = serializer.data
        for presupuesto in presupuestos:
            contrato = Contrato.objects.get(id=presupuesto["contrato"])
            partidas = Partida.objects.filter(contrato=contrato)
            presupuesto["total_partidas"], presupuesto["total_APU"] = get_total_partidas(partidas)
            presupuesto["n_partidas"] = partidas.count()
            tipo = TipoPresupuesto.objects.get(id=presupuesto['tipo'])
            presupuesto["name_contrato"] = contrato.nombre
            presupuesto['tipo'] = TipoPresupuestoSerializer(tipo).data
        return JsonResponse({'total_pages': total_pages, 'total_objects':count_objects, 'actual_page': out_pag, 'objects': response_data}, status=200)