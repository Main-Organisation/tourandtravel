from django.urls import path
from .views import *

urlpatterns = [
    path('login/', AdminLoginView.as_view(), name='admin-login'),
    path('logout/', AdminLogoutView.as_view(), name='admin-logout'),
    path('dashboard/', AdminDashboardView.as_view(), name='admin-dashboard'),
    path('user-approval/', AdminSupplierApprovalView.as_view(), name='admin-supplier-approval'),
    path('user-services/', AdminSupplierServiceView.as_view(), name='admin-user-services'),
    path('agent-approval/', AdminAgentApprovalView.as_view(), name='admin-agent-approval'),
    path('member/', MemberView.as_view(), name='admin-member'),
    path('supplier/', SupplierView.as_view(), name='admin-supplier'),
    path('newsbar/', NewsBarView.as_view(), name='admin-newsbar'),
    path('addplace/', AddPlaceView.as_view(), name='admin-addplace'),
    path('nationality/', NationalityView.as_view(), name='admin-nationality'),
    path('hotels/', HotelsView.as_view(), name='admin-hotels'),
    path('approved-hotel/', ApprovedHotelView.as_view(), name='admin-approved-hotel'),
    path('pending-hotel/', PendingHotelView.as_view(), name='admin-pending-hotel'),
    path('suspend-hotel/', SuspendHotelView.as_view(), name='admin-suspend-hotel'),
    path('transfer/', TransferView.as_view(), name='admin-transfer'),
    path('admin-dash/', AdminDashView.as_view(), name='admindashboard'),
]
