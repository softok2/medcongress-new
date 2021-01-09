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
from MedCongressAdmin.forms.inicio_forms import OfrecemosForm
from MedCongressApp.models import Ofrecemos
from MedCongressAdmin.apps import validarUser
    

class OfrecemosListView(validarUser,ListView):
    model = Ofrecemos
    context_object_name = 'ofrecemoss'
    template_name = 'inicio/ofrecemos/index.html'

class OfrecemosCreateView(validarUser,CreateView):
    model=Ofrecemos
    form_class = OfrecemosForm
    success_url = reverse_lazy('MedCongressAdmin:ofrecemos_list')
    template_name = 'inicio/ofrecemos/form.html'
    
class OfrecemosDeletedView(validarUser,DeleteView):
    model = Ofrecemos
    success_url = reverse_lazy('MedCongressAdmin:ofrecemos_list')

class OfrecemosUpdateView(validarUser,UpdateView):
    form_class = OfrecemosForm
    success_url = reverse_lazy('MedCongressAdmin:ofrecemos_list')
    template_name = 'inicio/ofrecemos/form.html'

    def get_queryset(self, **kwargs):
        return Ofrecemos.objects.filter(pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['update']=True
        return context


