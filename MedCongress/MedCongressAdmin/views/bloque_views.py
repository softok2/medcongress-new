from django import forms
import base64
from django.contrib import messages
from os import remove
from pathlib import Path
from django.shortcuts import get_object_or_404
from django.views.defaults import page_not_found
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.http import JsonResponse
from django.utils.crypto import get_random_string
from django.views.generic import CreateView, ListView, TemplateView
from django.views.generic.edit import DeleteView, FormView, UpdateView
from MedCongressAdmin.forms.congres_forms import BloqueForms,ModeradorBloqueForm,SelectPonencia
from MedCongressApp.models import Bloque, Congreso, Ponencia, Taller, RelBloqueModerador,Moderador,Organizador
from MedCongressAdmin.apps import validarUser,validarOrganizador
    

class BloquesListView(validarOrganizador,TemplateView):
    model = Bloque
    context_object_name = 'bloques'
    template_name = 'MedCongressAdmin/bloque/listar.html'
    def get(self, request, **kwargs):
        if self.request.GET.get('congreso'):
            congreso=Congreso.objects.filter(path=self.request.GET.get('congreso')).first()
            if congreso is None:
                return   HttpResponseRedirect(reverse('Error404'))
            if not Organizador.objects.filter(user=self.request.user.perfilusuario,congreso=congreso).exists() and not self.request.user.is_staff: 
                return   HttpResponseRedirect(reverse('Error403'))
        else:
            if not self.request.user.is_staff:
                return   HttpResponseRedirect(reverse('Error403'))   
        return self.render_to_response(self.get_context_data())
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        if self.request.GET.get('search'):
            context['search']=self.request.GET.get('search')
        if self.request.GET.get('congreso'):
            congreso=Congreso.objects.filter(path=self.request.GET.get('congreso')).first() 
            context['congres'] =congreso
            context['bloques']=Bloque.objects.filter(congreso=congreso)
        else:
            context['bloques']=Bloque.objects.all()
        return context

class BloqueCreateView(validarOrganizador,FormView):
    model=Bloque
    form_class = BloqueForms
    success_url = reverse_lazy('MedCongressAdmin:bloques_list')
    template_name = 'MedCongressAdmin/bloque/form.html'

    def get_context_data(self, **kwargs):
        context = super(BloqueCreateView, self).get_context_data(**kwargs)
        if self.kwargs.get('pk'):
            context['con']=Congreso.objects.get(pk=self.kwargs.get('pk'))
        return context 
        
    def get(self, request, **kwargs):
        if self.kwargs.get('pk'):
            congreso=Congreso.objects.filter(pk=self.kwargs.get('pk')).first()
            if not congreso:
                return   HttpResponseRedirect(reverse('Error404'))
            if not Organizador.objects.filter(user=self.request.user.perfilusuario,congreso=congreso).exists() and not self.request.user.is_staff : 
                return   HttpResponseRedirect(reverse('Error403'))
        return self.render_to_response(self.get_context_data())    
    
    def get_success_url(self):
        url=''
        if self.kwargs.get('pk'):
            congreso=Congreso.objects.get(pk=self.kwargs.get('pk'))
            url =  reverse_lazy('MedCongressAdmin:bloques_list')+'?congreso=%s'%(congreso.path)
            self.success_url =  '%s&search=%s'%(url,self.request.GET.get('search'))
        else:
            url= reverse_lazy('MedCongressAdmin:bloques_list')   
            self.success_url =  '%s?search=%s'%(url,self.request.GET.get('search'))
        return self.success_url 
    def form_valid(self, form):
        
        bloque = form.save(commit=False)
        path=bloque.titulo.replace("/","").replace(" ","-").replace("?","").replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("ñ","n")
        chars = '0123456789'
        secret_key = get_random_string(5, chars)
        bloque.path=path+secret_key  
        image_64_encode=self.request.POST['prueba']
        campo = image_64_encode.split(",")
        image_64_decode = base64.decodestring(bytes(campo[1], encoding='utf8')) 
        chars = '0123456789'
        nombre = get_random_string(5, chars)
        image_result = open('MedCongressApp/static/bloque/imagen_%s.png'%(nombre), 'wb') # create a writable image and write the decoding result
        image_result.write(image_64_decode)
        bloque.imagen='bloque/imagen_%s.png'%(nombre)
        bloque.save()
        return super(BloqueCreateView, self).form_valid(form)

