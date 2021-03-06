from django import forms
from django.contrib import messages
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from MedCongressApp.models import Ponente,PerfilUsuario
from MedCongressAdmin.forms.congres_forms import PonenteForm

class validarUser(UserPassesTestMixin):
    permission_denied_message = 'No tiene permiso para acceder a la administracion'
    login_url='/admin/login/'
    def test_func(self):
       
        if self.request.user.is_staff :
            return True
        else:
            return False
    

class PonentesListView(validarUser,ListView):
    model = Ponente
    context_object_name = 'ponentes'
    template_name = 'MedCongressAdmin/ponentes.html'

class  PonentesCreateView(validarUser,CreateView):
    form_class = PonenteForm
    success_url = reverse_lazy('MedCongressAdmin:Ponentes_list')
    template_name = 'MedCongressAdmin/ponente_form.html'

    def form_valid(self, form):
       
        taller=form.save(commit=False)
        taller.save()

        return super(PonentesCreateView, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        
        context = super(PonentesCreateView, self).get_context_data(**kwargs)
        ponentes=Ponente.objects.all()
        id=[]
        for ponente in ponentes:
            id.append(ponente.user.pk)
        context['users']=PerfilUsuario.objects.exclude(id__in=id)
        return context

class PonenteDeletedView(validarUser,DeleteView):
    model = Ponente
    success_url = reverse_lazy('MedCongressAdmin:talleres_list')


