from rest_framework import serializers
from ..models import Chemist
from user.serializer import AuthSerializer
from rest_framework.validators import UniqueValidator
from user.models import User


class ChemistSerializer(serializers.ModelSerializer):
    user = AuthSerializer.UserSerializer()

    class Meta:
        model = Chemist
        fields = '__all__'


class ChemistPostSerializer(serializers.ModelSerializer):
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
        model = Chemist
        fields = '__all__'

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'],
                                   email=validated_data['email'], first_name=validated_data['first_name'],
                                   last_name=validated_data['last_name'], mobile_number=validated_data['mobile_number'])
        user.set_password(validated_data['password'])
        user.save()
        chemist = Chemist.objects.create(user=user)
        return chemist


class ChemistPutSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(max_length=50, required=True)
    last_name = serializers.CharField(max_length=50, required=True)
    mobile_number = serializers.IntegerField(required=True)

    class Meta:
        model = Chemist
        fields = ['id', 'email', 'first_name', 'last_name', 'mobile_number', 'kyc_chem1', 'kyc_chem2', 'is_kyc_approved']

    def update(self, instance, validated_data):
        user = instance.user
        user.email = validated_data['email']
        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']
        user.mobile_number = validated_data['mobile_number']
        user.save()
        instance.kyc_chem1 = validated_data['kyc_chem1']
        instance.kyc_chem2 = validated_data['kyc_chem2']
        instance.is_kyc_approved = validated_data['is_kyc_approved']

        return instance
