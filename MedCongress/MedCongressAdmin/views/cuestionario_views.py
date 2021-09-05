from django import forms
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views.defaults import page_not_found
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.crypto import get_random_string
from django.views.generic import CreateView, ListView, TemplateView
from django.views.generic.edit import DeleteView, FormView, UpdateView
from MedCongressAdmin.forms.congres_forms import CuestionarioForms,PreguntaForm
from MedCongressApp.models import CuestionarioPregunta,CuestionarioRespuestas,Congreso,Organizador
from MedCongressAdmin.apps import validarUser,validarOrganizador
from django.db.models import Q    

class CuestionarioListView(validarOrganizador,TemplateView):
  
    template_name = 'MedCongressAdmin/cuestionario/listar.html'
    
    def get(self, request, **kwargs):
        user = get_object_or_404(Congreso,path=self.kwargs.get('path'))
        congreso=Congreso.objects.filter(path=self.kwargs.get('path')).first()
        if not Organizador.objects.filter(user=self.request.user.perfilusuario,congreso=congreso).exists() and not self.request.user.is_staff: 
            return   HttpResponseRedirect(reverse('Error403'))
        return self.render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        congreso=Congreso.objects.filter(path=self.kwargs.get('path')).first()
        preguntas_env=[]
        preguntas=CuestionarioPregunta.objects.filter(congreso=congreso)
        for pregunta in preguntas:
            respuesta_list=[]
            respuestas=CuestionarioRespuestas.objects.filter(pregunta=pregunta)
            for respuesta in respuestas:
                respuesta_list.append({'texto':respuesta.respuesta,
                                        'is_correcta':respuesta.is_correcto,
                                        'publicada':respuesta.published,
                                        })
            preguntas_env.append({'texto':pregunta.pregunta,
                                    'publicada':pregunta.published,
                                    'id':pregunta.pk,
                                    'respuestas':respuesta_list,})
        context['preguntas']=preguntas_env
        context['congreso']=congreso
        context['search']=self.request.GET.get('search')
       
        return context
class PreguntaCreateView(validarUser,FormView):
    form_class = PreguntaForm
    success_url = reverse_lazy('MedCongressAdmin:ponencias_list')
    template_name = 'MedCongressAdmin/cuestionario_form.html'

    def form_valid(self, form):
        pregunta=form.save(commit=True)
        
        cant=0
        for respuesta in self.request.POST.getlist('respuesta'):
            resp=CuestionarioRespuestas(pregunta=pregunta,respuesta=respuesta,published=self.request.POST.getlist('published_resp')[cant],is_correcto=self.request.POST.getlist('is_correcto')[cant])
            resp.save() 
            cant=cant+1  
        return super(PreguntaCreateView, self).form_valid(form)
    
    def get_success_url(self):
        user = get_object_or_404(Congreso,path=self.request.GET.get('congreso'))
        url= reverse_lazy('MedCongressAdmin:Congres_cuestionario',kwargs={'path': self.request.GET.get('congreso')} )    
        self.success_url =  '%s?search=%s'%(url,self.request.GET.get('search')) 
        return self.success_url  
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        congreso=Congreso.objects.filter(path=self.request.GET.get('congreso')).first()
        context['congreso']=congreso
       
        return context

class CustionarioUpdateView(validarUser,FormView):
    form_class = PreguntaForm
    success_url = reverse_lazy('MedCongressAdmin:ponencias_list')
    template_name = 'MedCongressAdmin/cuestionario_form.html'



    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        pregunta=CuestionarioPregunta.objects.get(pk=self.kwargs.get('pk'))
        context['respuestas']=CuestionarioRespuestas.objects.filter(pregunta=pregunta)
        context['congreso']=pregunta.congreso
        context['pregunta']=pregunta
        return context
    def form_valid(self, form):
        
        pregunta =CuestionarioPregunta.objects.get(pk=self.request.POST['update'])   
        pregunta.pregunta=self.request.POST['pregunta']
        if 'published' in self.request.POST:
            pregunta.published=self.request.POST['published']
        else:
            pregunta.published= False
        pregunta.save()
        CuestionarioRespuestas.objects.filter(pregunta=pregunta).delete()
        cant=0
        for respuesta in self.request.POST.getlist('respuesta'):
            resp=CuestionarioRespuestas(pregunta=pregunta,respuesta=respuesta,published=self.request.POST.getlist('published_resp')[cant],is_correcto=self.request.POST.getlist('is_correcto')[cant])
            resp.save() 
            cant=cant+1  
        return super(CustionarioUpdateView, self).form_valid(form)
    def get_initial(self):
        initial=super().get_initial()
        pregunta=CuestionarioPregunta.objects.get(pk=self.kwargs.get('pk'))
        initial['pregunta']=pregunta.pregunta
        initial['published']=pregunta.published
        return initial

    def get_success_url(self):

        pregunta=CuestionarioPregunta.objects.get(pk=self.kwargs.get('pk'))    
        url =  reverse_lazy('MedCongressAdmin:Congres_cuestionario',kwargs={'path': pregunta.congreso.path} )
        self.success_url =  '%s?search=%s'%(url,self.request.GET.get('search')) 
        return self.success_url 

class CustionarioDeletedView(validarUser,DeleteView):
    model = CuestionarioPregunta
    success_url = reverse_lazy('MedCongressAdmin:asig_congress_list')

