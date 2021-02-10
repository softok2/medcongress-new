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
from MedCongressAdmin.forms.nomencladores_forms import IdiomaForm
from MedCongressApp.models import Idioma,DocumentoPrograma
from MedCongressAdmin.apps import validarUser
    

class IdiomaListView(validarUser,ListView):
    model = Idioma
    context_object_name = 'idiomas'
    template_name = 'nomencladores/idioma/index.html'

class IdiomaCreateView(validarUser,CreateView):
    model=Idioma
    form_class = IdiomaForm
    success_url = reverse_lazy('MedCongressAdmin:idiomas_list')
    template_name = 'nomencladores/idioma/form.html'
    
    def form_valid(self, form):

        idioma=form.save(commit=False)       
       
        idioma.save()
        return super().form_valid(form)

class IdiomaDeletedView(validarUser,DeleteView):
    model = Idioma
    

    def delete(self,request, *args, **kwargs):
           
            idioma=Idioma.objects.get(pk=self.kwargs.get('pk'))
            if DocumentoPrograma.objects.filter(idioma= idioma).exists():
                return JsonResponse({'success':False}, safe=False)
            else:
                idioma.delete()
                return JsonResponse({'success':True}, safe=False)

class IdiomaUpdateView(validarUser,UpdateView):
    form_class = IdiomaForm
    success_url = reverse_lazy('MedCongressAdmin:idiomas_list')
    template_name = 'nomencladores/idioma/form.html'

    def get_queryset(self, **kwargs):
        return Idioma.objects.filter(pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['update']=True
        return context

    