class BloqueDeletedView(validarOrganizador,DeleteView):
    model = Bloque
    success_url = reverse_lazy('MedCongressAdmin:bloques_list')
    def get(self, request, **kwargs):
        bloque=Bloque.objects.get(pk=self.kwargs.get('pk'))
        if not Organizador.objects.filter(user=self.request.user.perfilusuario,congreso=bloque.congreso).exists()and not self.request.user.is_staff : 
            return   HttpResponseRedirect(reverse('Error403'))
        return self.render_to_response(self.get_context_data())    
    def delete(self,request, *args, **kwargs):
            
        bloque=Bloque.objects.get(pk=self.kwargs.get('pk'))
       
        if Ponencia.objects.filter(bloque=bloque).exists():
            return JsonResponse({'success':False,'evento': 'Ponencia'}, safe=False) 
        if Taller.objects.filter(bloque=bloque).exists():
            return JsonResponse({'success':False,'evento': 'Taller'}, safe=False) 
        else:
            bloque.delete()
            return JsonResponse({'success':True}, safe=False)

class BloquePonenciasListView(validarOrganizador,TemplateView):
    template_name= 'MedCongressAdmin/ponencias.html'  

    def get(self, request, **kwargs):
        bloque=Bloque.objects.filter(path=self.kwargs.get('path')).first()
        if bloque is None:
            return   HttpResponseRedirect(reverse('Error404'))
        if not Organizador.objects.filter(user=self.request.user.perfilusuario,congreso=bloque.congreso).exists() and not self.request.user.is_staff: 
            return   HttpResponseRedirect(reverse('Error403'))
        return self.render_to_response(self.get_context_data())    
    def get_context_data(self, **kwargs):
        context = super(BloquePonenciasListView, self).get_context_data(**kwargs)
        bloque=Bloque.objects.filter(path=self.kwargs.get('path')).first()
        context['bloque']=bloque
        if self.kwargs.get('tipo')=='congreso':
            context['congres']=bloque.congreso
        context['ponencias']=Ponencia.objects.filter(bloque=bloque)
        return context

class BloqueTalleresListView(validarOrganizador,TemplateView):
    template_name= 'MedCongressAdmin/talleres.html'  

    def get(self, request, **kwargs):
        bloque=Bloque.objects.filter(path=self.kwargs.get('path')).first()
        if bloque is None:
            return   HttpResponseRedirect(reverse('Error404'))
        return self.render_to_response(self.get_context_data())    
    def get_context_data(self, **kwargs):
        context = super(BloqueTalleresListView, self).get_context_data(**kwargs)
        bloque=Bloque.objects.filter(path=self.kwargs.get('path')).first()
        context['bloc']=bloque
        if self.kwargs.get('tipo')=='congreso':
            context['congres']=bloque.congreso
        context['talleres']=Taller.objects.filter(bloque=bloque)
        return context

