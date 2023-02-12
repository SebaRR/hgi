
from hgi_static.models import Contrato, EstadoOC, Moneda, TipoPago
from hgi_users.models import User
from hgi_ventas.models import TipoOC
from hgi_ventas.serializer import OrdenCompraSerializer
from hgi_users.models import Proveedor
from hgi_ventas.models import OrdenCompra
from hgi_ventas.models import CajaChica
from hgi_ventas.serializer import CajaChicaSerializer
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

class CajaChicaViewSet(viewsets.ModelViewSet):
    queryset = CajaChica.objects.all()
    authentication_classes = ()
    permission_classes = [permissions.AllowAny,]
    serializer_class = CajaChicaSerializer
    http_method_names = ["get", "patch", "delete", "post"]

    def retrieve(self, request, pk):
        self.queryset = CajaChica.objects.all()
        caja = self.get_object()
        data_caja = self.serializer_class(caja).data
        data_caja['nombre_estado'] = caja.estado.estado
        data_caja['nombre_creador'] = caja.creador.short_name()
        data_caja['nombre_contrato'] = caja.contrato.nombre
        return JsonResponse({"caja_chica":data_caja}, status=200)
    
    def get_queryset(self):
        self.get_queryset = CajaChica.objects.all()
        cajas = self.queryset

        if 'contrato' in self.request.query_params.keys():
            contrato = self.request.query_params['contrato']
            cajas = cajas.filter(contrato = contrato)
        
        if 'oc' in self.request.query_params.keys():
            oc = self.request.query_params['oc']
            cajas = cajas.filter(oc = oc)
            
        return cajas

    def list(self, request):
        cajas = self.get_queryset()
        pages = Paginator(cajas.order_by('fecha').reverse(), 25)
        out_pag = 1
        total_pages = pages.num_pages
        count_objects = pages.count
        if self.request.query_params.keys():
            if 'page' in self.request.query_params.keys():
                page_asked = int(self.request.query_params['page'])
                if page_asked in pages.page_range:
                    out_pag = page_asked
        cajas_all = pages.page(out_pag).object_list
        serializer = self.serializer_class(cajas_all, many=True)
        response_data = serializer.data
        for caja_data in response_data:
            caja = CajaChica.objects.get(id=caja_data['id'])
            caja_data['nombre_estado'] = caja.estado.estado
            caja_data['nombre_creador'] = caja.creador.short_name()
            caja_data['nombre_contrato'] = caja.contrato.nombre
        return JsonResponse({'total_pages': total_pages, 'total_objects':count_objects, 'actual_page': out_pag, 'objects': response_data}, status=200)

    def partial_update(self, request, pk, *args, **kwargs):
        self.queryset = CajaChica.objects.all()
        caja = self.get_object()
        if caja.estado.id == 1 or caja.estado.id == 6:
            if 'revision' in request.data.keys():
                del request.data['revision']
                data = request.data
                data['estado'] = 2
                serializer = self.serializer_class(caja, data=data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    data_caja = serializer.data
                    proveedor = Proveedor.objects.get(rs = 'Constructora VDZ SpA')
                    estado_oc = EstadoOC.objects.get(id=6)
                    forma_pago = TipoPago.objects.get(id=1)
                    tipo_oc = TipoOC.objects.get(id=13)
                    moneda = Moneda.objects.get(id=1)
                    contrato_oc = Contrato.objects.get(id=data_caja['contrato'])
                    emisor_oc = User.objects.get(id=data_caja['creador'])
                    creador_oc = User.objects.get(id=data_caja['creador'])
                    caja_oc = OrdenCompra.objects.create(
                        glosa='Generado por Caja Chica Id: ' + str(data_caja['id']),
                        proveedor=proveedor,
                        estado=estado_oc,
                        forma_pago=forma_pago,
                        contrato=contrato_oc,
                        emisor=emisor_oc,
                        creador=creador_oc,
                        tipo=tipo_oc,
                        moneda=moneda,
                        total=data_caja['total']
                    )
                    caja_oc_data = OrdenCompraSerializer(caja_oc).data
                    caja.oc = caja_oc.id
                    caja.save()
                    return JsonResponse({"status_text": "Caja editada con exito.", "caja": data_caja,"oc":caja_oc_data},status=202)
                else:
                    return JsonResponse({"status_text": str(serializer.errors)}, status=400)
            else:
                serializer = self.serializer_class(caja, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    data_caja = serializer.data
                    return JsonResponse({"status_text": "Caja editada con exito.", "caja": data_caja,},status=202)
                else:
                    return JsonResponse({"status_text": str(serializer.errors)}, status=400)
        else:
            return JsonResponse({"status_text": "Ya no puedes editarla."}, status=400)
        