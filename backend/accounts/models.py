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
        user.save()

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
    account = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False)


class StaffAccount(models.Model):
    account = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False)
