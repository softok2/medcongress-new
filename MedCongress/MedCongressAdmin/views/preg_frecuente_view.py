from django import forms
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views.defaults import page_not_found
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.crypto import get_random_string
from django.views.generic import CreateView, ListView, TemplateView, UpdateView
from django.views.generic.edit import DeleteView, FormView
from MedCongressAdmin.forms.congres_forms import PregFrecuenteForm
from MedCongressApp.models import PreguntasFrecuentes,Congreso,Organizador
from MedCongressAdmin.apps import validarUser,validarOrganizador


class PregFrecuenteListView(validarOrganizador,TemplateView):
    template_name= 'MedCongressAdmin/pregunta_frecuente/listar.html' 
    def get(self, request, **kwargs):
        congreso=Congreso.objects.filter(path=self.kwargs.get('path')).first()
        if congreso is None:
            return   HttpResponseRedirect(reverse('Error404'))
        if not Organizador.objects.filter(user=self.request.user.perfilusuario,congreso=congreso).exists() and not self.request.user.is_staff: 
            return   HttpResponseRedirect(reverse('Error403'))
        return self.render_to_response(self.get_context_data()) 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        congreso=Congreso.objects.filter(path=self.kwargs.get('path')).first()
        preguntas_env=[]
        preguntas=PreguntasFrecuentes.objects.filter(congreso=congreso)
        context['preguntas']=preguntas
        context['congreso']=congreso
       
        return context

class  PregFrecuenteCreateView(validarOrganizador,CreateView):
    form_class =PregFrecuenteForm
    template_name = 'MedCongressAdmin/pregunta_frecuente/form.html'

    def get(self, request, **kwargs):
        self.object=PreguntasFrecuentes.objects.filter(pk=0).first()
        congreso=Congreso.objects.filter(path=self.kwargs.get('path')).first()
        if congreso is None:
            return   HttpResponseRedirect(reverse('Error404'))
        if not Organizador.objects.filter(user=self.request.user.perfilusuario,congreso=congreso).exists() and not self.request.user.is_staff: 
            return   HttpResponseRedirect(reverse('Error403'))
        return self.render_to_response(self.get_context_data())

    def get_success_url(self):
        if self.kwargs.get('path'):
            self.success_url =  reverse_lazy('MedCongressAdmin:Congres_freg_frecuente',kwargs={'path': self.kwargs.get('path')} )
        return self.success_url  
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        congreso=Congreso.objects.filter(path=self.kwargs.get('path')).first()
        context['congreso']=congreso
       
        return context

class PregFrecuenteUpdateView(validarOrganizador,UpdateView):
    form_class = PregFrecuenteForm
    template_name = 'MedCongressAdmin/pregunta_frecuente/form.html'

    def get(self, request, **kwargs):
        pregunta=PreguntasFrecuentes.objects.filter(pk=self.kwargs.get('pk')).first()
        self.object=pregunta
        if pregunta is None:
            return   HttpResponseRedirect(reverse('Error404'))
        if not Organizador.objects.filter(user=self.request.user.perfilusuario,congreso=pregunta.congreso).exists() and not self.request.user.is_staff: 
            return   HttpResponseRedirect(reverse('Error403'))
        return self.render_to_response(self.get_context_data())

    def get_queryset(self, **kwargs):
        return PreguntasFrecuentes.objects.filter(pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        pregunta=PreguntasFrecuentes.objects.get(pk=self.kwargs.get('pk'))
        context['congreso']=pregunta.congreso
        context['update']=True
        
        return context

    def get_success_url(self):

        self.success_url =  reverse_lazy('MedCongressAdmin:Congres_freg_frecuente',kwargs={'path': self.object.congreso.path} )
        return self.success_url 

class PregFrecuenteDeletView(validarOrganizador,DeleteView):
    model = PreguntasFrecuentes
    success_url = reverse_lazy('MedCongressAdmin:asig_congress_list')


