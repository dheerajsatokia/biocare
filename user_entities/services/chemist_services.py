from ..models import Chemist
from ..serializers import chemist_serializer
from rest_framework.response import Response
from rest_framework import status


def get_chemist(pk=None):
    if pk:
        try:
            chemist = Chemist.objects.get(pk=pk)
            ser = chemist_serializer.ChemistSerializer(chemist)
            return Response(ser.data, status=status.HTTP_200_OK)
        except Chemist.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        ser = chemist_serializer.ChemistSerializer(Chemist.objects.all(), many=True)
        return Response(ser.data, status=status.HTTP_200_OK)


def create_chemist(data):
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
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


def update_chemist(data, pk=None):
    # user = get_object_or_404(User, id=pk)
    if not pk:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    try:
        chemist = Chemist.objects.get(pk=pk)
    except Chemist.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = chemist_serializer.ChemistPutSerializer(data=data)
    if serializer.is_valid():
        updated_chemist = serializer.update(chemist, serializer.validated_data)
        return Response(chemist_serializer.ChemistSerializer(updated_chemist).data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
