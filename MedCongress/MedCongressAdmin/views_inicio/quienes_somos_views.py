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
from MedCongressAdmin.forms.inicio_forms import QuienesSomosForm,ImagenQuienesSomosForms
from MedCongressApp.models import QuienesSomos, ImagenQuienesSomos
from MedCongressAdmin.apps import validarUser
    

class QuienesSomosListView(validarUser,ListView):
    model = QuienesSomos
    context_object_name = 'quienes_somoss'
    template_name = 'inicio/quienes_somos/index.html'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['imagenes']=ImagenQuienesSomos.objects.all()
        return context

class QuienesSomosCreateView(validarUser,CreateView):
    model=QuienesSomos
    form_class = QuienesSomosForm
    success_url = reverse_lazy('MedCongressAdmin:quienes_somos_list')
    template_name = 'inicio/quienes_somos/form.html'
class QuienesSomosUpdateView(validarUser,UpdateView):
    form_class = QuienesSomosForm
    success_url = reverse_lazy('MedCongressAdmin:quienes_somos_list')
    template_name = 'inicio/quienes_somos/form.html'

    def get_queryset(self, **kwargs):
        return QuienesSomos.objects.filter(pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['update']=True
        return context

    
class QuienesSomosImagenCreateView(validarUser,FormView):
    form_class = ImagenQuienesSomosForms
    success_url = reverse_lazy('MedCongressAdmin:quienes_somos_list')
    template_name = 'inicio/quienes_somos/form_imagen.html'

    def form_valid(self, form):
       
        q_somos = form.save(commit=False)
        image_64_encode=self.request.POST['prueba']
        campo = image_64_encode.split(",")
        image_64_decode = base64.decodestring(bytes(campo[1], encoding='utf8')) 
        chars = '0123456789'
        nombre = get_random_string(5, chars)
        image_result = open('MedCongressApp/static/congreso/imagen_%s.png'%(nombre), 'wb') # create a writable image and write the decoding result
        image_result.write(image_64_decode)
        q_somos.imagen='congreso/imagen_%s.png'%(nombre)
        q_somos.save() 
        return super(QuienesSomosImagenCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super(QuienesSomosImagenCreateView, self).get_context_data(**kwargs)
        cong=QuienesSomos.objects.filter().first()
        ctx['cong'] = cong
        return ctx

class QuienesSomosImagenDeletedView(validarUser,DeleteView):
    model = ImagenQuienesSomos
    success_url = reverse_lazy('MedCongressAdmin:cat_usuarios_list')
    def delete(self,request, *args, **kwargs):
            
        imagen=ImagenQuienesSomos.objects.get(pk=self.kwargs.get('pk'))
        if imagen.imagen:
            remove('MedCongressApp/static/%s'%( imagen.imagen))
        imagen.delete()
        return JsonResponse({'success':True}, safe=False)