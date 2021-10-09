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
    name = serializers.CharField(max_length=20)
    surname = serializers.CharField(max_length=30)
    institute = serializers.CharField(max_length=100)
    job_title = serializers.CharField(max_length=50)
    academic_title = serializers.CharField(max_length=50)

    class Meta:
        model = User
        fields = ['email', 'password', 'password2', 'name', 'surname', 'institute', 'job_title', 'academic_title']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User(email=validated_data.get('email'))
        user.set_password(validated_data.get('password'))
        user.save()

        staff = StaffAccount(account=user)

        staff.save()
        return user
