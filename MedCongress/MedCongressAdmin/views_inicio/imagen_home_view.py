from django import forms
import base64 
from os import remove
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views.defaults import page_not_found
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
from django.utils.crypto import get_random_string
from django.views.generic import CreateView, ListView, TemplateView
from django.views.generic.edit import DeleteView, FormView, UpdateView
from MedCongressAdmin.forms.inicio_forms import ImagenHomeForm
from MedCongressApp.models import ImagenHome
from MedCongressAdmin.apps import validarUser
    

class ImagenListView(validarUser,ListView):
    model = ImagenHome
    context_object_name = 'imagenes'
    template_name = 'inicio/imagen/index.html'

class ImagenCreateView(validarUser,CreateView):
   
    form_class = ImagenHomeForm
    success_url = reverse_lazy('MedCongressAdmin:imagen_list')
    template_name = 'inicio/imagen/form.html'

    def form_valid(self, form):
       
        imagen = form.save(commit=False)
       
        if self.request.POST['prueba']:
            image_64_encode=self.request.POST['prueba']
            campo = image_64_encode.split(",")
            image_64_decode = base64.decodestring(bytes(campo[1], encoding='utf8')) 
            image_result = open('MedCongressApp/static/congreso/imagen_home.png', 'wb') # create a writable image and write the decoding result
            image_result.write(image_64_decode)
            imagen.imagen='congreso/imagen_home.png'
        else:
            imagen.imagen='congreso/imagen1920X1080.png'

        imagen.save() 
        return super(ImagenCreateView, self).form_valid(form)

class ImagenDeletedView(validarUser,DeleteView):
    model = ImagenHome
    success_url = reverse_lazy('MedCongressAdmin:imagen_list')
    def delete(self,request, *args, **kwargs):
            
        imagen=ImagenHome.objects.get(pk=self.kwargs.get('pk'))
        if imagen.imagen:
            remove('MedCongressApp/static/%s'%( imagen.imagen))
        imagen.delete()
        return JsonResponse({'success':True}, safe=False)

class ImagenUpdateView(validarUser,UpdateView):
    form_class = ImagenHomeForm
    success_url = reverse_lazy('MedCongressAdmin:imagen_list')
    template_name = 'inicio/imagen/form.html'

    def get_queryset(self, **kwargs):
        return ImagenHome.objects.filter(pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['update']=True
        context['imagen']=ImagenHome.objects.get(pk=self.kwargs.get('pk')).imagen
        return context
    def form_valid(self, form):
       
        imagen = form.save(commit=False)

        
        image_64_encode=self.request.POST['prueba']
        campo = image_64_encode.split(",")
        chars = '0123456789'
        nom= get_random_string(3, chars)
        image_64_decode = base64.decodestring(bytes(campo[1], encoding='utf8'))
        image_result = open('MedCongressApp/static/congreso/imagen_home_%s.png'%(nom), 'wb') # create a writable image and write the decoding result
        image_result.write(image_64_decode)
        if imagen.imagen:
            remove('MedCongressApp/static/%s'%( imagen.imagen))
        imagen.imagen='congreso/imagen_home_%s.png'%(nom)
        imagen.save()     
            
           
        return super(ImagenUpdateView, self).form_valid(form)

