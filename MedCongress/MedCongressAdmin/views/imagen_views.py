from django import forms
from django.contrib import messages
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse_lazy,reverse
from django.views.generic import ListView,TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView,FormView
from MedCongressApp.models import ImagenCongreso,Congreso,Organizador
from MedCongressAdmin.forms.congres_forms import ImagenCongForms
from MedCongressAdmin.apps import validarUser,validarOrganizador
    
         
class ImagenesListView(validarOrganizador,TemplateView):
    template_name= 'MedCongressAdmin/imagen/listar.html' 
    

    def get(self, request, **kwargs):
        congreso=Congreso.objects.filter(path=self.kwargs.get('path')).first()
        if congreso is None:
            return   HttpResponseRedirect(reverse('Error404'))
        if not Organizador.objects.filter(user=self.request.user.perfilusuario,congreso=congreso).exists() and not self.request.user.is_staff: 
            return   HttpResponseRedirect(reverse('Error403'))
        return self.render_to_response(self.get_context_data())    
    def get_context_data(self, **kwargs):
        context = super(ImagenesListView, self).get_context_data(**kwargs)
        congreso=Congreso.objects.filter(path=self.kwargs.get('path')).first()
        context['congres']=congreso
        context['imagenes']=ImagenCongreso.objects.filter(congreso=congreso)
        return context    

class CongressImagenCreateView(validarOrganizador,FormView):
    form_class = ImagenCongForms
    success_url = reverse_lazy('MedCongressAdmin:Congres_imagenes')
    template_name = 'MedCongressAdmin/imagen_congress_form.html'

    def form_valid(self, form):
        imagen=form.save(commit=True)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super(CongressImagenCreateView, self).get_context_data(**kwargs)
        cong=Congreso.objects.filter(pk=self.kwargs.get('pk')).first()
        ctx['cong'] = cong
        return ctx
    def get_success_url(self):
        congreso=Congreso.objects.get(pk=self.kwargs.get('pk'))
        self.success_url =  reverse_lazy('MedCongressAdmin:Congres_imagenes',kwargs={'path': congreso.path} )
        return self.success_url
