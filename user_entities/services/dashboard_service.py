from ..serializers import dashboard_serializer
from rest_framework.response import Response
from rest_framework import status
from ..models import Doctor, Chemist, LabUser


def get_count():
    data = {'doctor': Doctor.objects.all().count(),
            'chemist': Chemist.objects.all().count(),
            'lab': LabUser.objects.all().count(),
            }
    ser = dashboard_serializer.CountingSerializer(data=data)
    if ser.is_valid():
        return ser.data


def get_dashboard():
    count = get_count()
    data = {'counts': count}
    ser = dashboard_serializer.DashBoardSerializer(data=data)
    if ser.is_valid():
        return Response(ser.data, status=status.HTTP_200_OK)
    return Response(ser.errors)
