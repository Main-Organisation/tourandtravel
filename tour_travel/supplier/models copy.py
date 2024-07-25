from django.db import models
from django_countries.fields import CountryField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class Person(models.Model):
    name = models.CharField(max_length=100)
    country = CountryField()

class Service(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class SupplierManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username field must be set")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, password, **extra_fields)

class Supplier(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)
    company = models.CharField(max_length=255)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    country = CountryField()
    city = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15)
    services = models.ManyToManyField(Service, blank=True)
    approved_services = models.ManyToManyField(Service, related_name='approved_services', blank=True)
    is_approved = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = SupplierManager()

    def __str__(self):
        return self.username
