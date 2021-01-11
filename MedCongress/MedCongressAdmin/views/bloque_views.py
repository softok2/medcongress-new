from django import forms
from django.contrib import messages
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
from MedCongressApp.models import Bloque, Congreso, Ponencia, Taller, RelBloqueModerador,Moderador
from MedCongressAdmin.apps import validarUser
    

class BloquesListView(validarUser,ListView):
    model = Bloque
    context_object_name = 'bloques'
    template_name = 'MedCongressAdmin/bloques.html'

class BloqueCreateView(validarUser,FormView):
    model=Bloque
    form_class = BloqueForms
    success_url = reverse_lazy('MedCongressAdmin:bloques_list')
    template_name = 'MedCongressAdmin/bloque_form.html'

    def get_context_data(self, **kwargs):
        
        context = super(BloqueCreateView, self).get_context_data(**kwargs)
        if self.kwargs.get('pk'):
            context['con']=Congreso.objects.get(pk=self.kwargs.get('pk'))
        return context 
    
    def get_success_url(self):
        if self.kwargs.get('pk'):
            congreso=Congreso.objects.get(pk=self.kwargs.get('pk'))
            self.success_url =  reverse_lazy('MedCongressAdmin:Congres_bloques',kwargs={'path': congreso.path} )
        return self.success_url 
    def form_valid(self, form):
        
        bloque = form.save(commit=False)
        path=bloque.titulo.replace("/","").replace(" ","-").replace("?","").replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("ñ","n")
        chars = '0123456789'
        secret_key = get_random_string(5, chars)
        bloque.path=path+secret_key  
        bloque.save()
        return super(BloqueCreateView, self).form_valid(form)


class BloqueDeletedView(validarUser,DeleteView):
    model = Bloque
    success_url = reverse_lazy('MedCongressAdmin:bloques_list')

    def delete(self,request, *args, **kwargs):
            
        bloque=Bloque.objects.get(pk=self.kwargs.get('pk'))
       
        if bloque.congreso:
            return JsonResponse({'success':False,'evento': 'Congreso'}, safe=False)
        if Ponencia.objects.filter(bloque=bloque).exists():
            return JsonResponse({'success':False,'evento': 'Ponencia'}, safe=False) 
        if Taller.objects.filter(bloque=bloque).exists():
            return JsonResponse({'success':False,'evento': 'Taller'}, safe=False) 
        else:
            bloque.delete()
            return JsonResponse({'success':True}, safe=False)

class BloquePonenciasListView(validarUser,TemplateView):
    template_name= 'MedCongressAdmin/ponencias.html'  

    def get(self, request, **kwargs):
        bloque=Bloque.objects.filter(path=self.kwargs.get('path')).first()
        if bloque is None:
            return   HttpResponseRedirect(reverse('Error404'))
        return self.render_to_response(self.get_context_data())    
    def get_context_data(self, **kwargs):
        context = super(BloquePonenciasListView, self).get_context_data(**kwargs)
        bloque=Bloque.objects.filter(path=self.kwargs.get('path')).first()
        context['bloque']=bloque
        if self.kwargs.get('tipo')=='congreso':
            context['congres']=bloque.congreso
        context['ponencias']=Ponencia.objects.filter(bloque=bloque)
        return context

class BloqueTalleresListView(validarUser,TemplateView):
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

class BloqueUpdateView(validarUser,UpdateView):
    form_class = BloqueForms
    success_url = reverse_lazy('MedCongressAdmin:bloques_list')
    template_name = 'MedCongressAdmin/bloque_form.html'

    def get_queryset(self, **kwargs):
        return Bloque.objects.filter(pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        self.objects=Bloque.objects.get(pk=self.kwargs.get('pk'))
        context = super(BloqueUpdateView, self).get_context_data(**kwargs)
        if self.kwargs.get('tipo') and self.kwargs.get('tipo')=='congreso':
            context['con']=self.objects.congreso
        context['update']=self.objects.congreso.titulo
        return context

    def get_success_url(self):
        self.objects=Bloque.objects.get(pk=self.kwargs.get('pk'))
        if self.kwargs.get('tipo') and self.kwargs.get('tipo')=='congreso':
            congreso=self.objects.congreso
            print(self.kwargs.get('tipo'))
            self.success_url =  reverse_lazy('MedCongressAdmin:Congres_bloques',kwargs={'path': congreso.path} )
        return self.success_url
class BloqueModeradoresListView(validarUser,TemplateView):
    template_name= 'MedCongressAdmin/bloque_moderadores.html' 
    def get(self, request, **kwargs):
        bloque=Bloque.objects.filter(path=self.kwargs.get('path')).first()
        if bloque is None:
            return   HttpResponseRedirect(reverse('Error404'))
        return self.render_to_response(self.get_context_data())   

    def get_context_data(self, **kwargs):
        context = super(BloqueModeradoresListView, self).get_context_data(**kwargs)
        bloque=Bloque.objects.filter(path=self.kwargs.get('path')).first()
        context['bloque']=bloque
        context['moderadores']=RelBloqueModerador.objects.filter(bloque=bloque)
        return context   

class  BloqueModeradoresCreateView(validarUser,FormView):
    
    form_class = ModeradorBloqueForm
    # success_url = reverse_lazy('MedCongressAdmin:ponencias_list')
    template_name = 'MedCongressAdmin/bloque_moderador_form.html'

    def form_valid(self, form):
        ponencia=form.save(commit=False)
        ponencia.save()
        return super(BloqueModeradoresCreateView, self).form_valid(form)

    def get_success_url(self):
           self.success_url =  reverse_lazy('MedCongressAdmin:Moderadores_bloque',kwargs={'path': self.kwargs.get('path')} )
           return self.success_url
    def get_context_data(self, **kwargs):
        ctx = super(BloqueModeradoresCreateView, self).get_context_data(**kwargs)
        bloq=Bloque.objects.filter(path=self.kwargs.get('path')).first()
        moderadores=RelBloqueModerador.objects.filter(bloque=bloq)
        id=[]
        for ponente in moderadores:
            id.append(ponente.moderador.pk)
        ctx['moderadores']=Moderador.objects.exclude(id__in=id)
        ctx['bloq'] = bloq
        return ctx
    def get(self, request, **kwargs):
        bloque=Bloque.objects.filter(path=self.kwargs.get('path')).first()
        if bloque is None:
            return   HttpResponseRedirect(reverse('Error404'))
        return self.render_to_response(self.get_context_data()) 
class BloqueModeradoresDeletedView(validarUser,DeleteView):
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
        bloque=Bloque.objects.filter(path=self.kwargs.get('path')).first()
        if bloque is None:
            return   HttpResponseRedirect(reverse('Error404'))    
        return self.render_to_response(self.get_context_data()) 

    def get_success_url(self):
           self.success_url =  reverse_lazy('MedCongressAdmin:Bloque_ponencias',kwargs={'path': self.kwargs.get('path')} )
           return self.success_url

    def get_context_data(self, **kwargs):
       
        context = super(PonenciaSeleccionarView, self).get_context_data(**kwargs)
        bloque=Bloque.objects.filter(path=self.kwargs.get('path')).first()
        context['congreso'] = bloque.congreso
        return context
    def form_valid(self, form):
        ponencia_pk=self.request.POST['ponencia']
        
        bloque=Bloque.objects.filter(path=self.kwargs.get('path')).first()
        print(bloque)
        ponencia=Ponencia.objects.filter(pk=ponencia_pk).update(bloque=bloque)
        return super().form_valid(form)



    


