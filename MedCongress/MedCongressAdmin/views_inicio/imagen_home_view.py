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
from MedCongressAdmin.forms.inicio_forms import ImagenHomeForm
from MedCongressApp.models import ImagenHome
from MedCongressAdmin.apps import validarUser
    

class ImagenListView(validarUser,ListView):
    model = ImagenHome
    context_object_name = 'imagenes'
    template_name = 'inicio/imagen/index.html'

class ImagenCreateView(validarUser,CreateView):
   
    form_class = ImagenHomeForm
    success_url = reverse_lazy('MedCongressAdmin:imagen_list')
    template_name = 'inicio/imagen/form.html'
    
class ImagenDeletedView(validarUser,DeleteView):
    model = ImagenHome
    success_url = reverse_lazy('MedCongressAdmin:imagen_list')

class ImagenUpdateView(validarUser,UpdateView):
    form_class = ImagenHomeForm
    success_url = reverse_lazy('MedCongressAdmin:imagen_list')
    template_name = 'inicio/imagen/form.html'

    def get_queryset(self, **kwargs):
        return ImagenHome.objects.filter(pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['update']=True
        context['imagen']=ImagenHome.objects.get(pk=self.kwargs.get('pk')).imagen
        return context


