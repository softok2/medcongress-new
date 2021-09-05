from django import forms
from django.contrib import messages
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse_lazy,reverse
from django.views.generic import ListView,TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from MedCongressApp.models import ImagenCongreso,Congreso,Organizador
from MedCongressAdmin.forms.congres_forms import ImagenCongresoForms
from MedCongressAdmin.apps import validarUser,validarOrganizador
    


class ImagenCreateView(validarUser,CreateView):
    form_class = ImagenCongresoForms
    success_url = reverse_lazy('MedCongressAdmin:congress_list')
    template_name = 'MedCongressAdmin/congres_form.html'

    def post(self, request, **kwargs):
        if request.is_ajax:
            query =request.FILES
            
            imagen=ImagenCongreso(imagen=query)
            imagen.save()
            

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
