"""
URL configuration for attendance project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView ,# This tells DRF: "By default, force everyone to authenticate using JWT." 
    TokenRefreshView , 

)

from core.views import AttendanceListCreateAPI , EmployeeListCreateAPI , AttendanceDetailAPI , EmployeeDetailAPI , ManagerLateDashboardAPI , login_view , signup_view , admin_dashboard , profile_view , attendance_action , employee_dashboard
# This tells DRF: "By default, force everyone to authenticate using JWT."
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/attendance/' , AttendanceListCreateAPI.as_view() , name='attendance-list-create'),
    path('api/employee/' , EmployeeListCreateAPI.as_view() , name='employee-list-create'),
    path('api/attendance/<int:pk>/' , AttendanceDetailAPI.as_view() , name='attendance-detail'),
    path('api/employee/<int:pk>/' , EmployeeDetailAPI.as_view() , name="employee-detail"),    # Real-World Principle: The Login Endpoints
    # POST username/password here to get your Access and Refresh tokens

    # Real-World Principle: The Login Endpoints
    # POST username/password here to get your Access and Refresh tokens
    path('api/token/' , TokenObtainPairView.as_view() , name='token_obbtain_pair'),

    # POST your Refresh token here to get a new Access token when the old one expires
    path('api/token/refresh' , TokenRefreshView.as_view() , name='token_refresh'),

    path('api/manager/dashboard/late/' , ManagerLateDashboardAPI.as_view() , name='manager-late-dashboard') ,

    # Web Pages
    path('core/signup/', signup_view, name='signup'),
    path('', login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('core/admin-dashboard/', admin_dashboard, name='admin-dashboard'),
    path('core/employee-dashboard/', employee_dashboard, name='employee-dashboard'),
    path('core/profile/', profile_view, name='profile'),
    path('core/attendance/action/', attendance_action, name='attendance-action'),

    path('dashboard-router/', dashboard_router, name='dashboard-router'),,


]
