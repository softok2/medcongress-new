from django.views.generic import TemplateView
from MedCongressApp.models import Pais
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import  HttpResponse,HttpResponseForbidden
from django.urls import reverse

 



class validarUser(UserPassesTestMixin):
    permission_denied_message = 'No tiene permiso para acceder a la administracion'
    login_url='/admin/login/'
    def test_func(self):
       
        if self.request.user.is_staff :
            return True
        else:
            return False
    
class DashboardView(validarUser,TemplateView):
    template_name= 'MedCongressAdmin/dashboard.html' 
    
  
    