class BloqueUpdateView(validarOrganizador,UpdateView):
    form_class = BloqueForms
    success_url = reverse_lazy('MedCongressAdmin:bloques_list')
    template_name = 'MedCongressAdmin/bloque/form.html'

    def get(self, request, **kwargs):
        
       
        bloque=Bloque.objects.filter(pk=self.kwargs.get('pk')).first()
        self.object=bloque
        if self.request.GET.get('congreso'):
            if not bloque:
                return   HttpResponseRedirect(reverse('Error404'))
            if not Organizador.objects.filter(user=self.request.user.perfilusuario,congreso=bloque.congreso).exists() and not self.request.user.is_staff : 
                return   HttpResponseRedirect(reverse('Error403'))
        else:
            if not self.request.user.is_staff:
                return   HttpResponseRedirect(reverse('Error403'))  
        return self.render_to_response(self.get_context_data())  

    def get_queryset(self, **kwargs):
        return Bloque.objects.filter(pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        self.objects=Bloque.objects.get(pk=self.kwargs.get('pk'))
        context = super(BloqueUpdateView, self).get_context_data(**kwargs)
        if self.object.imagen:
            context['imagen']=self.object.imagen
        if self.request.GET.get('congreso'):
            context['con']=self.objects.congreso
        context['update']=self.objects.congreso.titulo
        return context

    def get_success_url(self):
        self.objects=Bloque.objects.get(pk=self.kwargs.get('pk'))
        url= reverse_lazy('MedCongressAdmin:bloques_list' )+'?search=%s'%(self.request.GET.get('search'))
        if self.request.GET.get('congreso'):
            congreso=self.objects.congreso
            url+='&congreso=%s'%(congreso.path)
        self.success_url = url 
        return self.success_url 
    
    def form_valid(self, form):
        bloque = form.save(commit=False)
        imagen=self.request.POST['prueba']
        bloque_edit=Bloque.objects.get(pk=self.kwargs.get('pk'))
        if 'bloque/' not in imagen:
            image_64_encode=self.request.POST['prueba']
            campo = image_64_encode.split(",")
            chars = '0123456789'
            nombre = get_random_string(5, chars)
            image_64_decode = base64.decodestring(bytes(campo[1], encoding='utf8'))
            image_result = open('MedCongressApp/static/bloque/imagen_%s.png'%(nombre), 'wb') # create a writable image and write the decoding result
            image_result.write(image_64_decode)
            if bloque_edit.imagen:
                fileObj = Path('MedCongressApp/static/%s'%( bloque_edit.imagen))
                if fileObj.is_file():
                    remove('MedCongressApp/static/%s'%( bloque_edit.imagen))

            bloque.imagen='bloque/imagen_%s.png'%(nombre)
            bloque.save()
        return super(BloqueUpdateView, self).form_valid(form)    

class BloqueModeradoresDeletedView(validarOrganizador,DeleteView):
    model = RelBloqueModerador
    success_url = reverse_lazy('MedCongressAdmin:Moderadores_list')

class  PonenciaSeleccionarView(validarUser,FormView):
    
    model=Ponencia
    form_class = SelectPonencia
    # success_url = reverse_lazy('MedCongressAdmin:ponencias_list')
    template_name='MedCongressAdmin/select_ponencia_form.html'
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['path'] = self.kwargs.get('path')
        return kwargs
        
    def get(self, request, **kwargs):
        if self.request.GET.get('congreso'):
            congreso=Congreso.objects.filter(path=self.request.GET.get('congreso')).first()
            if congreso is None:
                return   HttpResponseRedirect(reverse('Error404'))
        if self.request.GET.get('bloque'):
            congreso=Bloque.objects.filter(path=self.request.GET.get('bloque')).first()
            if congreso is None:
                return   HttpResponseRedirect(reverse('Error404'))
        return self.render_to_response(self.get_context_data())

    def get_success_url(self):
        url=reverse_lazy('MedCongressAdmin:ponencias_list')
        self.success_url='%s?&search=%s'%(url,self.request.GET.get('search'))
        if self.request.GET.get('congreso'):
            self.success_url =  '%s?congreso=%s&search=%s'%(url,self.request.GET.get('congreso'),self.request.GET.get('search')) 
        if self.request.GET.get('bloque'): 
            self.success_url =  '%s?bloque=%s&search=%s'%(url,self.request.GET.get('bloque'),self.request.GET.get('search')) 
            if self.request.GET.get('congreso_bloque'):
                self.success_url =  '%s?bloque=%s&search=%s&congreso_bloque=true'%(url,self.request.GET.get('bloque'),self.request.GET.get('search')) 

        return self.success_url 

    def get_context_data(self, **kwargs):
       
        context = super(PonenciaSeleccionarView, self).get_context_data(**kwargs)
        bloque=Bloque.objects.filter(path=self.kwargs.get('path')).first()
        context['ponencias']=Ponencia.objects.filter(congreso=bloque.congreso)
        if self.request.GET.get('congreso'):
            context['congreso']=Congreso.objects.filter(path=self.request.GET.get('congreso')).first()   
        if self.request.GET.get('bloque'):
            context['bloque']=Bloque.objects.filter(path=self.request.GET.get('bloque')).first()
            if self.request.GET.get('congreso_bloque'):
                context['congreso_bloque']=context['bloque'].congreso
        return context

    def form_valid(self, form):
        ponencia_pk=self.request.POST['ponencia']
        
        bloque=Bloque.objects.filter(path=self.kwargs.get('path')).first()
        ponencia=Ponencia.objects.filter(pk=ponencia_pk).update(bloque=bloque)
        return super().form_valid(form)



    


