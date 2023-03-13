
from hgi_static.models import GestionCambios
from hgi_static.serializer import GestionCambiosSerializer
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

class GestionCambiosViewSet(viewsets.ModelViewSet):
    queryset = GestionCambios.objects.all()
    authentication_classes = ()
    permission_classes = [permissions.AllowAny,]
    serializer_class = GestionCambiosSerializer
    http_method_names = ["get", "patch", "post"]

    def retrieve(self, request, pk):
        self.queryset = GestionCambios.objects.all()
        gestion_cambio = self.get_object()
        gestion_cambio_data = self.serializer_class(gestion_cambio).data
        return JsonResponse({"gestion_cambio":gestion_cambio_data}, status=200)
    
    def get_queryset(self):
        self.get_queryset = GestionCambios.objects.all().order_by("-fecha")
        gestion_cambios = self.queryset

        if 'id' in self.request.query_params.keys():
            id = self.request.query_params['id']
        else:
            return gestion_cambios
        
        if 'contrato' in self.request.query_params.keys():
            contrato = self.request.query_params['contrato']
            gestion_cambios = gestion_cambios.filter(type_model = "Contrato").filter(obj_id=id)
        
        elif 'obra' in self.request.query_params.keys():
            obra = self.request.query_params['obra']
            gestion_cambios = gestion_cambios.filter(type_model = "Obra").filter(obj_id=id)
        
        elif 'oc' in self.request.query_params.keys():
            obra = self.request.query_params['oc']
            gestion_cambios = gestion_cambios.filter(type_model = "Oc").filter(obj_id=id)
        
        elif 'cliente' in self.request.query_params.keys():
            cliente = self.request.query_params['cliente']
            gestion_cambios = gestion_cambios.filter(type_model = "Cliente").filter(obj_id=id)
        
        elif 'proveedor' in self.request.query_params.keys():
            proveedor = self.request.query_params['proveedor']
            gestion_cambios = gestion_cambios.filter(type_model = "Proveedor").filter(obj_id=id)
        
        elif 'cajachica' in self.request.query_params.keys():
            caja_chica = self.request.query_params['cajachica']
            gestion_cambios = gestion_cambios.filter(type_model = "CajaChica").filter(obj_id=id)
        
        elif 'presupuesto' in self.request.query_params.keys():
            presupuesto = self.request.query_params['presupuesto']
            gestion_cambios = gestion_cambios.filter(type_model = "Presupuesto").filter(obj_id=id)
        
        elif 'prodrecurso' in self.request.query_params.keys():
            prodrecurso = self.request.query_params['prodrecurso']
            gestion_cambios = gestion_cambios.filter(type_model = "ProdRecurso").filter(obj_id=id)
        
        elif 'itemcc' in self.request.query_params.keys():
            itemcc = self.request.query_params['itemcc']
            gestion_cambios = gestion_cambios.filter(type_model = "ItemCC").filter(obj_id=id)
        
        elif 'itemrecurso' in self.request.query_params.keys():
            itemrecurso = self.request.query_params['itemrecurso']
            gestion_cambios = gestion_cambios.filter(type_model = "ItemRecurso").filter(obj_id=id)
        
        elif 'productooc' in self.request.query_params.keys():
            productooc = self.request.query_params['productooc']
            gestion_cambios = gestion_cambios.filter(type_model = "ProductoOc").filter(obj_id=id)
        
        return gestion_cambios

    def list(self, request):
        gestion_cambio = self.get_queryset()
        pages = Paginator(gestion_cambio, 99999)
        out_pag = 1
        total_pages = pages.num_pages
        count_objects = pages.count
        if self.request.query_params.keys():
            if 'page' in self.request.query_params.keys():
                page_asked = int(self.request.query_params['page'])
                if page_asked in pages.page_range:
                    out_pag = page_asked
        gestion_cambio_all = pages.page(out_pag).object_list
        serializer = self.serializer_class(gestion_cambio_all, many=True)
        response_data = serializer.data
        
        return JsonResponse({'total_pages': total_pages, 'total_objects':count_objects, 'actual_page': out_pag, 'objects': response_data}, status=200)