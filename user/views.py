from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from user.serializer.AuthSerializer import UserSerializer
from .models import User
from .services.auth_services import Login, Register, get_user, forget_password_token, verity_forget_password_token, \
    delete_user, update_user


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['POST'])
def Loginview(request):
    return Login(data=request.data)


class UserView(APIView):
    def get(self, request, pk=None):
        return get_user(pk)

    def post(self, request):
        return Register(data=request.data)

    def put(self, request, pk=None):
        return update_user(data=request.data, pk=pk)

    def delete(self, request, pk=None):
        return delete_user(pk)


class ForgetPassword(APIView):
    def post(self, request):
        return forget_password_token(data=request.data)

    def get(self, request, token):
        return verity_forget_password_token(token)
