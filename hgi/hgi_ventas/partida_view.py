
from hgi.utils import get_user_from_usertoken
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
        pages = Paginator(partidas.order_by('inicio').reverse(), 99999)
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

    def partial_update(self, request, pk, *args, **kwargs):
        self.queryset = Partida.objects.all()
        partida = self.get_object()
        serializer = self.serializer_class(partida, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data_partida = serializer.data
            return JsonResponse({"status_text": "Partida editado con exito.", "partida": data_partida,},status=202)
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
        
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            partida_serializer = serializer.data
            return JsonResponse({"partida":partida_serializer}, status=201)
        return JsonResponse({'status_text':str(serializer.errors)}, status=201)