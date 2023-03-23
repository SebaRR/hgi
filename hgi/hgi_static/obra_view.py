from hgi.utils import get_changes_list
from hgi.utils import register_change
from hgi.utils import get_user_from_usertoken
from hgi_users.models import Client
from hgi_static.models import Obra
from hgi_static.serializer import ObraSerializer
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


class ObraViewSet(viewsets.ModelViewSet):
    queryset = Obra.objects.all()
    authentication_classes = ()
    permission_classes = [permissions.AllowAny,]
    serializer_class = ObraSerializer
    http_method_names = ["get", "patch", "delete", "post"]

    def retrieve(self, request, pk):
        self.queryset = Obra.objects.all()
        obra = self.get_object()
        data_obra = self.serializer_class(obra).data
        client = Client.objects.get(id=data_obra['cliente'])
        data_obra['client_name'] = client.business_name
        return JsonResponse({"obra":data_obra}, status=200)
    
    def get_queryset(self, user):
        if user.empresa is not None:
            queryset = Obra.objects.filter(empresa=user.empresa)
        else:
            queryset = Obra.objects.all()
        print(user.empresa.id)
        obras = queryset

        if 'empresa' in self.request.query_params.keys():
            empresa = self.request.query_params['empresa']
            obras = obras.filter(empresa = empresa) 
        
        return obras
    
    def list(self, request):
        user = get_user_from_usertoken(request.headers["Authorization"])
        obras = self.get_queryset(user)
        pages = Paginator(obras.order_by('fecha').reverse(), 99999)
        out_pag = 1
        total_pages = pages.num_pages
        count_objects = pages.count
        if self.request.query_params.keys():
            if 'page' in self.request.query_params.keys():
                page_asked = int(self.request.query_params['page'])
                if page_asked in pages.page_range:
                    out_pag = page_asked
        obras_all = pages.page(out_pag).object_list
        serializer = self.serializer_class(obras_all, many=True)
        response_data = serializer.data
        for obra in response_data:
            client = Client.objects.get(id=obra['cliente'])
            obra['client_name'] = client.business_name
        
        return JsonResponse({'total_pages': total_pages, 'total_objects':count_objects, 'actual_page': out_pag, 'objects': response_data}, status=200)
    
    def create(self, request):
        try:
            data = json.loads(request.body)
        except JSONDecodeError as error:
            return JsonResponse({'Request error': str(error)},status=400)
        
        if 'Authorization' in request.headers:
            user = get_user_from_usertoken(request.headers['Authorization'])
            if "creador" not in data.keys():
                data['creador'] = user.id
        else:
            return JsonResponse ({'status_text':'No usaste token'}, status=403)
        
        serializer = self.serializer_class(data = data)
        if serializer.is_valid():
            serializer.save()
            obra_data = serializer.data
            register_change(obra_data["id"],[1,],user,"Obra")
            response = {'obra': obra_data}
            return JsonResponse(response, status=201)
        return JsonResponse({'status_text': str(serializer.errors)}, status=400)
    
    def partial_update(self, request, pk, *args, **kwargs):
        self.queryset = Obra.objects.all()
        obra = self.get_object()

        if 'Authorization' in request.headers:
            user = get_user_from_usertoken(request.headers['Authorization'])
        else:
            return JsonResponse ({'status_text':'No usaste token'}, status=403)
        
        serializer = self.serializer_class(obra, data=request.data, partial=True)
        changes = get_changes_list(request.data)
        if serializer.is_valid():
            serializer.save()
            obra_data = serializer.data
            register_change(obra_data["id"],changes,user,"Obra")
            return JsonResponse({"status_text": "Obra editada con exito.", "obra": obra_data,},status=202)
        else:
            return JsonResponse({"status_text": str(serializer.errors)}, status=400)
        
    def destroy(self, request, *args, **kwargs):
        self.queryset = Obra.objects.all()
        obra = self.get_object()
        if obra is not None:
            obra.delete()
            return JsonResponse({'status_text': 'Obra eliminada correctamente'}, status=200)

