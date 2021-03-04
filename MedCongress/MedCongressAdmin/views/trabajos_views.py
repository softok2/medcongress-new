from os import remove
from django import forms
from django.contrib import messages
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse_lazy,reverse
from django.views.generic import ListView,CreateView,TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.edit import  DeleteView, UpdateView,FormView
from MedCongressApp.models import TrabajosInvestigacion,Congreso
from MedCongressAdmin.forms.congres_forms import CongresoTrabajoForm
from MedCongressAdmin.apps import validarUser
from django.http import JsonResponse
from  MedCongressApp.claves import URL_SITE


class TrabajosListView(validarUser,TemplateView):
    template_name = 'MedCongressAdmin/trabajos_list.html'


    def get(self, request, **kwargs):
        congreso=Congreso.objects.filter(path=self.kwargs.get('path')).first()
        if congreso is None:
            return   HttpResponseRedirect(reverse('Error404'))
        return self.render_to_response(self.get_context_data())    
    def get_context_data(self, **kwargs):
        context = super(TrabajosListView, self).get_context_data(**kwargs)
        congreso=Congreso.objects.filter(path=self.kwargs.get('path')).first()
        context['congres']=congreso
        context['trabajos']=TrabajosInvestigacion.objects.filter(congreso=congreso)
        return context  

class  CongressTrabajoCreateView(validarUser,CreateView):
    info_sended =Congreso()
    form_class = CongresoTrabajoForm
    # success_url = reverse_lazy('MedCongressAdmin:ponencias_list')
    template_name = 'MedCongressAdmin/congreso_trabajo_form.html'
    def form_valid(self, form):
        congreso=form.save(commit=False)
  
        congreso.save()
        return super(CongressTrabajoCreateView, self).form_valid(form)

    def get_success_url(self):
           self.success_url =  reverse_lazy('MedCongressAdmin:Congres_trabajos',kwargs={'path': self.kwargs.get('path')} )
           return self.success_url

    def get_context_data(self, **kwargs):
        ctx = super(CongressTrabajoCreateView, self).get_context_data(**kwargs)
        pon=Congreso.objects.filter(path=self.kwargs.get('path')).first()
        ctx['cong'] = pon
        return ctx

        
class CongressTrabajoUpdateView(validarUser,UpdateView):

    form_class = CongresoTrabajoForm
    template_name = 'MedCongressAdmin/congreso_trabajo_form.html'

    def get_queryset(self, **kwargs):
        return TrabajosInvestigacion.objects.filter(pk=self.kwargs.get('pk'))

    def form_valid(self, form):
        congreso=form.save(commit=False)
  
        congreso.save()
        return super(CongressTrabajoUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['update']=True
        trabajo=TrabajosInvestigacion.objects.get(pk=self.kwargs.get('pk'))
        context['trabajo']= trabajo
        context['foto']= trabajo.foto
        pon=Congreso.objects.filter(path=self.kwargs.get('path')).first()
        context['cong'] = pon
        return context
    def get_success_url(self):
           self.success_url =  reverse_lazy('MedCongressAdmin:Congres_trabajos',kwargs={'path': self.kwargs.get('path')} )
           return self.success_url
    