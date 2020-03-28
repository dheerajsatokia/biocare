from django.shortcuts import render
from rest_framework.views import APIView
from .services import doctor_services, chemist_services, lab_user_services


# Create your views here.
class DoctorView(APIView):
    def get(self, request, pk=None):
        return doctor_services.get_doctor(pk)

    def post(self, request):
        return doctor_services.create_doctor(request.data)

    def delete(self, request, pk=None):
        return doctor_services.delete_doctor(pk)


class ChemistView(APIView):
    def get(self, request, pk=None):
        return chemist_services.get_chemist(pk)

    def post(self, request):
        return chemist_services.create_doctor(request.data)

    def delete(self, request, pk=None):
        return chemist_services.delete_chemist(pk)


class LabUserView(APIView):
    def get(self, request, pk=None):
        return lab_user_services.get_lab_user(pk)

    def post(self, request):
        return lab_user_services.create_lab_user(request.data)

    def delete(self, request, pk=None):
        return lab_user_services.delete_lab_user(pk)
