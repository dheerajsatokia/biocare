from django.shortcuts import render
from rest_framework.views import APIView
from .services import doctor_services


# Create your views here.
class DoctorView(APIView):
    def get(self, request):
        return doctor_services.get_doctors()

    def post(self, request):
        return doctor_services.create_doctor(request.data)

    def delete(self, request):
        pass
