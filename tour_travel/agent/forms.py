from typing import Any
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib import messages
from .models import Agent


class AgentRegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    mobile_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    company_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    country = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)


    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()
        # print(f"form_data: {cleaned_data}")
        password = cleaned_data.get('password')
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        if password and len(password) < 6:
            messages.error(self.request, _("Password should be at least 6 characters long"))
            return redirect('agent-signup')
            raise ValidationError(_("Password should be at least 6 characters long"))
        
        # check if username or email is already registered or not
        if User.objects.filter(username=username).exists():
            messages.error(self.request, _("Username already exists"))
            return redirect('agent-signup')
            raise ValidationError(_('Username already exists'))
        if User.objects.filter(email=email).exists():
            messages.error(self.request, _("Email already exists"))
            return redirect('agent-signup')
            raise ValidationError(_('Email already exists'))
        
        return cleaned_data