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
from MedCongressAdmin.forms.congres_forms import CongresoCategPagoForm
from MedCongressApp.models import PreguntasFrecuentes,Congreso,Organizador,RelCongresoCategoriaPago
from MedCongressAdmin.apps import validarUser,validarOrganizador

class CategPagosListView(validarOrganizador,TemplateView):
    template_name= 'MedCongressAdmin/boleto/listar.html' 
    

    def get(self, request, **kwargs):
        congreso=Congreso.objects.filter(path=self.kwargs.get('path')).first()
        if congreso is None:
            return   HttpResponseRedirect(reverse('Error404'))
        if not Organizador.objects.filter(user=self.request.user.perfilusuario,congreso=congreso).exists() and not self.request.user.is_staff: 
            return   HttpResponseRedirect(reverse('Error403'))
        return self.render_to_response(self.get_context_data())    
    def get_context_data(self, **kwargs):
        context = super(CategPagosListView, self).get_context_data(**kwargs)
        congreso=Congreso.objects.filter(path=self.kwargs.get('path')).first()
        context['congres']=congreso
        context['cat_pagos']=RelCongresoCategoriaPago.objects.filter(congreso=congreso)
        return context        
        

class  CongressCategPagosCreateView(validarOrganizador,CreateView):
    info_sended =Congreso()
    form_class = CongresoCategPagoForm
    template_name = 'MedCongressAdmin/boleto/form.html'

    def get(self, request, **kwargs):
        congreso=Congreso.objects.filter(path=self.kwargs.get('path')).first()
        boleto=RelCongresoCategoriaPago.objects.filter(pk=0).first()
        self.object=boleto
        if congreso is None:
            return   HttpResponseRedirect(reverse('Error404'))
        if not Organizador.objects.filter(user=self.request.user.perfilusuario,congreso=congreso).exists() and not self.request.user.is_staff: 
            return   HttpResponseRedirect(reverse('Error403'))
        return self.render_to_response(self.get_context_data())  
   
    def form_valid(self, form):
        congreso=form.save(commit=False)
  
        congreso.save()
        return super(CongressCategPagosCreateView, self).form_valid(form)

    def get_success_url(self):
           self.success_url =  reverse_lazy('MedCongressAdmin:Congres_pagos',kwargs={'path': self.kwargs.get('path')} )
           return self.success_url

    def get_context_data(self, **kwargs):
        ctx = super(CongressCategPagosCreateView, self).get_context_data(**kwargs)
        congreso=Congreso.objects.filter(path=self.kwargs.get('path')).first()
        ctx['cong'] = congreso
        return ctx

    
class CongressCategPagosUpdateView(validarOrganizador,UpdateView):

    form_class = CongresoCategPagoForm
    success_url = reverse_lazy('MedCongressAdmin:ponencias_list')
    template_name = 'MedCongressAdmin/boleto/form.html'

    def get(self, request, **kwargs):
        
        boleto=RelCongresoCategoriaPago.objects.filter(pk=self.kwargs.get('pk')).first()
        self.object=boleto
        if boleto is None:
            return   HttpResponseRedirect(reverse('Error404'))
        if not Organizador.objects.filter(user=self.request.user.perfilusuario,congreso=boleto.congreso).exists() and not self.request.user.is_staff: 
            return   HttpResponseRedirect(reverse('Error403'))
        return self.render_to_response(self.get_context_data())  
   
    def get_queryset(self, **kwargs):
        return RelCongresoCategoriaPago.objects.filter(pk=self.kwargs.get('pk'))


    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['update']=True
        context['categoria']= RelCongresoCategoriaPago.objects.get(pk=self.kwargs.get('pk'))
        context['cong'] = context['categoria'].congreso
        return context

    def get_success_url(self):
           self.success_url =  reverse_lazy('MedCongressAdmin:Congres_pagos',kwargs={'path': self.object.congreso.path} )
           return self.success_url

class CongressCategPagosDeletedView(validarOrganizador,DeleteView):
    model = RelCongresoCategoriaPago
    success_url = reverse_lazy('MedCongressAdmin:cat_usuarios_list')

