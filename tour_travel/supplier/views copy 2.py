from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.translation import gettext as _
from .forms import SupplierForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Supplier
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.http import HttpResponse





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

# class SupplierLoginView(View):
#     def get(self, request, *args, **kwargs):
#         if request.user.is_authenticated:
#             return redirect('supplier-dashboard')
#         return render(request, 'supplier/supplier_login.html')

#     def post(self, request, *args, **kwargs):
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         sup_code = request.POST.get('sup_code')

#         user = User.objects.filter(username=username).first()
#         if user:
#             if hasattr(user, 'supplier'):
#                 if user.supplier.supplier_code != sup_code:
#                     messages.error(request, _('Invalid Supplier Code'))
#                     return redirect('supplier-login')
#                 elif user.supplier.is_reject:
#                     messages.error(request, _("Your account is rejected, please contact admin"))
#                     return redirect('supplier-login')
#                 elif not user.supplier.is_verify:
#                     messages.error(request, _("Your account is not verified yet"))
#                     return redirect('supplier-login')
#                 else:
#                     user = authenticate(request, username=username, password=password)
#                     if user is not None:
#                         login(request, user)
#                         return redirect('supplier-dashboard')
#                     else:
#                         messages.error(request, _("Invalid Credentials!"))
#                         return redirect('supplier-login')
#             else:
#                 messages.error(request, _("No supplier account found with given credentials"))
#                 return redirect('supplier-login')
#         else:
#             messages.error(request, _("Invalid Credentials!"))
#             return redirect('supplier-login')




from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

def SupplierLoginView(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            print(username,password,user)
            if user is not None:
                if user.is_approved:
                    login(request, user)
                    return redirect('index')  # Redirect to a success page.
                else:
                    # Add a message to inform the user they are not approved yet.
                    return render(request, 'login.html', {'form': form, 'error': 'Account not approved yet.'})
            else:
                # Return an 'invalid login' error message.
                return render(request, 'login.html', {'form': form, 'error': 'Invalid username or password.'})
    else:
        form = AuthenticationForm()
    return redirect('index')  


    

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
