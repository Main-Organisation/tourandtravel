from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from supplier.models import Supplier, Service
from agent.models import Agent


class AdminDashView(View):
    def get(self, request):
        return render(request, 'admin_user/admin_dash.html')
class MemberView(View):
    def get(self, request):
        return render(request, 'admin_user/member.html')

class AgentView(View):
    print("in agentview function view")
    def get(self, request):
        return render(request, 'admin_user/agent.html')

class SupplierView(View):
    def get(self, request):
        return render(request, 'admin_user/supplier.html')

class NewsBarView(View):
    def get(self, request):
        return render(request, 'admin_user/newsbar.html')


class AddPlaceView(View):
    def get(self, request):
        print('In addplace view function')
        return render(request, 'admin_user/addplace.html')

class NationalityView(View):
    def get(self, request):
        return render(request, 'admin_user/nationality.html')

class HotelsView(View):
    def get(self, request):
        return render(request, 'admin_user/hotals.html')

class ApprovedHotelView(View):
    def get(self, request):
        return render(request, 'admin_user/approvedhotel.html')

class PendingHotelView(View):
    def get(self, request):
        return render(request, 'admin_user/pendinghotel.html')
class SuspendHotelView(View):
    def get(self, request):
        return render(request, 'admin_user/pendinghotel.html')
class TransferView(View):
    def get(self, request):
        return render(request, 'admin_user/transfer.html')


class AdminAgentApprovalView(View):
    def get(self, request):
        return render(request, 'admin_user/agent.html')


#################################################################################################






class AdminLoginView(View):
    def get(self, request):
        return render(request, 'admin_user/admin_login.html')
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not username or not password:
            messages.error(request, _('Please provide username and password'))
            return redirect('admin-login')
        try:
            user = User.objects.get(username=username)
            if not user.is_superuser:
                messages.error(request, _('Only Admin can login'))
                return redirect('admin-login')
        except User.DoesNotExist:
            messages.error(request, _('Invalid username or password'))
            return redirect('admin-login')
        
        if user.check_password(password):
            login(request, user)
            return redirect('admin-dashboard')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('admin-login')
        


class AdminLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('admin-login')
    

class AdminDashboardView(LoginRequiredMixin, View):
    login_url = 'admin-login'
    def get(self, request):
        if not request.user.is_authenticated or not request.user.is_staff:
            return redirect('admin-login')
        return render(request, 'admin_user/admin_dash.html')
    

class AdminSupplierApprovalView(LoginRequiredMixin, View):
    login_url = 'admin-login'
    def get(self, request):
        if not request.user.is_authenticated or not request.user.is_staff:
            return redirect('admin-login')
        suppliers = Supplier.objects.order_by('-id')
        context = {'suppliers': suppliers}
        return render(request, 'admin_user/supplier.html', context)
    
    def post(self, request):
        for key, value in request.POST.items():
            if key.startswith('approve_'):
                supp_id = key.split('_')[1]
                try:
                    supplier = Supplier.objects.get(id=supp_id)
                except Supplier.DoesNotExist:
                    messages.error(request, _('Supplier does not exist'))
                    return redirect('admin-user-approval')
                
                supplier.is_verify = True
                supplier.save(update_fields=['is_verify'])
                messages.success(request, _('Supplier approved successfully'))

            # reject supplier
            if key.startswith('reject_'):
                supp_id = key.split('_')[1]
                try:
                    supplier = Supplier.objects.get(id=supp_id)
                except Supplier.DoesNotExist:
                    messages.error(request, _('Supplier does not exist'))
                    return redirect('admin-user-approval')
                
                supplier.is_reject = True
                supplier.save(update_fields=['is_reject'])
                messages.success(request, _('Supplier rejected'))

            # Update services
            if key.startswith('service_'):
                supp_id = key.split('_')[1]
                service_name = key.split('_', 2)[2]
                try:
                    supplier = Supplier.objects.get(id=supp_id)
                    service = Service.objects.get(name=service_name)
                except (Supplier.DoesNotExist, Service.DoesNotExist):
                    continue
                
                if value == 'on':
                    supplier.services.add(service)
                else:
                    supplier.services.remove(service)

        for supplier in Supplier.objects.prefetch_related('services').all():
            selected_services = [key.split('_', 2)[2] for key in request.POST if key.startswith(f'service_{supplier.id}_') and request.POST[key] == 'on']
            unselected_services = Service.objects.exclude(name__in=selected_services)
            supplier.services.remove(*unselected_services)

        return redirect('admin-supplier-approval')
    

class AdminSupplierServiceView(LoginRequiredMixin, View):
    login_url = 'admin-login'
    def get(self, request):
        if not request.user.is_authenticated or not request.user.is_staff:
            return redirect('admin-login')
        suppliers = Supplier.objects.all()
        for supplier in suppliers:
            print("Yes supplier is looping")
            for service in supplier.services.all():
                if service.name == 'Hotel' or service.name == 'hotel':
                    print("Yes hotel is present")
                    for hotel in supplier.hotels.all():
                        if hotel.is_active:
                            print(f"Hotel_Name: {hotel.name}")
        context = {'suppliers': suppliers}
        return render(request, 'admin_user/services.html', context)
    

# class AdminAgentApprovalView(LoginRequiredMixin, View):
#     login_url = 'admin-login'
#     def get(self, request, *args, **kwargs):
#         print("In the get function of AdminAgentApprovalView")
#         if not request.user.is_authenticated or not request.user.is_staff:
#             return redirect('admin-login')
#         agents = Agent.objects.all()
#         context = {'agents': agents}
#         return render(request, 'admin_user/agent_approval.html', context)
    
#     def post(self, request, *args, **kwargs):
#         agent_id = request.POST.get('approve')
#         try:
#             agent = Agent.objects.get(id=int(agent_id))
#         except Agent.DoesNotExist:
#             messages.error(request, _('Agent does not exist'))
#             return redirect('admin-agent-approval')
#         agent.is_verify = True
#         agent.save(update_fields=['is_verify'])
#         return redirect('admin-agent-approval')