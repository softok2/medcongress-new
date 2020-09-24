import json
from datetime import date

import requests
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.template.response import TemplateResponse
from django.urls import reverse, reverse_lazy
from django.utils.crypto import get_random_string
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DetailView, FormView, ListView,
                                  TemplateView, View)
from requests.auth import HTTPBasicAuth

from .forms import UserPerfilUser
from .models import (CategoriaPagoCongreso, Congreso, EspecialidadCongreso,
                     Ponencia, Ponente, RelCongresoCategoriaPago,
                     RelCongresoUser)
from .pager import Pager

# Create your views here.

##### Inicio #####

class Home(TemplateView):
    template_name= 'MedCongressApp/home.html' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ponentes'] = len(Ponente.objects.all())
        context['especialidades'] = len(EspecialidadCongreso.objects.all())
        context['afiliados'] = len(User.objects.all())
        return context

##### Listar Congresos #####

class CongresoListView(ListView):
    model=Congreso
    queryset=Congreso.objects.all()
    context_object_name='congreso_list'
    paginate_by = 9

    
    # def get_context_data(self, **kwargs):
    #     context = super(CongresoListView, self).get_context_data(**kwargs)
    #     context['pager_url'] = '%sall' % self.request.path
    #     return Pager.get_paginated_context(context)


##### Visualizar Congreso #####

class CongresoDetail(DetailView):
    model = Congreso
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['dias_faltan']=date.today()-self.model.fecha_inicio
        context['categorias_pago']= RelCongresoCategoriaPago.objects.filter(congreso=self.kwargs.get('pk'))
        context['ponencias']= Ponencia.objects.filter(congreso=self.kwargs.get('pk'))
       
        context['permiso']= len(RelCongresoUser.objects.filter(user=self.request.user.pk,congreso=self.kwargs.get('pk'))) 
        
        return context

##### Formulario Tarjeta Pagar Congreso #####

@method_decorator(login_required,name='dispatch')
class CongresoCardForm(TemplateView):

    template_name= 'MedCongressApp/tarjeta.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['categoria']= CategoriaPagoCongreso.objects.get(id=self.kwargs.get('pk_cat'))
        context['congreso']= Congreso.objects.get(id=self.kwargs.get('pk')) 
        context['pago']= RelCongresoCategoriaPago.objects.get(congreso=self.kwargs.get('pk'),categoria=self.kwargs.get('pk_cat'))
        
        return context

    def post(self, request, **kwargs):

        congreso= RelCongresoCategoriaPago.objects.get(congreso=request.POST["congreso_id"],categoria=request.POST["categoria_id"])
 
        url='https://sandbox-api.openpay.mx/v1/muq0plqu35rnjyo7sf2v/charges'
        params= {
                "source_id" : request.POST["token_id"],
                "method" : "card",
                "amount" : congreso.precio,
                "currency" : "MXN",
                "description" : "Cargo inicial a mi cuenta",
                "device_session_id" : request.POST["deviceIdHiddenFieldName"],
                "customer" : {
                        "name" : request.POST["nombre"],
                        "last_name" : "Vazquez Juarez",
                       
                        "email" : self.request.user.email
                }
            }
        headers={'Content-type': 'application/json'}
        response=requests.post(url=url,auth=HTTPBasicAuth('sk_d07c7b6ffeeb4acaaa15babdaac4101e:', ''),data=json.dumps(params),headers=headers)
        pagar_congreso=RelCongresoUser.objects.create(user=self.request.user.id,congreso=request.POST["congreso_id"],categoria_pago=request.POST["categoria_id"])
        pagar_congreso.save()
        return HttpResponse(response.content)
        
       

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['pagar']= RelCongresoCategoriaPago.objects.filter(congreso=self.kwargs.get('pk'), categoria=self.kwargs.get('pk_cat'))
    
    #     return context

##### Formulario para registrar usuario #####
@method_decorator(login_required,name='dispatch')
class PerfilUserCreate(CreateView):
    model=User
    form_class= UserPerfilUser
    template_name='MedCongressApp/registrarse.html'
    success_url = reverse_lazy('Home')
    def form_valid(self, form):
        #email = EmailMessage('Subject', 'Body', to=['dennis.molinetg@gmail.com'])
        # send_mail(
        #         'Subject here',
        #         'Here is the message.',
        #         'dennis.molinetg@gmail.com',
        #         ['milenis.morenop@gmail.com'],
        #         fail_silently=False,
        #         )
        #email.send()
        user = form['user'].save(commit=False)
        us=User.objects.create_user(user.username,user.email,user.password)
        perfiluser = form['perfiluser'].save(commit=False)
        us.first_name=user.first_name
        us.last_name=user.last_name
        us.is_active = False
        group= Group.objects.get(name='Cliente')
        us.groups.add(group)
        us.save()
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        secret_key = get_random_string(20, chars)
        perfiluser.activation_key=secret_key
        perfiluser.usuario = us
        perfiluser.save()
        # datas={}
        # datas['activation_key']=secret_key
        # datas['email']=user.email
        # datas['username']=user.username
        # datas['email_path']="/ActivationEmail.txt"
        # datas['email_subject']="Activation de votre compte yourdomain"
        # #form.sendEmail(datas)
       
        return HttpResponseRedirect(reverse('Home'))
