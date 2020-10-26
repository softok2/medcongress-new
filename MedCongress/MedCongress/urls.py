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

from django.views.defaults import permission_denied
from django.conf.urls import (
handler400, handler403, handler404, handler500
)
# from MedCongressApp.views import bad_request,permission_denied,page_not_found,server_error

# handler400 = bad_request
# handler403 = permission_denied
# handler404 = page_not_found
# handler500 = server_error




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('MedCongressApp.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('administration/', include('MedCongressAdmin.urls')),
]

