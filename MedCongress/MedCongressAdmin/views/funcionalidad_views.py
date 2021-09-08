import json
from django import forms
import base64
import os
from django.conf import settings
from os import remove
from pathlib import Path
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views.defaults import page_not_found
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.crypto import get_random_string
from django.views.generic import CreateView, ListView, TemplateView
from django.views.generic.edit import DeleteView, FormView, UpdateView
from MedCongressAdmin.forms.funcionalidades_form import EnviarCorreosForms
from MedCongressApp.models import SocioCongreso,RelCongresoSocio,Congreso,Organizador,RelCongresoUser
from MedCongressAdmin.apps import validarUser,validarOrganizador
from django.db.models import Q 
from MedCongressAdmin.task import Constancia,AsignarBeca 
from django.core.mail import EmailMessage     


class EnviarCorreos(validarOrganizador,FormView):
    template_name = 'MedCongressAdmin/funcionalidades/enviar_correo_form.html'
    form_class = EnviarCorreosForms

    def get_context_data(self, **kwargs):
        context = super(EnviarCorreos, self).get_context_data(**kwargs)
        congreso=Congreso.objects.all()
        context['congresos']=congreso
        return context
    
    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs(*args, **kwargs)
        kwargs['user'] =self.request.user
        return kwargs

    def form_valid(self, request, **kwargs):
        congreso_id= self.request.POST['congreso']
        congreso=Congreso.objects.filter(pk=congreso_id).first()
        asunto= self.request.POST['asunto']
        mensaje= self.request.POST['mensaje']

        users=RelCongresoUser.objects.filter(congreso=congreso).distinct('user')
        user_to=[]
        for user in users:
            user_to.append(user.user.usuario.email)
        email = EmailMessage(asunto,mensaje , to = user_to)
        email.content_subtype ="html"
        if self.request.FILES.get('adjunto'):
            adjunto=self.request.FILES.get('adjunto')
            with open('MedCongressApp/static/congreso/img_constancia/%s'%(adjunto.name), 'wb+') as destination:
                for chunk in adjunto.chunks():
                    destination.write(chunk)
       
            email.attach_file('MedCongressApp/static/congreso/img_constancia/%s'%(adjunto.name))
        email.send()
        if self.request.FILES.get('adjunto'):
            fileObj = Path('MedCongressApp/static/congreso/img_constancia/%s'%(adjunto.name))
            if fileObj.is_file():
                remove('MedCongressApp/static/congreso/img_constancia/%s'%(adjunto.name))
        messages.warning(self.request, 'Se le envio el correo a los usuarios de Congreso %s satisfactoriamente'%(congreso.titulo))
        return HttpResponseRedirect(reverse('MedCongressAdmin:enviar_email'))
