import base64 
from os import remove
from pathlib import Path
from django.utils.crypto import get_random_string
from django import forms
from django.contrib import messages
from django.http import HttpResponseBadRequest, HttpResponseRedirect,JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from MedCongressApp.models import Pais
from MedCongressAdmin.apps import validarUser
    

class CountryListView(validarUser,ListView):
    model = Pais
    context_object_name = 'countries'
    template_name = 'MedCongressAdmin/country.html'


class CountryForm(validarUser,forms.ModelForm):
    prueba=forms.CharField(required=False)
    class Meta:
        model = Pais
        fields = ['denominacion','prueba']
        widgets = {'denominacion': forms.TextInput(
            attrs={'class': 'form-control'})}
        error_messages = {
            'denominacion':{
                'unique': 'Este <b>País</b> ya esta registrado.'
            },
        }
    def clean(self, *args, **kwargs):
        cleaned_data = super(CountryForm, self).clean(*args, **kwargs)
        banderas = cleaned_data.get('prueba', None)
        if not banderas :
            self.add_error('prueba', 'Debe  entrar una <b>Bandera</b>')


class CountryCreateView(validarUser,CreateView):
    form_class = CountryForm
    success_url = reverse_lazy('MedCongressAdmin:country_list')
    template_name = 'MedCongressAdmin/country_form.html'

    def get_context_data(self, **kwargs):
        context = super(CountryCreateView, self).get_context_data(**kwargs)
        context['form_title'] = 'Nuevo'
        return context

    

    def form_valid(self, form):
        pais=form.save(commit=False)
        
        image_64_encode=self.request.POST['prueba']
        campo = image_64_encode.split(",")
        image_64_decode = base64.decodestring(bytes(campo[1], encoding='utf8')) 
        chars = '0123456789'
        nombre = get_random_string(5, chars)
        image_result = open('MedCongressApp/static/banderas/imagen_%s.png'%(nombre), 'wb') # create a writable image and write the decoding result
        image_result.write(image_64_decode)
        pais.banderas='banderas/imagen_%s.png'%(nombre)
        pais.save()
        return super().form_valid(form)


class CountryUpdateView(validarUser,UpdateView):
    form_class = CountryForm
    success_url = reverse_lazy('MedCongressAdmin:country_list')
    template_name = 'MedCongressAdmin/country_form.html'

    def get_queryset(self, **kwargs):
        return Pais.objects.filter(pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super(CountryUpdateView, self).get_context_data(**kwargs)
        context['update'] = True
        if self.object.banderas:
            context['banderas']='/static/%s'%(self.object.banderas)
        
        return context

    def form_valid(self, form):
        
        pais=form.save(commit=False)
        banderas=self.request.POST['prueba']
        if 'banderas/' not in banderas:
            image_64_encode=self.request.POST['prueba']
            campo = image_64_encode.split(",")
            chars = '0123456789'
            nombre = get_random_string(5, chars)
            image_64_decode = base64.decodestring(bytes(campo[1], encoding='utf8'))
            image_result = open('MedCongressApp/static/banderas/imagen_%s.png'%(nombre), 'wb') # create a writable image and write the decoding result
            image_result.write(image_64_decode)
            if pais.banderas:
                fileObj = Path('MedCongressApp/static/%s'%( pais.banderas))
                if fileObj.is_file():    
                    remove('MedCongressApp/static/%s'%( pais.banderas))
            pais.banderas='banderas/imagen_%s.png'%(nombre)
        pais.save()
        return super().form_valid(form)

class CountryDeleteView(validarUser,DeleteView):
    model = Pais
    success_url = reverse_lazy('MedCongressAdmin:country_list')
    template_name = 'MedCongressAdmin/country_form.html'

    def get_context_data(self, **kwargs):
        context = super(CountryDeleteView, self).get_context_data(**kwargs)
        context['form_title'] = 'Eliminar'
        context['delete_value'] = self.object.denominacion
        return context
    def delete(self,request, *args, **kwargs):
            
        pais=Pais.objects.get(pk=self.kwargs.get('pk'))
        if pais.banderas:
            fileObj = Path('MedCongressApp/static/%s'%( pais.banderas))
            if fileObj.is_file(): 
                remove('MedCongressApp/static/%s'%( pais.banderas))
        pais.delete()
        return JsonResponse({'success':True}, safe=False)