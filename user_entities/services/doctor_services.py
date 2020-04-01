from ..models import Doctor
from ..serializers import doctor_serializers
from rest_framework.response import Response
from rest_framework import status


# def get_doctors():
#     doctors = Doctor.objects.all()
#     ser = doctor_serializers.DoctorSerializer(doctors, many=True)
#     return Response(ser.data)


def get_doctor(pk):
    if pk:
        try:
            doctor = Doctor.objects.get(pk=pk)
            ser = doctor_serializers.DoctorSerializer(doctor)
            return Response(ser.data, status=status.HTTP_200_OK)
        except Doctor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
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
            dr = Doctor.objects.get(pk=pk)
            dr.user.address.delete()
            dr.user.delete()
            dr.delete()
            return Response(status=status.HTTP_200_OK)
        except Doctor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


def update_doctor(data, pk=None):
    # user = get_object_or_404(User, id=pk)
    if not pk:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    try:
        doctor = Doctor.objects.get(pk=pk)
    except Doctor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    ser = doctor_serializers.DoctorPutSerializer(data=data)
    if ser.is_valid():
        updated_user = ser.update(doctor, ser.validated_data)
        return Response(doctor_serializers.DoctorSerializer(updated_user).data, status=status.HTTP_200_OK)
    else:
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
