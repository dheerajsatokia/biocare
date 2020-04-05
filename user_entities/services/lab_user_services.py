from ..models import LabUser
from ..serializers import lab_user_serializer
from rest_framework.response import Response
from rest_framework import status


# def get_doctors():
#     doctors = Doctor.objects.all()
#     ser = doctor_serializers.DoctorSerializer(doctors, many=True)
#     return Response(ser.data)


def get_lab_user(pk):
    if pk:
        lab_user = LabUser.objects.get(pk=pk)
        ser = lab_user_serializer.LabUserSerializer(lab_user)
        return Response(ser.data, status=status.HTTP_200_OK)
    else:
        ser = lab_user_serializer.LabUserSerializer(LabUser.objects.filter(is_kyc_approved=True), many=True)
        return Response(ser.data, status=status.HTTP_200_OK)


def create_lab_user(data):
    ser = lab_user_serializer.LabUserPostSerializer(data=data)
    if ser.is_valid():
        lab_user = ser.create(ser.validated_data)
        return Response(lab_user_serializer.LabUserSerializer(lab_user).data, status=status.HTTP_201_CREATED)
    else:
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


def delete_lab_user(pk=None):
    if pk:
        try:
            LabUser.objects.get(pk=pk).delete()
            return Response(status=status.HTTP_200_OK)
        except LabUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


def update_lab_user(data, pk=None):
    # user = get_object_or_404(User, id=pk)
    if not pk:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    try:
        lab_user = LabUser.objects.get(pk=pk)
    except LabUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    ser = lab_user_serializer.LabUserPutSerializer(data=data)
    if ser.is_valid():
        updated_user = ser.update(lab_user, ser.validated_data)
        return Response(lab_user_serializer.LabUserSerializer(updated_user).data, status=status.HTTP_200_OK)
    else:
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


def approve_lab(data):
    if not 'id' in data:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    try:
        lab = LabUser.objects.get(id=data['id'])
        lab.is_kyc_approved = True
        lab.save()
        return Response(status=status.HTTP_200_OK)
    except LabUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
