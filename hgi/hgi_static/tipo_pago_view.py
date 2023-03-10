
from hgi.utils import get_user_from_usertoken
from hgi_static.serializer import TipoPagoSerializer
from hgi_static.models import TipoPago
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


class TipoPagoViewSet(viewsets.ModelViewSet):
    queryset = TipoPago.objects.all()
    authentication_classes = ()
    permission_classes = [permissions.AllowAny,]
    serializer_class = TipoPagoSerializer
    http_method_names = ["get", "patch", "delete", "post"]

    def retrieve(self, request, pk):
        self.queryset = TipoPago.objects.all()
        ppto = self.get_object()
        data_ppto = self.serializer_class(ppto).data
        return JsonResponse({"tipo_pago":data_ppto}, status=200)
    
    def create(self, request):
        try:
            data = json.loads(request.body)
        except JSONDecodeError as error:
            return JsonResponse({'Request error': str(error)},status=400)
        if "creador" not in data.keys():
            if 'Authorization' in request.headers:
                user = get_user_from_usertoken(request.headers['Authorization'])
                data['creador'] = user.id
            else:
                return JsonResponse ({'status_text':'No usaste token'}, status=403)
        serializer = self.serializer_class(data = data)
        if serializer.is_valid():
            serializer.save()
            tipo_pago_data = serializer.data
            response = {'tipo_pago': tipo_pago_data}
            return JsonResponse(response, status=201)
        return JsonResponse({'status_text': str(serializer.errors)}, status=400)