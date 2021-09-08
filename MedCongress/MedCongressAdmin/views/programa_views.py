from django import forms
import base64
from django.contrib import messages
from os import remove
from pathlib import Path
from django.shortcuts import get_object_or_404
from django.views.defaults import page_not_found
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.http import JsonResponse
from django.utils.crypto import get_random_string
from django.views.generic import CreateView, ListView, TemplateView
from django.views.generic.edit import DeleteView, FormView, UpdateView
from MedCongressAdmin.forms.congres_forms import CongresoProgramaForm
from MedCongressApp.models import DocumentoPrograma, Congreso, Ponencia, Taller, RelBloqueModerador,Moderador,Organizador,Sala
from MedCongressAdmin.apps import validarUser,validarOrganizador
    
class ProgramaListView(validarOrganizador,TemplateView):
    template_name= 'MedCongressAdmin/programa/listar.html' 
    

    def get(self, request, **kwargs):
        congreso=Congreso.objects.filter(path=self.kwargs.get('path')).first()
        if congreso is None:
            return   HttpResponseRedirect(reverse('Error404'))
        if not Organizador.objects.filter(user=self.request.user.perfilusuario,congreso=congreso).exists() and not self.request.user.is_staff: 
            return   HttpResponseRedirect(reverse('Error403'))
        return self.render_to_response(self.get_context_data())    
    def get_context_data(self, **kwargs):
        context = super(ProgramaListView, self).get_context_data(**kwargs)
        congreso=Congreso.objects.filter(path=self.kwargs.get('path')).first()
        context['congres']=congreso
        context['programas']=DocumentoPrograma.objects.filter(congreso=congreso)
        return context        
 
class  ProgramaCreateView(validarOrganizador,CreateView):
    info_sended =Congreso()
    form_class = CongresoProgramaForm
    # success_url = reverse_lazy('MedCongressAdmin:ponencias_list')
    template_name = 'MedCongressAdmin/programa/form.html'
    def form_valid(self, form):
        congreso=form.save(commit=False)
  
        congreso.save()
        return super(ProgramaCreateView, self).form_valid(form)

    def get_success_url(self):
           self.success_url =  reverse_lazy('MedCongressAdmin:Congres_programas',kwargs={'path': self.kwargs.get('path')} )
           return self.success_url

    def get_context_data(self, **kwargs):
        ctx = super(ProgramaCreateView, self).get_context_data(**kwargs)
        pon=Congreso.objects.filter(path=self.kwargs.get('path')).first()
        ctx['cong'] = pon
        return ctx
    def get(self, request, **kwargs):
        congreso=Congreso.objects.filter(path=self.kwargs.get('path')).first()
        self.object= congreso
        if congreso is None:
            return   HttpResponseRedirect(reverse('Error404'))
        if not Organizador.objects.filter(user=self.request.user.perfilusuario,congreso=congreso).exists() and not self.request.user.is_staff: 
            return   HttpResponseRedirect(reverse('Error403'))
        return self.render_to_response(self.get_context_data())   

class ProgramaUpdateView(validarOrganizador,UpdateView):

    form_class = CongresoProgramaForm
    template_name = 'MedCongressAdmin/programa/form.html'

    def get_queryset(self, **kwargs):
        return DocumentoPrograma.objects.filter(pk=self.kwargs.get('pk'))

    def form_valid(self, form):
        congreso=form.save(commit=False)
  
        congreso.save()
        return super(ProgramaUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['update']=True
        context['programa']= self.object
        context['cong'] = self.object.congreso
        return context
    def get_success_url(self):
           self.success_url =  reverse_lazy('MedCongressAdmin:Congres_programas',kwargs={'path': self.object.congreso.path} )
           return self.success_url

    def get(self, request, **kwargs):
        doc=DocumentoPrograma.objects.filter(pk=self.kwargs.get('pk')).first()
        self.object= doc
        if doc is None:
            return   HttpResponseRedirect(reverse('Error404'))
        if not Organizador.objects.filter(user=self.request.user.perfilusuario,congreso=doc.congreso).exists() and not self.request.user.is_staff: 
            return   HttpResponseRedirect(reverse('Error403'))
        return self.render_to_response(self.get_context_data())  

class ProgramaDeletedView(validarOrganizador,DeleteView):
    model = DocumentoPrograma
    success_url = reverse_lazy('MedCongressAdmin:cat_usuarios_list')
