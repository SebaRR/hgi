from django.utils import timezone
from django.shortcuts import render
from hgi_users.serializer import UserSerializer
from hgi_users.models import User
from hgi_users.serializer import CreateUserSerializer, UserTokenSerializer
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
from rest_framework import viewsets




class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    authentication_classes = ()
    permission_classes = []
    serializer_class = UserSerializer
    http_method_names = ["get", "patch", "delete"]


    def retrieve(self, request, pk):
        self.queryset = User.objects.all()
        user = self.get_object()
        data_user = self.serializer_class(user).data
        if request.user.id == data_user["id"]:
            if request.user.last_name is not None:
                data_user["last_name"] = request.user.first_last_name
            else:
                data_user["last_name"] = " "
        return JsonResponse({"user":data_user}, status=200)


    def partial_update(self, request, pk, *args, **kwargs):
        self.queryset = User.objects.all()
        user = self.get_object()
        edited = timezone.now()
        user.updated_at = edited
        user.save()
        serializer = self.serializer_class(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data_user = serializer.data
            return JsonResponse({"status_text": "Usuario editado con exito.", "user": data_user,},status=202)
        else:
            return JsonResponse({"status_text": str(serializer.errors)}, status=400)



@csrf_exempt
@api_view(["POST"])
def register(request):
    try:
        data = json.loads(request.body)
    except JSONDecodeError as error:
        return JsonResponse({
                "status_text": "Error parsing body: maybe a trailing comma?",
                "error": str(error),
            },status=400,)

    data["email"] = data["email"].lower()
    serializer = CreateUserSerializer(data=data)
    if serializer.is_valid():
        instance, token = serializer.save()
        data_user = serializer.data
        token = str(token).replace("(<Token: ", "").replace(">, True)", "")
        data_user["oauth_token"] = token
        data = {"token": token, "user": data_user["id"], "validation": True}
        validation_token = UserTokenSerializer(data=data)
        if validation_token.is_valid():
            validation_token.save()
            return JsonResponse({"status_text": "Usuario creado con exito.", "user": data_user,},status=202)
    return JsonResponse({"status_text": str(serializer.errors)}, status=400)


@csrf_exempt
@api_view(["POST"])
def login(request):
    data = json.loads(request.body)
    if ("username" in data.keys()) and ("password" in data.keys()):
        user = User.objects.get(username=data["username"].lower())
        if user:
            if user.check_password(data["password"]):
                user = user
                serializer = UserSerializer(user)
                token = serializer.get_token()
                serializer = serializer.data
                serializer['token'] = str(token)
                return JsonResponse({"user":serializer}, status=202)
            return JsonResponse({"status_text": "Contraseña incorrecta"}, status=403)
        return JsonResponse({"status_text": "El usuario no existe"}, status=403)
    return JsonResponse({"status_text": "No se enviaron los parametros correctos"}, status=403)


@csrf_exempt
@api_view(["POST"])
def logout(request):
    request.user.auth_token.delete()
    logout(request)
    return JsonResponse({"status_text" : "Sesión cerrada con exito."}, status=202)