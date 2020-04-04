from rest_framework import serializers
from ..models import LabUser
from user.serializer import AuthSerializer
from rest_framework.validators import UniqueValidator
from user.models import User, Address


class LabUserSerializer(serializers.ModelSerializer):
    user = AuthSerializer.UserSerializer()

    class Meta:
        model = LabUser
        fields = '__all__'


class LabUserPostSerializer(serializers.ModelSerializer):
    user = serializers.CharField(required=False)
    username = serializers.CharField(required=True, max_length=255,
                                     validators=[UniqueValidator(queryset=User.objects.all())])
    confirm_password = serializers.CharField(max_length=255, required=True)
    password = serializers.CharField(max_length=255, required=True)
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    first_name = serializers.CharField(max_length=50, required=True)
    last_name = serializers.CharField(max_length=50, required=True)
    mobile_number = serializers.IntegerField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])

    address1 = serializers.CharField(max_length=1024)
    address2 = serializers.CharField(max_length=1024)
    zip_code = serializers.CharField(max_length=12)
    city = serializers.CharField(max_length=12)
    country = serializers.CharField(max_length=250)

    class Meta:
        model = LabUser
        fields = '__all__'

    def validate(self, data):
        if not data.get('password') or not data.get('confirm_password'):
            raise serializers.ValidationError("Please enter a password and "
                                              "confirm it.")

        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError("passwords doesn't match.")

        return data

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'],
                                   email=validated_data['email'], first_name=validated_data['first_name'],
                                   last_name=validated_data['last_name'], mobile_number=validated_data['mobile_number'])
        user.set_password(validated_data['password'])
        user.save()

        Address.objects.create(user=user,
                               address1=validated_data['address1'],
                               address2=validated_data['address2'],
                               zip_code=validated_data['zip_code'],
                               city=validated_data['city'],
                               country=validated_data['country'],
                               )
        lab_user = LabUser.objects.create(user=user)
        return lab_user


class LabUserPutSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(max_length=50, required=True)
    last_name = serializers.CharField(max_length=50, required=True)
    mobile_number = serializers.IntegerField(required=True)

    address1 = serializers.CharField(max_length=1024)
    address2 = serializers.CharField(max_length=1024)
    zip_code = serializers.CharField(max_length=12)
    city = serializers.CharField(max_length=12)
    country = serializers.CharField(max_length=250)

    class Meta:
        model = LabUser
        fields = ['id', 'email', 'first_name', 'last_name', 'mobile_number', 'kyc_lab1', 'kyc_lab2', 'is_kyc_approved',
                  'address1', 'address2', 'zip_code', 'city', 'country']

    def update(self, instance, validated_data):
        user = instance.user
        user.email = validated_data.get('email')
        user.first_name = validated_data.get('first_name')
        user.last_name = validated_data.get('last_name')
        user.mobile_number = validated_data.get('mobile_number')
        user.save()

        address = user.address
        address.address1 = validated_data.get('address1')
        address.address2 = validated_data.get('address2')
        address.zip_code = validated_data.get('zip_code')
        address.city = validated_data.get('city')
        address.country = validated_data.get('country')
        address.save()

        instance.kyc_lab1 = validated_data.get('kyc_lab1')
        instance.kyc_lab2 = validated_data.get('kyc_lab2')
        instance.is_kyc_approved = validated_data.get('is_kyc_approved')

        return instance
