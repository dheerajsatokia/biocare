from ..models import Doctor
from ..serializers import doctor_serializers
from rest_framework.response import Response
from rest_framework import status


def get_doctors():
    doctors = Doctor.objects.all()
    ser = doctor_serializers.DoctorSerializer(doctors, many=True)
    return Response(ser.data)


def create_doctor(data):
    ser = doctor_serializers.DoctorPostSerializer(data=data)
    if ser.is_valid():
        doctor = ser.create(ser.validated_data)
        return Response(doctor_serializers.DoctorSerializer(doctor).data, status=status.HTTP_201_CREATED)
    else:
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


def delete_doctor(pk=None):
    pass
