from django import forms
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views.defaults import page_not_found
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.crypto import get_random_string
from django.views.generic import CreateView, ListView, TemplateView
from django.views.generic.edit import DeleteView, FormView, UpdateView
from MedCongressAdmin.forms.congres_forms import CuestionarioForms,PreguntaForm
from MedCongressApp.models import CuestionarioPregunta,CuestionarioRespuestas,Congreso
from MedCongressAdmin.apps import validarUser
    

class CuestionarioListView(validarUser,ListView):
    model = CuestionarioPregunta
    context_object_name = 'cuestionarios'
    template_name = 'MedCongressAdmin/cuestionarios.html'


class PreguntaCreateView(validarUser,FormView):
    form_class = PreguntaForm
    success_url = reverse_lazy('MedCongressAdmin:ponencias_list')
    template_name = 'MedCongressAdmin/cuestionario_form.html'

    def form_valid(self, form):
        pregunta=form.save(commit=True)
        
        cant=0
        for respuesta in self.request.POST.getlist('respuesta'):
            resp=CuestionarioRespuestas(pregunta=pregunta,respuesta=respuesta,published=self.request.POST.getlist('published_resp')[cant],is_correcto=self.request.POST.getlist('is_correcto')[cant])
            resp.save() 
            cant=cant+1  
        return super(PreguntaCreateView, self).form_valid(form)
    
    def get_success_url(self):
        if self.kwargs.get('path'):
            congreso=Congreso.objects.filter(path=self.kwargs.get('path')).first()
            self.success_url =  reverse_lazy('MedCongressAdmin:Congres_cuestionario',kwargs={'path': congreso.path} )
        return self.success_url  
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        congreso=Congreso.objects.filter(path=self.kwargs.get('path'),published=True).first()
        context['congreso']=congreso
       
        return context

class CustionarioUpdateView(validarUser,FormView):
    form_class = PreguntaForm
    success_url = reverse_lazy('MedCongressAdmin:ponencias_list')
    template_name = 'MedCongressAdmin/cuestionario_form.html'



    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        pregunta=CuestionarioPregunta.objects.get(pk=self.kwargs.get('pk'))
        context['respuestas']=CuestionarioRespuestas.objects.filter(pregunta=pregunta)
        context['congreso']=pregunta.congreso
        context['pregunta']=pregunta
        return context
    def form_valid(self, form):
        
        pregunta =CuestionarioPregunta.objects.get(pk=self.request.POST['update'])   
        pregunta.pregunta=self.request.POST['pregunta']
        pregunta.published=self.request.POST['published']
        pregunta.save()
        CuestionarioRespuestas.objects.filter(pregunta=pregunta).delete()
        cant=0
        for respuesta in self.request.POST.getlist('respuesta'):
            resp=CuestionarioRespuestas(pregunta=pregunta,respuesta=respuesta,published=self.request.POST.getlist('published_resp')[cant],is_correcto=self.request.POST.getlist('is_correcto')[cant])
            resp.save() 
            cant=cant+1  
        return super(CustionarioUpdateView, self).form_valid(form)
    def get_initial(self):
        initial=super().get_initial()
        pregunta=CuestionarioPregunta.objects.get(pk=self.kwargs.get('pk'))
        initial['pregunta']=pregunta.pregunta
        initial['published']=pregunta.published
        return initial

    def get_success_url(self):
        if self.kwargs.get('pk'):
            pregunta=CuestionarioPregunta.objects.get(pk=self.kwargs.get('pk'))
            
            self.success_url =  reverse_lazy('MedCongressAdmin:Congres_cuestionario',kwargs={'path': pregunta.congreso.path} )
        return self.success_url 

class CustionarioDeletedView(validarUser,DeleteView):
    model = CuestionarioPregunta
    success_url = reverse_lazy('MedCongressAdmin:asig_congress_list')