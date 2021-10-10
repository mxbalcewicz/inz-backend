from rest_framework import serializers
from .models import User, StaffAccount, DeaneryAccount
from rest_framework.validators import UniqueValidator
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    """
    User serializer extended with created, updated readonly fields
    """
    class Meta:
        model = User
        fields = ['id', 'email', 'is_dean', 'is_staff', 'is_superuser']


class DeanRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User(email=validated_data.get('email'))
        user.set_password(validated_data.get('password'))
        user.save()
        dean = DeaneryAccount(account=user)
        dean.save()
        return user


class StaffRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = StaffAccount
        fields = ['name', 'surname', 'institute', 'job_title', 'academic_title', 'email', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User(email=validated_data.get('email'))
        user.set_password(validated_data.get('password'))
        user.save()

        staff = StaffAccount(account=user,
                             name=validated_data.get('name'),
                             surname=validated_data.get('surname'),
                             institute=validated_data.get('institute'),
                             job_title=validated_data.get('job_title'),
                             academic_title=validated_data.get('academic_title')
                             )
        staff.save()
        return user
