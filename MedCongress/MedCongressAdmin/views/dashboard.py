from django.views.generic import TemplateView
from MedCongressApp.models import Pais
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import  HttpResponse,HttpResponseForbidden
from django.urls import reverse
from MedCongressAdmin.apps import validarUser
    
class DashboardView(validarUser,TemplateView):
    template_name= 'MedCongressAdmin/dashboard.html' 
    
  
    