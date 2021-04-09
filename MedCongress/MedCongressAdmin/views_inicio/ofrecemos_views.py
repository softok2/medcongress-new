import base64 
from os import remove
from django import forms
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views.defaults import page_not_found
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import JsonResponse,HttpResponse
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
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        if self.request.GET.get('search'):
            context['search']=self.request.GET.get('search')
        context['ofrecemoss']=Ofrecemos.objects.all()
        return context

class OfrecemosCreateView(validarUser,CreateView):
    model=Ofrecemos
    form_class = OfrecemosForm
    success_url = reverse_lazy('MedCongressAdmin:ofrecemos_list')
    template_name = 'inicio/ofrecemos/form.html'
    def get_success_url(self):
        url =  reverse_lazy('MedCongressAdmin:ofrecemos_list')
        if self.request.GET.get('search'):
            self.success_url =  '%s?search=%s'%(url,self.request.GET.get('search'))
        else:
            self.success_url =  url
        return self.success_url

    def form_valid(self, form):
       
        imagen = form.save(commit=False)
       
        if self.request.POST['prueba']:
            image_64_encode=self.request.POST['prueba']
            campo = image_64_encode.split(",")
            chars = '0123456789'
            nombre = get_random_string(5, chars)
            image_64_decode = base64.decodestring(bytes(campo[1], encoding='utf8')) 
            image_result = open('MedCongressApp/static/assets/img/iconos/icono_%s.png'%(nombre), 'wb') # create a writable image and write the decoding result
            image_result.write(image_64_decode)
            imagen.icono='assets/img/iconos/icono_%s.png'%(nombre)

        imagen.save() 
        return super(OfrecemosCreateView, self).form_valid(form)
class OfrecemosDeletedView(validarUser,DeleteView):
    model = Ofrecemos
    success_url = reverse_lazy('MedCongressAdmin:ofrecemos_list')
    def delete(self,request, *args, **kwargs):
            
        imagen=Ofrecemos.objects.get(pk=self.kwargs.get('pk'))
        if imagen.icono:
            remove('MedCongressApp/static/%s'%( imagen.icono))
        imagen.delete()
        return JsonResponse({'success':True}, safe=False)

class OfrecemosUpdateView(validarUser,UpdateView):
    form_class = OfrecemosForm
    success_url = reverse_lazy('MedCongressAdmin:ofrecemos_list')
    template_name = 'inicio/ofrecemos/form.html'

    def get_queryset(self, **kwargs):
        return Ofrecemos.objects.filter(pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        ofrecemos= Ofrecemos.objects.get(pk=self.kwargs.get('pk'))
        context['update']=True
        context['icono']=ofrecemos.icono
        return context
    def get_success_url(self):
        url = reverse_lazy('MedCongressAdmin:ofrecemos_list')
        self.success_url =  '%s?search=%s'%(url,self.request.GET.get('search'))
       
        return self.success_url

    def form_valid(self, form):
        ofrecemos= Ofrecemos.objects.get(pk=self.kwargs.get('pk'))
        imagen = form.save(commit=False) 
        if self.request.POST['prueba']:
            icono=self.request.POST['prueba']
            if 'esset/' not in icono:
            
                image_64_encode=self.request.POST['prueba']
                campo = image_64_encode.split(",")
                chars = '0123456789'
                nombre = get_random_string(5, chars)
                image_64_decode = base64.decodestring(bytes(campo[1], encoding='utf8'))
                image_result = open('MedCongressApp/static/assets/img/iconos/icono_%s.png'%(nombre), 'wb') # create a writable image and write the decoding result
                image_result.write(image_64_decode)
                if  ofrecemos.icono:
                    remove('MedCongressApp/static/%s'%( ofrecemos.icono))
                imagen.icono='assets/img/iconos/icono_%s.png'%(nombre)   
        imagen.save()     
            
           
        return super(OfrecemosUpdateView, self).form_valid(form)