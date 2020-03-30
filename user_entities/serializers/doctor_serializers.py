from rest_framework import serializers
from ..models import Doctor
from user.serializer import AuthSerializer
from rest_framework.validators import UniqueValidator
from user.models import User


class DoctorSerializer(serializers.ModelSerializer):
    user = AuthSerializer.UserSerializer()

    class Meta:
        model = Doctor
        fields = '__all__'


class DoctorPostSerializer(serializers.ModelSerializer):
    user = serializers.CharField(required=False)
    username = serializers.CharField(required=True, max_length=255,
                                     validators=[UniqueValidator(queryset=User.objects.all())])
    confirm_password = serializers.CharField(max_length=255, required=True)
    password = serializers.CharField(max_length=255, required=True)
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    first_name = serializers.CharField(max_length=50, required=True)
    last_name = serializers.CharField(max_length=50, required=True)
    mobile_number = serializers.IntegerField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = Doctor
        fields = '__all__'

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'],
                                   email=validated_data['email'], first_name=validated_data['first_name'],
                                   last_name=validated_data['last_name'], mobile_number=validated_data['mobile_number'])
        user.set_password(validated_data['password'])
        user.save()
        doctor = Doctor.objects.create(user=user)
        return doctor


class DoctorPutSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(max_length=50, required=True)
    last_name = serializers.CharField(max_length=50, required=True)
    mobile_number = serializers.IntegerField(required=True)

    class Meta:
        model = Doctor
        fields = ['id', 'email', 'mobile_number', 'first_name', 'last_name', 'kyc_doc1', 'kyc_doc2', 'is_kyc_approved']

    def update(self, instance, validated_data):
        user = instance.user
        user.email = validated_data.get('email')
        user.mobile_number = validated_data.get('mobile_number')
        user.first_name = validated_data.get('first_name')
        user.last_name = validated_data.get('last_name')
        user.save()
        instance.kyc_doc1 = validated_data.get('kyc_doc1')
        instance.kyc_doc2 = validated_data.get('kyc_doc2')
        instance.is_kyc_approved = validated_data.get('is_kyc_approved')

        return instance
