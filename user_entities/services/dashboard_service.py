from ..serializers import dashboard_serializer
from rest_framework.response import Response
from ..models import Doctor, Chemist, LabUser
from ..serializers import doctor_serializers, chemist_serializer, lab_user_serializer
import json


def get_count():
    data = {'doctor': Doctor.objects.filter(is_kyc_approved=True).count(),
            'chemist': Chemist.objects.filter(is_kyc_approved=True).count(),
            'lab': LabUser.objects.filter(is_kyc_approved=True).count(),
            }
    ser = dashboard_serializer.CountingSerializer(data=data)
    if ser.is_valid():
        return ser.data


def doctor_pending_approval():
    doctors = Doctor.objects.filter(is_kyc_approved=False)
    doctors = doctor_serializers.DoctorSerializer(doctors, many=True).data

    chemist_obj = Chemist.objects.filter(is_kyc_approved=False)
    chemist = chemist_serializer.ChemistSerializer(chemist_obj, many=True).data

    labs = LabUser.objects.filter(is_kyc_approved=False)
    labs = lab_user_serializer.LabUserSerializer(labs, many=True).data

    data = {
        'doctors': doctors,
        'chemist': chemist,
        'labs': labs
    }
    json_str = json.dumps(data)
    json_data = json.loads(json_str)
    return json_data


def get_dashboard():
    count = get_count()
    data = {'counts': count, 'pending_approvals': doctor_pending_approval()}
    return Response(data)
