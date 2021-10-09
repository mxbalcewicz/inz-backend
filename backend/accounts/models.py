from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.conf import settings


class UserManager(BaseUserManager):
    """
    Custom user manager linked to User model
    """
    def create_user(self, email, password, **kwargs):
        """
        Create and return a `User` with an email and password
        """
        if not email:
            raise ValueError('User must have an email.')
        email = self.normalize_email(email)
        user = self.model(email=self.normalize_email(email), **kwargs)
        user.is_active = True
        user.set_password(password)

        return user

    def create_superuser(self, email, password, **kwargs):
        """
        Create and return a `User` with superuser (admin) permissions
        """
        if password is None:
            raise TypeError('Superuser must have a password.')
        if email is None:
            raise TypeError('Superuser must have an email.')

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractUser):
    """
    Custom user model
    """
    username = None
    email = models.EmailField(unique=True, blank=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_dean = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class DeaneryAccount(models.Model):
    """
    DeaneryAccount model linked to User instance
    """
    account = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False)


class StaffAccount(models.Model):
    """
    StaffAccount model linked to User instance extended by additional information
    """
    account = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False)
    name = models.CharField(max_length=20, blank=False, default='')
    surname = models.CharField(max_length=30, blank=False, default='')
    institute = models.CharField(max_length=100, blank=False, default='')
    job_title = models.CharField(max_length=50, blank=False, default='')
    academic_title = models.CharField(max_length=50, blank=False, default='')
