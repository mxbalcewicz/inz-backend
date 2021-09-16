from rest_framework import serializers
from .models import User
from django.core.exceptions import ObjectDoesNotExist


class UserSerializer(serializers.ModelSerializer):
    """
    User serializer extended with created, updated readonly fields
    """
    class Meta:
        model = User
        fields = ['id', 'email', 'is_dean', 'is_staff', 'is_superuser']


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=8, required=True)
    email = serializers.EmailField(required=True, max_length=128)

    class Meta:
        model = User
        fields = ['id', 'email', 'password']

    def create(self, validated_data, is_dean=False, is_staff=False):
        try:
            user = User.objects.get(email=validated_data['email'])
        except ObjectDoesNotExist:
            password = validated_data['password']
            email = validated_data['email']
            user = User.objects.create_user(email=email, password=password)
        return user