from ..models import Doctor, Chemist
from ..serializers import doctor_serializers
from rest_framework.response import Response
from rest_framework import status


# def get_doctors():
#     doctors = Doctor.objects.all()
#     ser = doctor_serializers.DoctorSerializer(doctors, many=True)
#     return Response(ser.data)


def get_doctor(pk):
    if pk:
        doctor = Doctor.objects.get(pk=pk)
        ser = doctor_serializers.DoctorSerializer(doctor)
        return Response(ser.data, status=status.HTTP_200_OK)
    else:
        ser = doctor_serializers.DoctorSerializer(Doctor.objects.all(), many=True)
        return Response(ser.data, status=status.HTTP_200_OK)


def create_doctor(data):
    ser = doctor_serializers.DoctorPostSerializer(data=data)
    if ser.is_valid():
        doctor = ser.create(ser.validated_data)
        return Response(doctor_serializers.DoctorSerializer(doctor).data, status=status.HTTP_201_CREATED)
    else:
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


def delete_doctor(pk=None):
    if pk:
        try:
            Doctor.objects.get(pk=pk).delete()
            return Response(status=status.HTTP_200_OK)
        except Doctor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)



