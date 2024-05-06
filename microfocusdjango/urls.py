from django.urls import path
from . import views
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetCompleteView


urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.register, name='register'),
    path('activate/<uidb64>/<token>/', views.VerificationView.as_view(), name='activate'),
    path('login', views.login_user, name='login'),
    path('password_reset', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/password_reset/done/', PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('password_reset/reset/<uidb64>/<token>/set-password/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/reset/done/', PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('password_reset/login', views.login_user, name='password_reset_login'),
    path('school_dashboard', views.school_dashboard, name='school_dashboard'),
    path('admin_user/dashboard', views.admin_dashboard, name='admin_dashboard'),
    path('logout', views.logout_user, name='logout'),

]