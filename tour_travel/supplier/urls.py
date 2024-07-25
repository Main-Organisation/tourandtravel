from django.urls import path
from .views import SupplierRegisterView, SupplierLoginView, approve_supplier, LogoutView, SupplierDashboardView

urlpatterns = [
    path('register/', SupplierRegisterView.as_view(), name='register'),
    path('login/', SupplierLoginView, name='login'),
    path('approve-supplier/<int:supplier_id>/', approve_supplier, name='approve-supplier'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('supplier-dashboard/', SupplierDashboardView.as_view(), name='supplier-dashboard'),
    # Add other paths here
]
