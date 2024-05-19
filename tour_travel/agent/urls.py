from django.urls import path
from .views import (
    AgentSignupView, 
    AgentLoginView, 
    AgentDashboardView, 
    AgentLogoutView,
    AgentDashboardFirstPage,
    AgentDashboardSecondPage,
    AgentBuildPackageView
)


urlpatterns = [
    path('agent-signup/', AgentSignupView.as_view(), name='agent-signup'),
    path('agent-login/', AgentLoginView.as_view(), name='agent-login'),
    path('agent-home/', AgentDashboardView.as_view(), name='agent-home'),
    path('agent-logout/', AgentLogoutView.as_view(), name='agent-logout'),
    path('agent-dashboard/first-page/', AgentDashboardFirstPage.as_view(), name='agent-dashboard-first-page'),
    path('agent-dashboard/second-page/', AgentDashboardSecondPage.as_view(), name='agent-dashboard-second-page'),
    path('agent/build-package/', AgentBuildPackageView.as_view(), name='agent-build-package'),
]
