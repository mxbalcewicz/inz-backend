from .serializers import UserSerializer, DeanAccountSerializer, StaffAccountSerializer
from .models import DeaneryAccount, StaffAccount
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
    serializer_class = StaffAccountSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        deanery_accounts = StaffAccount.objects.all()
        serializer = self.serializer_class(deanery_accounts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StaffAccountRetrieveUpdateDeleteView(APIView):
    """
    StaffAccount retrieve, update, delete view
    """
    serializer_class = StaffAccountSerializer
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        instance = get_object_or_404(StaffAccount, pk=pk)
        serializer = self.serializer_class(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        instance = StaffAccount.objects.get(pk=pk)
        instance.account.delete()
        instance.delete()
        return Response(status=status.HTTP_200_OK)

    def put(self, request, pk):
        """Email update only method"""
        instance = StaffAccount.objects.get(pk=pk)
        instance.account.email = request.data.get('account.email')
        instance.account.save()
        serializer = self.serializer_class(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)