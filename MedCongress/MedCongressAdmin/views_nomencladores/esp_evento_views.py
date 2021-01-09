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
from MedCongressAdmin.forms.nomencladores_forms import EspEventoForm
from MedCongressApp.models import EspecialidadCongreso,Congreso
from MedCongressAdmin.apps import validarUser
    

class EspEventoListView(validarUser,ListView):
    model = EspecialidadCongreso
    context_object_name = 'esp_eventos'
    template_name = 'nomencladores/esp_eventos/index.html'

class EspEventoCreateView(validarUser,CreateView):
    model=EspecialidadCongreso
    form_class = EspEventoForm
    success_url = reverse_lazy('MedCongressAdmin:esp_eventos_list')
    template_name = 'nomencladores/esp_eventos/form.html'


class EspEventoDeletedView(validarUser,DeleteView):
    model = EspecialidadCongreso
    success_url = reverse_lazy('MedCongressAdmin:esp_eventos_list')

    def delete(self,request, *args, **kwargs):
            
        especialidad=EspecialidadCongreso.objects.get(pk=self.kwargs.get('pk'))
       
        if Congreso.objects.filter(especialidad=especialidad).exists():
            return JsonResponse({'success':False}, safe=False)
        else:
            especialidad.delete()
            return JsonResponse({'success':True}, safe=False)

class EspEventoUpdateView(validarUser,UpdateView):
    form_class = EspEventoForm
    success_url = reverse_lazy('MedCongressAdmin:esp_eventos_list')
    template_name = 'nomencladores/esp_eventos/form.html'

    def get_queryset(self, **kwargs):
        return EspecialidadCongreso.objects.filter(pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['update']=True
        return context


