from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from user.serializer.AuthSerializer import UserSerializer
from .models import User
from .services.auth_services import Login, Register, get_user, forget_passeord_token, verity_forget_password_token


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['POST'])
def Loginview(request):
    return Login(data=request.data)


@api_view(['POST'])
def Registerview(request):
    return Register(data=request.data)


class UserView(APIView):
    def get(self, request, pk=None):
        return get_user(pk)


class ForgetPassword(APIView):
    def post(self, request):
        return forget_passeord_token(data=request.data)

    def get(self, request, token):
        return verity_forget_password_token(token)
