from django.core.validators import MinValueValidator, MaxValueValidator
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
        if password is None:
            raise TypeError('User must have a password.')
        if not email:
            raise ValueError('User must have an email.')
        email = self.normalize_email(email)
        user = self.model(email=self.normalize_email(email), **kwargs)

        user.is_staff = True
        user.set_password(password)
        user.save()

        return user

    def create_dean_user(self, email, password, **kwargs):
        """
        Create and return a `User` with an email and password
        """
        if password is None:
            raise TypeError('User must have a password.')
        if not email:
            raise ValueError('User must have an email.')
        # if password != password2:
        #     raise ValueError("User's passwords do not match.")
        email = self.normalize_email(email)
        user = self.model(email=self.normalize_email(email), **kwargs)
        user.is_dean = True
        user.is_active = True
        user.set_password(password)
        user.save()

        return user

    def create_staff_user(self, email, **kwargs):
        """
        Create and return a `User` with an email and password
        """
        if not email:
            raise ValueError('User must have an email.')
        password = User.objects.make_random_password()
        email = self.normalize_email(email)
        user = self.model(email=self.normalize_email(email), **kwargs)
        user.is_staff = True
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

        #user = self.create_user(email, password)
        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.is_active = True
        user.is_superuser = True
        user.is_staff = True
        user.is_dean = True
        user.save()

        return user


class User(AbstractUser):
    """
    Custom user model
    """
    username = None
    email = models.EmailField(unique=True, blank=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_dean = models.BooleanField(default=False)

    name = models.CharField(max_length=20, null=True, default=None)
    surname = models.CharField(max_length=30, null=True, default=None)
    institute = models.CharField(max_length=100, null=True, default=None)
    job_title = models.CharField(max_length=50, null=True, default=None)
    academic_title = models.CharField(max_length=50, null=True, default=None)
    pensum_hours = models.IntegerField(blank=True, null=True, default=None, validators=[
        MinValueValidator(0),
        MaxValueValidator(250),
    ])
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f'Account id:{self.id}, Email:{self.email}, IsActive:{self.is_active}, IsStaff:{self.is_staff}, IsDean:{self.is_dean}'


# class DeaneryAccount(models.Model):
#     """
#     DeaneryAccount model linked to User instance
#     """
#     account = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False, primary_key=True)

#     def __str__(self):
#         return f'Account id:{self.account.id}, Email:{self.account.email}'


# class StaffAccount(models.Model):
#     """
#     StaffAccount model linked to User instance extended by additional information
#     """
#     account = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False, primary_key=True)
#     name = models.CharField(max_length=20, blank=False, default='')
#     surname = models.CharField(max_length=30, blank=False, default='')
#     # temp, should be relation to class Institute :X
#     institute = models.CharField(max_length=100, blank=False, default='')
#     job_title = models.CharField(max_length=50, blank=False, default='')
#     academic_title = models.CharField(max_length=50, blank=False, default='')
#     pensum_hours = models.IntegerField(blank=False, default=168, validators=[
#         MinValueValidator(0),
#         MaxValueValidator(250),
#     ])

#     def __str__(self):
#         return f'Account id:{self.account.id}, Name:{self.name} Surname:{self.surname} Email:{self.account.email}'
