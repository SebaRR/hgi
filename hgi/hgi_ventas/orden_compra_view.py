
from hgi_static.serializer import ContratoSerializer
from hgi_static.models import Contrato
from hgi.utils import get_user_from_usertoken, user_can_see_oc, can_accept_oc
from hgi_ventas.models import OrdenCompra
from hgi_ventas.serializer import OrdenCompraSerializer
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


class OrdenCompraViewSet(viewsets.ModelViewSet):
    queryset = OrdenCompra.objects.all()
    authentication_classes = ()
    permission_classes = [permissions.AllowAny,]
    serializer_class = OrdenCompraSerializer
    http_method_names = ["get", "patch", "delete", "post"]

    def retrieve(self, request, pk):
        self.queryset = OrdenCompra.objects.all()
        ppto = self.get_object()
        data_ppto = self.serializer_class(ppto).data
        return JsonResponse({"orden_compra":data_ppto}, status=200)
    
    def get_queryset(self):
        self.get_queryset = OrdenCompra.objects.all()
        oc = self.queryset
        if 'proveedor' in self.request.query_params.keys():
            proveedor = self.request.query_params['proveedor']
            oc = oc.filter(proveedor = proveedor)
            
        return oc
    
    def list(self, request):

        if 'Authorization' in request.headers:
            user = get_user_from_usertoken(request.headers['Authorization'])
        else:
            return JsonResponse ({'status_text':'No usaste token'}, status=403)

        ocs = self.get_queryset()
        final_oc_list = []

        if ocs.count() == 0:
            return JsonResponse ({"total_pages": 0,"total_objects": 0,"actual_page": 0,"objects": [],},status=200,)
        
        for oc in ocs.reverse():
            if user_can_see_oc(user, oc):
                final_oc_list.append(oc)

        pages = Paginator(final_oc_list, 20)
        out_pag = 1
        total_pages = pages.num_pages
        count_objects = pages.count
        if self.request.query_params.keys():
            if "page" in self.request.query_params.keys():
                page_asked = int(self.request.query_params["page"])
                if page_asked in pages.page_range:
                    out_pag = page_asked
        oc_list = pages.page(out_pag).object_list
        serializer = self.serializer_class(oc_list, many=True)
        response_data = serializer.data
        #for oc in response_data:

        return JsonResponse (
            {
                "total_pages": total_pages,
                "total_objects": count_objects,
                "actual_page": out_pag,
                "objects": response_data,
            },status=200,)
    
    def create(self, request):

        try:
            data = json.loads(request.body)
        except JSONDecodeError as error:
            return JsonResponse({'Request error': str(error)},status=400)
        
        if 'Authorization' in request.headers:
            user = get_user_from_usertoken(request.headers['Authorization'])
        else:
            return JsonResponse ({'status_text':'No usaste token'}, status=403)

        data['creador'] = user
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            oc_serializer = serializer.data
            return JsonResponse({"oc":oc_serializer}, status=201)
        return JsonResponse({'status_text':str(serializer.errors)}, status=201)

    def partial_update(self, request, *args, **kwargs):
        
        if 'Authorization' in request.headers:
            user = get_user_from_usertoken(request.headers['Authorization'])
        else:
            return JsonResponse ({'status_text':'No usaste token'}, status=403)

        self.queryset = OrdenCompra.objects.all()
        oc = self.get_object()
        contrato = oc.contrato
        can_accept, list_produtcs = can_accept_oc(oc)
        if 'auto_a' in request.data.keys() or 'auto_r' in request.data.keys():
            if (contrato.administrador.id == user.id or contrato.visitador == user.id) and contrato.responsable.id == user.id:
                if can_accept:
                    serializer = OrdenCompraSerializer(oc, data={"autorizacion_adm": True, "autorizacion_res": True, "estado": 7}, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        return Response({'oc_data':serializer.data,'products':list_produtcs}, status=status.HTTP_202_ACCEPTED)
                    else:
                        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return JsonResponse ({'status_text':'La partida no acepta ese gasto.','products':list_produtcs}, status=403)
        if 'auto_a' in request.data.keys():
            if contrato.administrador.id == user.id or contrato.visitador == user.id:
                if can_accept:
                    if oc.autorizacion_res:
                        serializer = OrdenCompraSerializer(oc, data={"autorizacion_adm": True, "estado": 7}, partial=True)
                    else:
                        serializer = OrdenCompraSerializer(oc, data={"autorizacion_adm": True}, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        oc_data = serializer.data
                        return Response({'oc_data':oc_data,'products':list_produtcs}, status=status.HTTP_202_ACCEPTED)
                    else:
                        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return JsonResponse ({'status_text':'La partida no acepta ese gasto.','products':list_produtcs}, status=403)
            else:
                return JsonResponse ({'status_text':'No tienes autorización para realizar esta acción.'}, status=403)
        elif 'auto_r' in request.data.keys():
            if contrato.responsable.id == user.id:
                if can_accept:
                    if oc.autorizacion_adm:
                        serializer = OrdenCompraSerializer(oc, data={"autorizacion_adm": True, "estado": 7}, partial=True)
                    else:
                        serializer = OrdenCompraSerializer(oc, data={"autorizacion_res": True}, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        oc_data = serializer.data
                        return Response({'oc_data':oc_data,'products':list_produtcs}, status=status.HTTP_202_ACCEPTED)
                    else:
                        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return JsonResponse ({'status_text':'La partida no acepta ese gasto.','products':list_produtcs}, status=403)
            else:
                return JsonResponse ({'status_text':'No tienes autorización para realizar esta acción.'}, status=403)
        else:
            serializer = OrdenCompraSerializer(oc, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            else:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        

        