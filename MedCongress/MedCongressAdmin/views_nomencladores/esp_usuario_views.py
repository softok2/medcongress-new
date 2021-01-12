from django import forms
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views.defaults import page_not_found
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
from django.utils.crypto import get_random_string
from django.views.generic import CreateView, ListView, TemplateView
from django.views.generic.edit import DeleteView, FormView, UpdateView
from MedCongressAdmin.forms.nomencladores_forms import EspUsuarioForm
from MedCongressApp.models import Especialidades,PerfilUsuario
from MedCongressAdmin.apps import validarUser
    

class EspUsuarioListView(validarUser,ListView):
    model = Especialidades
    context_object_name = 'esp_usuarios'
    template_name = 'nomencladores/esp_usuarios/index.html'

class EspUsuarioCreateView(validarUser,CreateView):
    model=Especialidades
    form_class = EspUsuarioForm
    success_url = reverse_lazy('MedCongressAdmin:esp_usuarios_list')
    template_name = 'nomencladores/esp_usuarios/form.html'


class EspUsuarioDeletedView(validarUser,DeleteView):
    model = Especialidades
    success_url = reverse_lazy('MedCongressAdmin:esp_usuarios_list')

    def delete(self,request, *args, **kwargs):
            
        especialidad=Especialidades.objects.get(pk=self.kwargs.get('pk'))
       
        if PerfilUsuario.objects.filter(especialidad=especialidad).exists():
            return JsonResponse({'success':False}, safe=False)
        else:
            especialidad.delete()
            return JsonResponse({'success':True}, safe=False)

class EspUsuarioUpdateView(validarUser,UpdateView):
    form_class = EspUsuarioForm
    success_url = reverse_lazy('MedCongressAdmin:esp_usuarios_list')
    template_name = 'nomencladores/esp_usuarios/form.html'

    def get_queryset(self, **kwargs):
        return Especialidades.objects.filter(pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['update']=True
        return context


