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
from home.models import Country
from .models import Service, Supplier

# Create your views here.


class SupplierRegisterView(View):
    def get(self, request, *args, **kwargs):
        services = Service.objects.all()
        countries = Country.objects.all()
        context = {'services': services, 'countries': countries}
        return render(request, 'supplier/supplier_signup.html', context)
    
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        mobile_number = request.POST.get('mobile')
        company_name = request.POST.get('company')
        c_id = request.POST.get('country')
        city = request.POST.get('city')
        services = request.POST.getlist('services')
        try:
            country = Country.objects.get(id=c_id)
        except Country.DoesNotExist:
            messages.error(request, _('Country does not exist.'))
            return redirect('supplier-register')
        data = {
            'username': username,
            'email': email
        }
        errors = validate_user(**data)
        if errors or len(errors) > 0:
            for error in errors:
                messages.error(request, error)
            return redirect('index')
        try:
            _user = User(
            username=username, email=email, password=password,
            first_name=first_name, last_name=last_name)
            validate_password(password, _user)
        except Exception as e:
            messages.error(request, str(e))
            return redirect('index')
        try:
            with transaction.atomic():
                user = User.objects.create_user(
                    username=username, email=email, password=password,
                    first_name=first_name, last_name=last_name)
                supplier = Supplier.objects.create(
                    user=user,
                    email=email,
                    mobile_number=mobile_number,
                    company_name=company_name,
                    country=country,
                    city=city,
                )
            if services:
                supplier.services.add(*services)
            messages.success(request, _(
                f"Registration Success, your SUP_CODE is: {supplier.supplier_code}, you can login once verified."
                ))
        except Exception as e:
            messages.error(request, str(e))
            return redirect('supplier-register')
        return redirect('index')
    

class SupplierLoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('supplier-dashboard')
        return render(request, 'supplier/supplier_login.html')
    
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        sup_code = request.POST.get('sup_code')

        user = User.objects.filter(username=username)
        if user.exists():
            user = user.first()
            if user.supplier: 
                if user.supplier.supplier_code != sup_code:
                    messages.error(request, _('Invalid Supplier Code'))
                    return redirect('index')
                elif user.supplier.is_reject:
                    messages.error(request, _("Your account is rejected, please contact admin"))
                    return redirect('index')
                elif not user.supplier.is_verify:
                    messages.error(request, _("Your account is not verified yet"))
                    return redirect('index')
                else:
                    user = authenticate(request, username=username, password=password)
                    if user is not None:
                        login(request, user)
                        return redirect('supplier-dashboard')
                    else:
                        messages.error(request, _("Invalid Credentials!"))
                        return redirect('index')
            else:
                messages.error(request, _("No supplier account found with given credentials"))
                return redirect('index')
        else:
            messages.error(request, _("Invalid Credentials!"))
            return redirect('index')
        

class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, _('Logged out successfully'))
        return redirect('index')
    

class SupplierDashboardView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'supplier/supplier_dashboard.html')