"""MedCongress URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path,include
from django.utils.functional import curry
from django.contrib.auth.views import *
from django.views.defaults import permission_denied
from MedCongressApp.forms import EmailValidationOnForgotPassword,PasswordChangeOnForgotPassword




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('MedCongressApp.urls')),

    path('administration/', include('MedCongressAdmin.urls')),
    
    path('accounts/password_reset/', PasswordResetView.as_view(template_name='registration/password_reset_form.html',form_class=EmailValidationOnForgotPassword), name='password_reset'),
    path('accounts/password_reset/done/', PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html',form_class=PasswordChangeOnForgotPassword), name='password_reset_confirm'),
    path('accounts/reset/done/', PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    path('accounts/', include('django.contrib.auth.urls')),
]   

