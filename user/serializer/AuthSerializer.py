import secrets

from django.contrib.auth import authenticate
from django.utils.translation import ugettext as _
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework_jwt.settings import api_settings

from ..models import User, ForgetPasswordToken


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(min_length=255)
    mobile_number = serializers.CharField(max_length=12)
    confirm_password = serializers.CharField(max_length=255)

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'],

                                        validated_data['password'], validated_data['mobile_number'])
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'mobile_number')


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class CustomJWTSerializer(JSONWebTokenSerializer):
    # TODO parameterize with env var
    username_field = 'username'
    password_field = 'password'

    def validate(self, attrs):

        password = attrs.get(self.password_field)
        user_obj = User.objects.filter(email__iexact=attrs.get(self.username_field)).first() or User.objects.filter(
            username__iexact=attrs.get(self.username_field)).first()
        if user_obj is not None:
            credentials = {
                'username': user_obj.username,
                'password': password
            }
            if all(credentials.values()):
                user = authenticate(**credentials)
                if user:
                    if not user.is_active:
                        msg = ('User account is disabled.')
                        raise serializers.ValidationError(msg)

                    payload = jwt_payload_handler(user)

                    return {
                        'token': jwt_encode_handler(payload),
                        'user': user_obj
                    }
                else:
                    msg = {"error": 'Unable to log in with provided credentials.'}
                    raise serializers.ValidationError(msg)

            else:
                msg = _('Must include "{username_field}" and "password".')
                msg = msg.format(username_field=self.username_field)
                raise serializers.ValidationError(msg)

        else:
            msg = {"error": 'Unable to log in with provided credentials.'}
            raise serializers.ValidationError(msg)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'mobile_number', 'first_name', 'last_name', 'full_name']
        # fields = '__all__'


class UserPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'mobile_number', 'first_name', 'last_name', 'full_name']


from django.core import exceptions


class UserRegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length=255, required=True)
    password = serializers.CharField(max_length=255, required=True)
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    first_name = serializers.CharField(max_length=50, required=True)
    last_name = serializers.CharField(max_length=50, required=True)
    mobile_number = serializers.IntegerField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = '__all__'

    def validate(self, attrs):
        if not attrs['password'] == attrs['confirm_password']:
            raise serializers.ValidationError('Password and Confirm Password must be same. ')
        attrs.pop('confirm_password')
        return attrs

    def validate_password(self, value):
        if value:
            errors = dict()
            try:
                import django.contrib.auth.password_validation as validators

                # validate the password and catch the exception
                validators.validate_password(password=value, user=User)

                # the exception raised here is different than serializers.ValidationError
            except exceptions.ValidationError as e:
                errors['password'] = list(e.messages)
                raise serializers.ValidationError(e)

        return value

    def create_user(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

    def save(self, **kwargs):
        super().save()


class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    username = serializers.CharField(max_length=255, required=False)

    def validate(self, attrs):
        if not attrs.get('email') and not attrs.get('username'):
            msg = _('Email or Password must not be null.')
            raise serializers.ValidationError(msg)
        user = None
        if attrs.get('email'):
            user = User.objects.filter(email__iexact=attrs.get('email')).first()
        if attrs.get('username'):
            user = User.objects.filter(username__iexact=attrs.get('username')).first()
        if user:
            self.payload = jwt_payload_handler(user)
            attrs['user'] = user
            self.user = user
            return attrs
        else:
            raise serializers.ValidationError(_('No user found.'))

    def create_token(self):
        from django.utils import timezone
        from datetime import timedelta
        token = secrets.token_urlsafe(50)
        ForgetPasswordToken.objects.create(token=token, user=self.user,
                                           exp_time=timezone.now() + timedelta(0, 300))
        return token
