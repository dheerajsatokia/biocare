from ..models import Patient
from ..serializers.patient_serializer import PatientSerializer, PatientPostSerializer, PatientPutSerializer
from rest_framework.response import Response
from rest_framework import status


def get_patient(pk=None):
    if pk:
        try:
            patient = Patient.objects.get(pk=pk)
            ser = PatientSerializer(patient)
            return Response(ser.data, status=status.HTTP_200_OK)
        except Patient.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        ser = PatientSerializer(Patient.objects.all(), many=True)
        return Response(ser.data, status=status.HTTP_200_OK)


def create_patient(data):
    ser = PatientPostSerializer(data=data)
    if ser.is_valid():
        patient = ser.create(ser.validated_data)
        return Response(PatientSerializer(patient).data, status=status.HTTP_201_CREATED)
    else:
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


def update_patient(data, pk=None):
    if not pk:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    try:
        patient = Patient.objects.get(pk=pk)
        ser = PatientPutSerializer(data=data)
    except Patient.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    if ser.is_valid():
        updated_patient = (ser.update(patient, ser.validated_data))
        return Response(PatientSerializer(updated_patient).data, status=status.HTTP_200_OK)
    else:
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


def delete_patient(pk=None):
    if pk:
        try:
            patient = Patient.objects.get(pk=pk)
            patient.user.address.delete()
            patient.user.delete()
            patient.delete()
            return Response(status=status.HTTP_200_OK)
        except Patient.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
