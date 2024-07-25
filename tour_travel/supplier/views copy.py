from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.translation import gettext as _
from .forms import SupplierForm

class SupplierRegisterView(View):
    def get(self, request):
        form = SupplierForm()
        return render(request, 'supplier/supplier_signup.html', {'form': form})

    def post(self, request):
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        print(form.errors)  # Add this line to print form errors
        return render(request, 'supplier/supplier_signup.html', {'form': form})

class SupplierLoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('supplier-dashboard')
        return render(request, 'supplier/supplier_login.html')

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        sup_code = request.POST.get('sup_code')

        user = User.objects.filter(username=username).first()
        if user:
            if hasattr(user, 'supplier'):
                if user.supplier.supplier_code != sup_code:
                    messages.error(request, _('Invalid Supplier Code'))
                    return redirect('supplier-login')
                elif user.supplier.is_reject:
                    messages.error(request, _("Your account is rejected, please contact admin"))
                    return redirect('supplier-login')
                elif not user.supplier.is_verify:
                    messages.error(request, _("Your account is not verified yet"))
                    return redirect('supplier-login')
                else:
                    user = authenticate(request, username=username, password=password)
                    if user is not None:
                        login(request, user)
                        return redirect('supplier-dashboard')
                    else:
                        messages.error(request, _("Invalid Credentials!"))
                        return redirect('supplier-login')
            else:
                messages.error(request, _("No supplier account found with given credentials"))
                return redirect('supplier-login')
        else:
            messages.error(request, _("Invalid Credentials!"))
            return redirect('supplier-login')

class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, _('Logged out successfully'))
        return redirect('index')

class SupplierDashboardView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'supplier/supplier_dashboard.html')
