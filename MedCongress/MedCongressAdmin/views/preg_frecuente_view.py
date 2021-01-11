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
from MedCongressApp.models import PreguntasFrecuentes,Congreso
from MedCongressAdmin.apps import validarUser


class  PregFrecuenteCreateView(validarUser,CreateView):
    form_class =PregFrecuenteForm
    template_name = 'MedCongressAdmin/preg_frecuente_form.html'


    def get_success_url(self):
        if self.kwargs.get('path'):
            self.success_url =  reverse_lazy('MedCongressAdmin:Congres_freg_frecuente',kwargs={'path': self.kwargs.get('path')} )
        return self.success_url  
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        congreso=Congreso.objects.filter(path=self.kwargs.get('path'),published=True).first()
        context['congreso']=congreso
       
        return context

class PregFrecuenteUpdateView(validarUser,UpdateView):
    form_class = PregFrecuenteForm
    template_name = 'MedCongressAdmin/preg_frecuente_form.html'

    def get_queryset(self, **kwargs):
        return PreguntasFrecuentes.objects.filter(pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        pregunta=PreguntasFrecuentes.objects.get(pk=self.kwargs.get('pk'))
        context['congreso']=pregunta.congreso
        context['update']=True
        
        return context
    # def form_valid(self, form):
        
    #     pregunta =CuestionarioPregunta.objects.get(pk=self.request.POST['update'])   
    #     pregunta.pregunta=self.request.POST['pregunta']
    #     pregunta.published=self.request.POST['published']
    #     pregunta.save()
    #     CuestionarioRespuestas.objects.filter(pregunta=pregunta).delete()
    #     cant=0
    #     for respuesta in self.request.POST.getlist('respuesta'):
    #         resp=CuestionarioRespuestas(pregunta=pregunta,respuesta=respuesta,published=self.request.POST.getlist('published_resp')[cant],is_correcto=self.request.POST.getlist('is_correcto')[cant])
    #         resp.save() 
    #         cant=cant+1  
    #     return super(CustionarioUpdateView, self).form_valid(form)
    # def get_initial(self):
    #     initial=super().get_initial()
    #     pregunta=CuestionarioPregunta.objects.get(pk=self.kwargs.get('pk'))
    #     initial['pregunta']=pregunta.pregunta
    #     initial['published']=pregunta.published
    #     return initial

    def get_success_url(self):
        if self.kwargs.get('pk'):
            pregunta=PreguntasFrecuentes.objects.get(pk=self.kwargs.get('pk'))
            
            self.success_url =  reverse_lazy('MedCongressAdmin:Congres_freg_frecuente',kwargs={'path': pregunta.congreso.path} )
        return self.success_url 

class PregFrecuenteDeletView(validarUser,DeleteView):
    model = PreguntasFrecuentes
    success_url = reverse_lazy('MedCongressAdmin:asig_congress_list')


