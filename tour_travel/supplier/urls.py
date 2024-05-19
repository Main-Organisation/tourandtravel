from django.urls import path
from .views import SupplierRegisterView, SupplierLoginView, SupplierDashboardView


urlpatterns = [
    path('register/', SupplierRegisterView.as_view(), name='supplier-register'),
    path('login/', SupplierLoginView.as_view(), name='supplier-login'),
    path('dashboard/', SupplierDashboardView.as_view(), name='supplier-dashboard'),
]
