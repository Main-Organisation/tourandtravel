import random
import string

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from home.models import Country


# Create your models here.


class Service(models.Model):
    name = models.CharField(max_length=55)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class Supplier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='supplier')
    supplier_code = models.CharField(max_length=25, null=True, blank=True, unique=True, editable=False)
    email = models.EmailField(
        unique=True, null=True, blank=True,
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )
    mobile_number = models.CharField(max_length=15, null=True, blank=True)
    company_name = models.CharField(max_length=150, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL,
                                related_name='country_suppliers', null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    services = models.ManyToManyField(Service)
    is_verify = models.BooleanField(default=False)
    is_reject = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.supplier_code}"
    
    
    def save(self, *args, **kwargs):
        """Generates unique supplier code"""
        if self.pk is None:
            CODE_PREFIX = "SUPP"
            while True:
                code = f"{CODE_PREFIX}{random.randint(100000, 999999)}"
                if not Supplier.objects.filter(supplier_code=code).exists():
                    self.supplier_code = code
                    break
        return super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = _("Supplier")
        verbose_name_plural = _("Suppliers")