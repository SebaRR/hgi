 
from hgi_ventas.serializer import PresupuestoSerializer
from hgi_ventas.models import Presupuesto
from hgi_static.models import Contrato, EstadoContrato, Obra
from hgi_static.serializer import ContratoSerializer
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



class ContratoViewSet(viewsets.ModelViewSet):
    queryset = Contrato.objects.all()
    authentication_classes = ()
    permission_classes = [permissions.AllowAny,]
    serializer_class = ContratoSerializer
    http_method_names = ["get", "patch", "delete", "post"]

    def retrieve(self, request, pk):
        self.queryset = Contrato.objects.all()
        contrato = self.get_object()
        data_contrato = self.serializer_class(contrato).data
        ppto = Presupuesto.objects.filter(contrato=data_contrato['id'])
        data_contrato['presupuestos'] = PresupuestoSerializer(ppto, many=True).data
        status = EstadoContrato.objects.get(id=data_contrato['estado'])
        obra = Obra.objects.get(id=data_contrato['obra'])
        data_contrato['estado_name'] = status.nombre
        data_contrato['obra_name'] = obra.nombre
        return JsonResponse({"contrato":data_contrato}, status=200)
    
    def list(self, request):
        contratos = self.get_queryset()
        pages = Paginator(contratos.order_by('inicio').reverse(), 25)
        out_pag = 1
        total_pages = pages.num_pages
        count_objects = pages.count
        if self.request.query_params.keys():
            if 'page' in self.request.query_params.keys():
                page_asked = int(self.request.query_params['page'])
                if page_asked in pages.page_range:
                    out_pag = page_asked
        contratos_all = pages.page(out_pag).object_list
        serializer = self.serializer_class(contratos_all, many=True)
        response_data = serializer.data
        for contrato in response_data:
            status = EstadoContrato.objects.get(id=contrato['estado'])
            obra = Obra.objects.get(id=contrato['obra'])
            contrato['estado_name'] = status.nombre
            contrato['obra_name'] = obra.nombre
        
        return JsonResponse({'total_pages': total_pages, 'total_objects':count_objects, 'actual_page': out_pag, 'objects': response_data}, status=200)