from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View
from django.db import transaction
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from agent.helpers import validate_user
from supplier.models import Supplier



class HomeView(View):
    def get(self, request):
        return render(request, 'home/index.html')
    
