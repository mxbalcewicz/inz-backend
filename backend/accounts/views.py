import random
from signal import raise_signal
import string
from tracemalloc import DomainFilter
from elasticsearch import serializer
import rest_framework
import jwt
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site

from .serializers import DeanAccountSerializer, ResetPasswordSerializer, UserSerializer, UserLoginSerializer, StaffAccountSerializer, StaffAccountUpdateSerializer, DeanAccountUpdateSerializer, SetNewPasswordSerializer
from .models import User
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from rest_framework_simplejwt import authentication
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from utils.email_handler import EmailUtil
from config.settings import SIMPLE_JWT, SECRET_KEY, FRONTEND_REDIRECT_URL
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from utils.email_handler import EmailUtil
from .permissions import CheckDeanOrStaffPermission

class ListUsers(RetrieveAPIView):
    """
    Admin only view to retrieve users in the system
    """
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer(many=True)


class DeanAccountGetPostView(APIView):
    serializer_class = DeanAccountSerializer
    permission_classes = (CheckDeanOrStaffPermission,)

    def get_queryset(self):
        return User.objects.filter(is_dean=True, is_superuser=False, is_active=True)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeanAccountRetrieveUpdateDeleteView(APIView):
    """
    DeaneryAccount retrieve, update, delete view
    """
    serializer_class = DeanAccountUpdateSerializer
    permission_classes = (CheckDeanOrStaffPermission,)

    def get(self, request, pk):
        instance = get_object_or_404(User, pk=pk)
        serializer = self.serializer_class(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        instance = User.objects.get(pk=pk)
        instance.account.delete()
        instance.delete()
        return Response(status=status.HTTP_200_OK)

    def put(self, request, pk):
        """Email update only method"""
        instance = User.objects.get(pk=pk)
        serializer = self.serializer_class(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class StaffAccountGetPostView(APIView):
    serializer_class = StaffAccountSerializer
    permission_classes = (CheckDeanOrStaffPermission,)

    def get_queryset(self):
        return User.objects.filter(is_staff=True, is_superuser=False, is_active=True)

    # Register method + send email verify
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data
        user = User.objects.get(email=user_data.get('email'))
        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request).domain
        relative_link = reverse("activate-account")
        abs_url = FRONTEND_REDIRECT_URL + \
            relative_link + "/" + str(token)
        email_body = "Witaj " + user.email + \
            "\nZweryfikuj adres email i aktywuj konto klikając w link:" + "\n" + abs_url
        data = {
            'domain': current_site,
            'email_body': email_body,
            'to_email': user.email,
            'email_subject': "EduPlanner - Zweryfikuj adres email"
        }

        EmailUtil.send_email(data)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StaffAccountRetrieveUpdateDeleteView(APIView):
    """
    StaffAccount retrieve, update, delete view
    """
    serializer_class = StaffAccountUpdateSerializer
    permission_classes = (CheckDeanOrStaffPermission,)

    def get(self, request, pk):
        instance = get_object_or_404(User, pk=pk)
        serializer = self.serializer_class(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        instance = User.objects.get(pk=pk)
        instance.delete()
        return Response(status=status.HTTP_200_OK)

    def put(self, request, pk):
        instance = User.objects.get(pk=pk)
        serializer = self.serializer_class(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class VerifyEmail(APIView):
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms='HS256')
            user = User.objects.get(pk=payload.get('user_id'))
            email = user.email
            if not user.is_active:
                user.is_active = True
                user.save()

            return Response({'email': 'Successfully activated!'}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError:
            return Response({'error': {'message': "Activation link expired.", 'code':"TOKEN_EXPIRED"}}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response({'error': {'message': "Invalid token.", 'code': "TOKEN_INVALID"}}, status=status.HTTP_400_BAD_REQUEST)


class ResendVerifyEmail(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        email = request.data.get('email')

        serializer = self.serializer_class(
            instance=User.objects.get(email=email))
        user_data = serializer.data
        user = get_object_or_404(User, email=user_data.get('email'))
        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request).domain
        relative_link = reverse("activate-account")
        abs_url = FRONTEND_REDIRECT_URL + \
            relative_link + "/" + str(token)
        email_body = "Witaj " + user.email + \
            "\nZweryfikuj adres email i aktywuj konto klikając w link:" + "\n" + abs_url
        data = {
            'domain': current_site,
            'email_body': email_body,
            'to_email': user.email,
            'email_subject': "EduPlanner - Zweryfikuj adres email"
        }

        EmailUtil.send_email(data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RequestPasswordResetEmail(APIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.data.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))

            redirect_url = FRONTEND_REDIRECT_URL
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request).domain
            relative_link = reverse(
                "password-reset-confirm", kwargs={'uidb64': uidb64, 'token': token})
            abs_url = redirect_url + relative_link
            email_body = "Witaj " + user.email + \
                "\nMożesz zresetować swoje hasło pod tym adresem:" + "\n" + abs_url
            data = {
                'domain': current_site,
                'email_body': email_body,
                'to_email': user.email,
                'email_subject': "EduPlanner - Zresetuj swoje hasło"
            }

            EmailUtil.send_email(data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)


class PasswordTokenCheckAPI(APIView):

    def get(self, request, uidb64, token):
        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response(status=status.HTTP_400_BAD_REQUEST)
            return Response({'message': "Credentials valid.", 'uidb64': uidb64, 'token': token}, status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class SetNewPasswordView(APIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(status=status.HTTP_200_OK)


class Login(APIView):
    permission_classes = (CheckDeanOrStaffPermission,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.data.get('email')
        password = request.data.get('password')
        if User.objects.filter(email=email).exists():
            user = User.objects.filter(email=email).first()
            if check_password(password, user.password):
                user_details = {'email': user.email}
                refresh = RefreshToken.for_user(user)
                user_details['access'] = str(refresh.access_token)
                role_name = "NONE"
                if user.is_dean:
                    role_name = "DEAN"
                if user.is_staff:
                    role_name = "STAFF"
                if user.is_superuser:
                    role_name = "ADMIN"

                user_details['role'] = role_name
                user_details['expire'] = int(
                    SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds())
                response = Response(user_details, status=status.HTTP_200_OK)
                response.set_cookie('refresh_token', str(refresh), httponly=True, secure=False, samesite=None,
                                    max_age=300, path="/",
                                    expires=int(SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()))
                return response
            else:
                return Response({'Error': 'Wrong password'}, status.HTTP_403_FORBIDDEN)
        else:
            return Response({'Error': 'Account not active or bad request'}, status=status.HTTP_400_BAD_REQUEST)


class Refresh(APIView):
    permission_classes = [CheckDeanOrStaffPermission]

    def post(self, request):
        if request.COOKIES.get('refresh_token'):
            old_refresh = jwt.decode(request.COOKIES.get(
                'refresh_token'), SECRET_KEY, algorithms=["HS256"])
            user = User.objects.filter(id=old_refresh['user_id']).first()
            refresh = RefreshToken.for_user(user)
            role_name = "NONE"
            if user.is_dean:
                role_name = "DEAN"
            if user.is_staff:
                role_name = "STAFF"
            if user.is_superuser:
                role_name = "ADMIN"

            user_details = {'access': str(refresh.access_token),
                            'expire': int(SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()),
                            'role': role_name
                            }
            response = Response(user_details, status=status.HTTP_200_OK)
            response.set_cookie('refresh_token', str(refresh), httponly=True, secure=False,
                                expires=int(SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()), samesite=None,
                                max_age=300, path="/")
            return response
        else:
            return Response({'Error': 'No refresh_token cookie.'}, status=status.HTTP_400_BAD_REQUEST)


class Logout(APIView):
    permission_classes = [CheckDeanOrStaffPermission]

    def post(self, request):
        if request.COOKIES.get('refresh_token'):
            response = Response(status=status.HTTP_200_OK)
            response.delete_cookie('refresh_token')
            return response
        else:
            return Response(status=status.HTTP_200_OK)
