from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Country(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=55)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')
