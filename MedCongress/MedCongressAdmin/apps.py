from django.apps import AppConfig
from django.contrib.auth.mixins import UserPassesTestMixin,AccessMixin
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse_lazy,reverse
from MedCongressApp.models import Moderador,PerfilUsuario, RelBloqueModerador,User,Ubicacion,Organizador
class MedcongressadminConfig(AppConfig):
    name = 'medCongressAdmin'

class validarUser(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        
        if not self.request.user.is_staff:
            # Redirect the user to somewhere else - add your URL here
            url = "%s?next=%s" %(reverse('login'),request.path) 
            return HttpResponseRedirect(url)

        # Checks pass, let http method handlers process the request
        return super().dispatch(request, *args, **kwargs)

class validarOrganizador(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        
        autent=False
        if not self.request.user.is_anonymous:
            if self.request.user.is_staff:
                autent=True
            if Organizador.objects.filter(user=self.request.user.perfilusuario).exists():
                autent=True
                # Redirect the user to somewhere else - add your URL here
        
        if autent:
            return super().dispatch(request, *args, **kwargs)
        else:
            url = "%s?next=%s" %(reverse('login'),request.path) 
            return HttpResponseRedirect(url)
