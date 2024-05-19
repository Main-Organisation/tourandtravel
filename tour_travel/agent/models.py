import random
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from home.models import Country


# Create your models here.

class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='agent')
    agent_code = models.CharField(max_length=25, null=True, blank=True, unique=True, editable=False)
    email = models.EmailField(
        unique=True, null=True, blank=True,
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )
    mobile_number = models.CharField(max_length=15, null=True, blank=True)
    company_name = models.CharField(max_length=150, null=True, blank=True)
    country = models.ForeignKey('home.Country', on_delete=models.PROTECT, related_name='agents')
    city = models.CharField(max_length=50, null=True, blank=True)
    is_verify = models.BooleanField(default=False)
    send_newsletter = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.user.username} - {self.agent_code}"
    
    def save(self, *args, **kwargs):
        """Generates unique agent code"""
        if self.pk is None:
            CODE_PREFIX = "AGN"
            while True:
                code = f"{CODE_PREFIX}{random.randint(100000, 999999)}"
                if not Agent.objects.filter(agent_code=code).exists():
                    self.agent_code = code
                    break
        return super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = _("Agent")
        verbose_name_plural = _("Agents")


class Booking(models.Model):
    """
    Model that will be used for booking details
    """
    web_id = models.CharField(max_length=25, null=True, blank=True, editable=False)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='bookings')
    location = models.ForeignKey(Country, on_delete=models.PROTECT, related_name='bookings')
    arrival_date = models.DateField()
    guest_name = models.CharField(max_length=55)
    nationality = models.CharField(max_length=55, null=True, blank=True)
    number_of_adults = models.IntegerField(default=0, verbose_name=_("Number of Adults"))
    number_of_cwb = models.IntegerField(default=0, verbose_name=_("Number of CWB"))
    number_of_cnb = models.IntegerField(default=0, verbose_name=_("Number of CNB"))
    number_of_infants = models.IntegerField(default=0, verbose_name=_("Number of Infants"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return f"{self.guest_name} - {self.web_id}"
    
    def save(self, *args, **kwargs):
        if self.pk is None:
            country = kwargs.get('country')
            # country = "India"
            _web_id = random.randint(1000, 9999)
            self.web_id = f"{country[:2].upper()}{0}{0}{_web_id}"
        super().save()
    
    class Meta:
        verbose_name = _("Booking")
        verbose_name_plural = _("Bookings")
