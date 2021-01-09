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
from MedCongressAdmin.forms.nomencladores_forms import CatUsuarioForm
from MedCongressApp.models import CategoriaUsuario,PerfilUsuario
from MedCongressAdmin.apps import validarUser
    

class CatUsuarioListView(validarUser,ListView):
    model = CategoriaUsuario
    context_object_name = 'cat_usuarios'
    template_name = 'nomencladores/cat_usuarios/index.html'

class CatUsuarioCreateView(validarUser,CreateView):
    model=CategoriaUsuario
    form_class = CatUsuarioForm
    success_url = reverse_lazy('MedCongressAdmin:cat_usuarios_list')
    template_name = 'nomencladores/cat_usuarios/form.html'
    
   

class CatUsuarioDeletedView(validarUser,DeleteView):
    model = CategoriaUsuario
    success_url = reverse_lazy('MedCongressAdmin:cat_usuarios_list')

    def delete(self,request, *args, **kwargs):
            
        categoria=CategoriaUsuario.objects.get(pk=self.kwargs.get('pk'))
        
        if PerfilUsuario.objects.filter(categoria=categoria).exists():
            return JsonResponse({'success':False}, safe=False)
        else:
            categoria.delete()
            return JsonResponse({'success':True}, safe=False)

class CatUsuarioUpdateView(validarUser,UpdateView):
    form_class = CatUsuarioForm
    success_url = reverse_lazy('MedCongressAdmin:cat_usuarios_list')
    template_name = 'nomencladores/cat_usuarios/form.html'

    def get_queryset(self, **kwargs):
        return CategoriaUsuario.objects.filter(pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['update']=True
        return context


