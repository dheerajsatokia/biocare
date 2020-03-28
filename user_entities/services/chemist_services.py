from ..models import Chemist
from ..serializers import chemist_serializer
from rest_framework.response import Response
from rest_framework import status


def get_chemist(pk=None):
    if pk:
        chemist = Chemist.objects.get(pk=pk)
        ser = chemist_serializer.ChemistSerializer(chemist)
        return Response(ser.data, status=status.HTTP_200_OK)
    else:
        ser = chemist_serializer.ChemistSerializer(Chemist.objects.all(), many=True)
        return Response(ser.data, status=status.HTTP_200_OK)


def create_doctor(data):
    ser = chemist_serializer.ChemistPostSerializer(data=data)
    if ser.is_valid():
        chemist = ser.create(ser.validated_data)
        return Response(chemist_serializer.ChemistSerializer(chemist).data, status=status.HTTP_201_CREATED)
    else:
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


def delete_chemist(pk=None):
    if pk:
        try:
            Chemist.objects.get(pk=pk).delete()
            return Response(status=status.HTTP_200_OK)
        except Chemist.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
