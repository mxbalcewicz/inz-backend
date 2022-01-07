import random
import string

from .serializers import UserSerializer, DeanAccountSerializer, StaffAccountSerializer, StaffAccountNormalSerializer
from .models import DeaneryAccount, StaffAccount, User
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework_simplejwt import authentication
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404


class ListUsers(RetrieveAPIView):
    """
    Admin only view to retrieve users in the system
    """
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer(many=True)


class DeanAccountGetPostView(APIView):
    """
    DeaneryAccount get, post view
    """
    serializer_class = DeanAccountSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        deanery_accounts = DeaneryAccount.objects.all()
        serializer = self.serializer_class(deanery_accounts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeanAccountRetrieveUpdateDeleteView(APIView):
    """
    DeaneryAccount retrieve, update, delete view
    """
    serializer_class = DeanAccountSerializer
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        instance = get_object_or_404(DeaneryAccount, pk=pk)
        serializer = self.serializer_class(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        instance = DeaneryAccount.objects.get(pk=pk)
        instance.account.delete()
        instance.delete()
        return Response(status=status.HTTP_200_OK)

    def put(self, request, pk):
        """Email update only method"""
        instance = DeaneryAccount.objects.get(pk=pk)
        instance.account.email = request.data.get('account.email')
        instance.account.save()
        updated_instance = DeaneryAccount.objects.get(pk=pk)
        serializer = self.serializer_class(updated_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StaffAccountGetPostView(APIView):
    """
    StaffAccount get, post view
    """
    serializer_class = StaffAccountNormalSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User(email=request.data.get('email'))
        user.set_password(self.generate_password())
        user.save()
        staff = StaffAccount.objects.create(account=user,
                                            name=request.data.get('name'),
                                            surname=request.data.get('surname'),
                                            institute=request.data.get('institute'),
                                            job_title=request.data.get('job_title'),
                                            academic_title=request.data.get('academic_title'),
                                            pensum_hours=request.data.get('pensum_hours')
                                            )
        staff.save()
        return Response(deleteNestedAccountInStaff(staff), status=status.HTTP_201_CREATED)

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

    def get(self, request):
        staff_accounts = StaffAccount.objects.all()
        data = []
        for i in staff_accounts:
            data.append(deleteNestedAccountInStaff(i))

        return Response(tuple(data), status=status.HTTP_200_OK)


def deleteNestedAccountInStaff(staff):
    if staff is not None:
        return {
            'id': staff.account.id,
            'email': staff.account.email,
            'name': staff.name,
            'surname': staff.surname,
            'institute': staff.institute,
            'job_title': staff.job_title,
            'academic_title': staff.academic_title,
            'pensum_hours': staff.pensum_hours
        }
    else:
        return {}


class StaffAccountRetrieveUpdateDeleteView(APIView):
    """
    StaffAccount retrieve, update, delete view
    """
    serializer_class = StaffAccountSerializer
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        instance = get_object_or_404(StaffAccount, pk=pk)

        return Response(deleteNestedAccountInStaff(instance), status=status.HTTP_200_OK)

    def delete(self, request, pk):
        instance = StaffAccount.objects.get(pk=pk)
        instance.account.delete()
        instance.delete()
        return Response(status=status.HTTP_200_OK)

    def put(self, request, pk):
        """Email update only method"""
        instance = StaffAccount.objects.get(pk=pk)
        instance.account.email = request.data.get('account.email')
        instance.name = request.data.get('name')
        instance.surname = request.data.get('surname')
        instance.institute = request.data.get('institute')
        instance.job_title = request.data.get('job_title')
        instance.academic_title = request.data.get('academic_title')
        instance.account.save()
        serializer = self.serializer_class(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
