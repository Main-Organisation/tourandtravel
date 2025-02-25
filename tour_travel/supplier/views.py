from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.utils.translation import gettext as _
from .forms import SupplierForm
from .models import Supplier
from django.contrib.auth.forms import AuthenticationForm

User = get_user_model()

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

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

def SupplierLoginView(request):
    if request.method == 'POST':
        print("supplier login view post")
        form = AuthenticationForm(request, data=request.POST)
        print(form)
        if form.is_valid():
            print("form is invalid")
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            print(f"username{username}")
            print(f"password {password}")
            if user is not None:
                if user.is_approved:
                    print("User is approved")
                    login(request, user)
                    return redirect('index')  # Redirect to a success page.
                else:
                    messages.error(request, 'Account not approved yet.')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'supplier/supplier_login.html', {'form': form})

class AgentLoginView(View):
    def get(self, request):
        return render(request, 'agent/agent_login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_approved or user.is_staff or user.is_superuser:
                login(request, user)
                return redirect('index')  # Redirect to the home page or any other page
            else:
                messages.error(request, 'Your account is not approved yet.')
        else:
            messages.error(request, 'Invalid username or password.')
        return render(request, 'agent/agent_login.html')

class MemberLoginView(View):
    def get(self, request):
        return render(request, 'member/member_login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_approved or user.is_staff or user.is_superuser:
                login(request, user)
                return redirect('index')  # Redirect to the home page or any other page
            else:
                messages.error(request, 'Your account is not approved yet.')
        else:
            messages.error(request, 'Invalid username or password.')
        return render(request, 'member/member_login.html')

def approve_supplier(request, supplier_id):
    supplier = get_object_or_404(Supplier, id=supplier_id)
    supplier.is_approved = True
    supplier.save()
    print("Supplier is approved")
    return redirect('index')

class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, _('Logged out successfully'))
        return redirect('index')

class SupplierDashboardView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'supplier/supplier_dashboard.html')
