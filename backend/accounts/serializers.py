from ast import Pass
from rest_framework.exceptions import AuthenticationFailed
from posixpath import supports_unicode_filenames
from unicodedata import name
from unittest.util import _MIN_END_LEN
from django.http import request
from rest_framework import serializers

# from api.views import validate
from .models import User
from rest_framework.validators import UniqueValidator
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
import random
import string


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']


class StaffAccountSerializer(serializers.ModelSerializer):
    email = serializers.CharField()
    # password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    # password2 = serializers.CharField(write_only=True, required=True)
    name = serializers.CharField(required=True)
    surname = serializers.CharField(required=True)
    institute = serializers.CharField(required=True)
    job_title = serializers.CharField(required=True)
    academic_title = serializers.CharField(required=True)
    pensum_hours = serializers.IntegerField(required=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'surname',
                  'institute', 'job_title', 'academic_title', 'pensum_hours']

    def create(self, validated_data):
        user = User.objects.create_staff_user(**validated_data)
        user.save()
        return user


class StaffAccountUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'surname', 'institute',
                  'job_title', 'academic_title', 'pensum_hours']

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        return instance


class DeanAccountUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        return instance


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()


class DeanAccountSerializer(serializers.ModelSerializer):
    email = serializers.CharField()
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    # password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_dean_user(**validated_data)
        user.save()
        return user


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, min_length=6, max_length=26)
    token = serializers.CharField(write_only=True)
    uidb64 = serializers.CharField(write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, validated_data):
        try:
            password = validated_data.get('password')
            token = validated_data.get('token')
            uidb64 = validated_data.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed
                # return Response(status=status.HTTP_401_UNAUTHORIZED)
            user.set_password(password)
            user.save()

            return user
        except Exception as e:
            raise AuthenticationFailed


class StaffAccountImportExportSerializer(serializers.ModelSerializer):
    email = serializers.CharField()
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    name = serializers.CharField(required=True)
    surname = serializers.CharField(required=True)
    institute = serializers.CharField(required=True)
    job_title = serializers.CharField(required=True)
    academic_title = serializers.CharField(required=True)
    pensum_hours = serializers.IntegerField(required=True)
    is_dean = serializers.BooleanField(required=True)
    is_staff = serializers.BooleanField(required=True)
    is_active = serializers.BooleanField(required=True)
    is_superuser = serializers.BooleanField(required=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'password2', 'name', 'surname',
                  'institute', 'job_title', 'academic_title', 'pensum_hours', 'is_dean', 'is_staff', 'is_active', 'is_superuser']

    def create(self, validated_data):
        user = User.objects.create_staff_user(**validated_data)
        user.save()
        return user
