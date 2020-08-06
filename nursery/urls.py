from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views
from django.conf.urls.static import static
from django.contrib import messages



urlpatterns = [
    path('',views.manager_home, name='manager_home'),
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='nursery_login'),
    path('register/', views.register, name='nursery_register'),
    path('logout/', auth_views.LogoutView.as_view(template_name='user/logout.html'), name='nursery_logout'),
    path('password-reset/',
        auth_views.PasswordResetView.as_view(
             template_name='user/password_reset.html'
         ),
         name='nursery_password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='user/password_reset_done.html'
         ),
         name='nursery_password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='user/password_reset_confirm.html'
         ),
         name='nursery_password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='user/password_reset_complete.html'
         ),
         name='nursery_password_reset_complete'),
]

