from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from ..models import User, ForgetPasswordToken
from ..serializer.AuthSerializer import CustomJWTSerializer, UserRegisterSerializer, UserSerializer, \
    ForgetPasswordSerializer, UserPutSerializer


def Login(data):
    serializer = CustomJWTSerializer(data=data)
    if serializer.is_valid():
        token = serializer.object.get('token')
        user = serializer.object.get('user')
        data = {"token": token}
        data['user'] = UserSerializer(user).data
        return Response(data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def Register(data):
    serializer = UserRegisterSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        user = serializer.instance
        user.set_password(serializer.validated_data['password'])
        user.is_active = True
        user.save()
        userserializer = UserSerializer(user)
        return Response(userserializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_user(pk=None):
    if pk:
        user = get_object_or_404(User, id=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        serializer = UserSerializer(User.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


def update_user(data, pk=None):
    # user = get_object_or_404(User, id=pk)
    user = User.objects.get(pk=pk)
    serializer = UserPutSerializer(data=data)
    if serializer.is_valid():
        updated_user = serializer.update(user, serializer.validated_data)
        return Response(UserSerializer(updated_user).data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def delete_user(pk=None):
    if pk:
        try:
            User.objects.get(pk=pk).delete()
            return Response(status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


def forget_password_token(data):
    ser = ForgetPasswordSerializer(data=data)
    if ser.is_valid():
        payload = 'http://127.0.0.1:8000/user/forget-password/' + ser.create_token()
        return Response(payload, status=status.HTTP_200_OK)
    else:
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


def verity_forget_password_token(token):
    db_token = None
    try:
        db_token = ForgetPasswordToken.objects.get(token=token)
    except ForgetPasswordToken.DoesNotExist:
        return Response({'error': 'Token is not valid'})

    if db_token.is_valid():
        return Response(status=200)
    else:
        return Response({'error': 'Token is expired'})
