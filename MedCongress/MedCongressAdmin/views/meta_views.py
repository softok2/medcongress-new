
from django import forms
from django.contrib import messages
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse_lazy,reverse
from django.views.generic import ListView,CreateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.edit import  DeleteView, UpdateView,FormView
from MedCongressApp.models import MetaPagInicio,MetaPagListCongreso
from MedCongressAdmin.forms.congres_forms import MetaPagInicioForm 

class validarUser(UserPassesTestMixin):
    permission_denied_message = 'No tiene permiso para acceder a la administracion'
    login_url='/admin/login/'
    def test_func(self):
       
        if self.request.user.is_staff :
            return True
        else:
            return False
    

class MetaPagInicioView(validarUser,ListView):
    model = MetaPagInicio
    context_object_name = 'metas_pag_inicio'
    template_name = 'MedCongressAdmin/meta_pag_inicio.html'

class MetaPagInicioUpdateView(validarUser,UpdateView):
    form_class = MetaPagInicioForm
    success_url = reverse_lazy('MedCongressAdmin:otros_list')
    template_name = 'MedCongressAdmin/meta_pag_inicio_form.html'

    def get_queryset(self, **kwargs):
        return MetaPagInicio.objects.filter(pk=self.kwargs.get('pk'))