from django import forms
from django.contrib import messages
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView,TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from MedCongressApp.models import Taller,RelTalleresCategoriaPago
from MedCongressAdmin.forms.congres_forms import TallerForms,TallerCategPagoForm

class validarUser(UserPassesTestMixin):
    permission_denied_message = 'No tiene permiso para acceder a la administracion'
    login_url='/admin/login/'
    def test_func(self):
       
        if self.request.user.is_staff :
            return True
        else:
            return False
    

class TalleresListView(validarUser,ListView):
    model = Taller
    context_object_name = 'talleres'
    template_name = 'MedCongressAdmin/talleres.html'

class  TallerCreateView(validarUser,CreateView):
    form_class = TallerForms
    success_url = reverse_lazy('MedCongressAdmin:talleres_list')
    template_name = 'MedCongressAdmin/taller_form.html'

    def form_valid(self, form):
       
        taller=form['taller'].save(commit=False)
        
        ubicacion= form['ubicacion'].save(commit=True)
        print(ubicacion)
        path=taller.titulo.replace("/","").replace(" ","-").replace("?","").replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("ñ","n")
        chars = '0123456789'
        secret_key = get_random_string(5, chars)
        taller.path=path+secret_key
        taller.lugar=ubicacion
        taller.save()
       
        return super(TallerCreateView, self).form_valid(form)


########## Vista de las Categorias de Pago de un Congreso #############

class TallerCategPagosListView(TemplateView):
    template_name= 'MedCongressAdmin/taller_cat_pagos.html' 
    

    def get(self, request, **kwargs):
        taller=Taller.objects.filter(path=self.kwargs.get('path'),published=True).first()
        if taller is None:
            return   HttpResponseRedirect(reverse('Error404'))
        return self.render_to_response(self.get_context_data())    
    def get_context_data(self, **kwargs):
        context = super(TallerCategPagosListView, self).get_context_data(**kwargs)
        taller=Taller.objects.filter(path=self.kwargs.get('path'),published=True).first()
        context['congres']=taller
        context['cat_pagos']=RelTalleresCategoriaPago.objects.filter(taller=taller)
        return context        
        
class  TallerCategPagosCreateView(validarUser,CreateView):
    info_sended =Taller()
    form_class = TallerCategPagoForm
    # success_url = reverse_lazy('MedCongressAdmin:ponencias_list')
    template_name = 'MedCongressAdmin/taller_cat_pago_form.html'
    def form_valid(self, form):
        congreso=form.save(commit=False)
  
        congreso.save()
        return super(TallerCategPagosCreateView, self).form_valid(form)

    def get_success_url(self):
           self.success_url =  reverse_lazy('MedCongressAdmin:Taller_pagos',kwargs={'path': self.kwargs.get('path')} )
           return self.success_url

    def get_context_data(self, **kwargs):
        ctx = super(TallerCategPagosCreateView, self).get_context_data(**kwargs)
        pon=Taller.objects.filter(path=self.kwargs.get('path'),published=True).first()
        ctx['cong'] = pon
        return ctx



