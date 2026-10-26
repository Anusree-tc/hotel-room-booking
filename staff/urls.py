from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path(
        'login/',
        LoginView.as_view(
    template_name='staff/login.html',
    redirect_authenticated_user=False
        ),
        name='staff_login'
    ),
    
path(
    'logout/',
    LogoutView.as_view(next_page='/staff/login/'),
    name='staff_logout'
),
    path('', views.dashboard, name='staff_dashboard'),
        path(
        'check-in/<int:booking_id>/',
        views.check_in_booking,
        name='staff_check_in'
    ),
    path(
        'check-out/<int:booking_id>/',
        views.check_out_booking,
        name='staff_check_out'
    ),
    path('reports/', views.admin_reports, name='admin_reports'),
]
