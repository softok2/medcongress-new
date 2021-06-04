from os import remove
import base64
from django import forms
from pathlib import Path
from django.utils.crypto import get_random_string
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
        path=congreso.titulo.replace("/","").replace(" ","-").replace("?","").replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("ñ","n")
        congreso.path=path 
        if self.request.POST['prueba']:
            image_64_encode=self.request.POST['prueba']
            campo = image_64_encode.split(",")
            image_64_decode = base64.decodestring(bytes(campo[1], encoding='utf8')) 
            chars = '0123456789'
            nom= get_random_string(5, chars)
            image_result = open('MedCongressApp/static/usuarios/foto_%s.png'%(nom), 'wb') # create a writable image and write the decoding result
            image_result.write(image_64_decode)
            congreso.foto='usuarios/foto_%s.png'%(nom)
        else:
            congreso.foto='usuarios/defaulthombre.png' 
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
        trabajo_update=TrabajosInvestigacion.objects.get(pk=self.kwargs.get('pk'))
        path=congreso.titulo.replace("/","").replace(" ","-").replace("?","").replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("ñ","n")
        congreso.path=path 
        foto=self.request.POST['prueba']
        if foto:
            if 'usuarios/' not in foto:
                image_64_encode=self.request.POST['prueba']
                campo = image_64_encode.split(",")
                image_64_decode = base64.decodestring(bytes(campo[1], encoding='utf8')) 
                chars = '0123456789'
                nom= get_random_string(5, chars)
                image_result = open('MedCongressApp/static/usuarios/foto_%s.png'%(nom), 'wb') # create a writable image and write the decoding result
                image_result.write(image_64_decode)
                if  trabajo_update.foto:
                        fileObj = Path('MedCongressApp/static/usuarios/foto_%s.png'%( trabajo_update.foto))
                        if fileObj.is_file():
                            remove('MedCongressApp/static/static/usuarios/foto_%s.png'%( trabajo_update.foto))
                congreso.foto='usuarios/foto_%s.png'%(nom)
        else:
            congreso.foto='usuarios/defaulthombre.png'
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
    
class CongressTrabajoDeletedView(validarUser,DeleteView):
    model = TrabajosInvestigacion
    success_url = reverse_lazy('MedCongressAdmin:cat_usuarios_list')

    def delete(self,request, *args, **kwargs):

        try:    
            documento=TrabajosInvestigacion.objects.get(pk=self.kwargs.get('pk'))
            remove('MedCongressApp/static/%s'%(documento.documento))
            documento.delete()
            
            return JsonResponse({'success':True}, safe=False)
        except FileNotFoundError :
            return JsonResponse({'success':False,'mensaje':'No se pudo eliminar este Documento'}, safe=False)
        # if RelCongresoAval.objects.filter(aval=patrocinadores).exists():
        #     return JsonResponse({'success':False}, safe=False)
        # else:
        #     patrocinadores.delete()
        #     
