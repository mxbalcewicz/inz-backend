from rest_framework import serializers
from .models import User, StaffAccount, DeaneryAccount
from rest_framework.validators import UniqueValidator
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.password_validation import validate_password
import random
import string


class UserSerializer(serializers.ModelSerializer):
    """
    User serializer extended with created, updated readonly fields
    """
    class Meta:
        model = User
        fields = ['id', 'email', ]


class UserReadSerializer(serializers.ModelSerializer):
    """
    User read only serializer
    """
    class Meta:
        model = User
        fields = ['id', 'email', 'is_dean', 'is_staff', 'is_superuser']


class DeanAccountSerializer(serializers.ModelSerializer):
    account = UserSerializer()
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = DeaneryAccount
        fields = ['account', 'password', 'password2']

    def create(self, validated_data):
        account_data = validated_data.pop('account')
        user = User(email=account_data.get('email'))
        user.set_password(validated_data.get('password'))
        user.save()
        dean = DeaneryAccount(account=user)
        dean.save()
        return dean


class StaffAccountSerializer(serializers.ModelSerializer):
    account = UserSerializer()

    class Meta:
        model = StaffAccount
        fields = ['name', 'surname', 'institute', 'job_title', 'academic_title', 'account']

    @staticmethod
    def generate_password():
        random_pass = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(16))
        return random_pass

    @staticmethod
    def generate_email(name, surname):
        pl_dict = {
            'ą': 'a',
            'ć': 'c',
            'ę': 'e',
            'ł': 'l',
            'ń': 'n',
            'ó': 'o',
            'ś': 's',
            'ź': 'z',
            'ż': 'ż'
        }
        name_initial = name[0]
        for i in surname:
            if i in pl_dict.keys():
                surname = surname.replace(i, pl_dict[i])

        email = (name_initial + surname + '@domain.com').lower()
        return email

    def create(self, validated_data):
        account_data = validated_data.get('account')
        user = User(email=account_data.get('email'))
        user.set_password(self.generate_password())
        user.save()
        staff = StaffAccount.objects.update_or_create(account=user,
                                                      name=validated_data.get('name'),
                                                      surname=validated_data.get('surname'),
                                                      institute=validated_data.get('institute'),
                                                      job_title=validated_data.get('job_title'),
                                                      academic_title=validated_data.get('academic_title')
                                                      )
        staff.save()
        return staff
