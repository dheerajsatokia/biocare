from django.shortcuts import render
from rest_framework.views import APIView
from .services import doctor_services, chemist_services, lab_user_services, dashboard_service, patient_services
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action, permission_classes as permission_decorator
from rest_framework.response import Response


# Create your views here.
class DoctorView(APIView):
    # permission_classes = [IsAuthenticated, ]

    def get(self, request, pk=None):
        return doctor_services.get_doctor(pk)

    @permission_decorator((IsAuthenticated,))
    def post(self, request):
        return doctor_services.create_doctor(request.data)

    def delete(self, request, pk=None):
        return doctor_services.delete_doctor(pk)

    def put(self, request, pk=None):
        return doctor_services.update_doctor(data=request.data, pk=pk)


class ChemistView(APIView):
    permission_classes = [AllowAny, ]

    def get(self, request, pk=None):
        return chemist_services.get_chemist(pk)

    def post(self, request):
        return chemist_services.create_chemist(request.data)

    def delete(self, request, pk=None):
        return chemist_services.delete_chemist(pk)

    def put(self, request, pk=None):
        return chemist_services.update_chemist(data=request.data, pk=pk)


class LabUserView(APIView):
    permission_classes = [AllowAny, ]

    def get(self, request, pk=None):
        return lab_user_services.get_lab_user(pk)

    def post(self, request):
        return lab_user_services.create_lab_user(request.data)

    def delete(self, request, pk=None):
        return lab_user_services.delete_lab_user(pk)

    def put(self, request, pk=None):
        return lab_user_services.update_lab_user(data=request.data, pk=pk)


class DashBoard(APIView):
    def get(self, request):
        return dashboard_service.get_dashboard()


class PatientView(APIView):
    permission_classes = [AllowAny, ]

    def get(self, request, pk=None):
        return patient_services.get_patient(pk)

    def post(self, request):
        return patient_services.create_patient(request.data)

    def put(self, request, pk=None):
        return patient_services.update_patient(data=request.data, pk=pk)

    def delete(self, request, pk=None):
        return patient_services.delete_patient(pk)
