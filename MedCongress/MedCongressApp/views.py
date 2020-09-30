import json
from collections import namedtuple
from datetime import date

import requests
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.db import connections
from django.http import HttpResponse, HttpResponseRedirect
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
                     RelCongresoUser,RelPonenciaPonente,PerfilUsuario)
from .pager import Pager

# Create your views here.

##### Inicio #####

class Home(TemplateView):
    template_name= 'MedCongressApp/home.html' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ponentes'] = Ponente.objects.all()
        context['especialidades'] = EspecialidadCongreso.objects.all()
        context['afiliados'] = User.objects.all()
        context['congresos']= Congreso.objects.all().order_by('fecha_inicio')
        
        return context

##### Listar Congresos #####

class CongresoListView(ListView):
    model=Congreso
    queryset=Congreso.objects.filter(published=True)
    context_object_name='congreso_list'
    paginate_by = 9

    
    # def get_context_data(self, **kwargs):
    #     context = super(CongresoListView, self).get_context_data(**kwargs)
    #     context['pager_url'] = '%sall' % self.request.path
    #     return Pager.get_paginated_context(context)


##### Visualizar Congreso #####

class CongresoDetail(TemplateView):
    template_name= 'MedCongressApp/congreso_detail.html' 
    

    def get(self, request, **kwargs):
        congreso=Congreso.objects.filter(path=self.kwargs.get('path'),published=True).first()
        if congreso is None:
            return   HttpResponseRedirect(reverse('Error404'))
        return self.render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super(CongresoDetail, self).get_context_data(**kwargs)
        congreso=Congreso.objects.filter(path=self.kwargs.get('path'),published=True).first()
        if congreso is not None:
           
            context['congreso']=congreso
            #context['dias_faltan']=date.today()-self.model.fecha_inicio
            with connections['default'].cursor() as cursor:
                    sql_query = '''SELECT DISTINCT fecha_inicio::date FROM public."MedCongressApp_ponencia" where published is TRUE  and congreso_id= '''+ str(congreso.id) +''' ORDER by fecha_inicio'''
                    cursor.execute(sql_query)
                    data = [row[0] for row in cursor.fetchall()]
            
            context['fecha_ponencias']= data
            ponencias_env=[] 
            ponentes_env=[]
            for dat in context['fecha_ponencias'] :
                ponencias=Ponencia.objects.filter(fecha_inicio__date=dat,).order_by('fecha_inicio')
                for ponencia in ponencias:
                    ponentes_env.append(Ponente.objects.filter(ponencia_ponente__pk=ponencia.id).distinct()) 

                ponencias_env.append(ponencias)
            
            context['ponencias']=ponencias_env
            prueba_ponecia=Ponencia.objects.filter(congreso=congreso.pk)
            id=[]
            for pp in prueba_ponecia:
                id.append(pp.pk)

            pon=Ponente.objects.filter(ponencia_ponente__in=id).distinct()
           
            context['ponentes_congreso']=pon
            print(context['ponentes_congreso'])
            pagos = RelCongresoUser.objects.filter(user=self.request.user.pk, congreso=congreso.pk).order_by('precio')
            cat_pago=RelCongresoCategoriaPago.objects.filter(congreso=congreso.pk)
           
            context['categorias_pago']=cat_pago
            if pagos.exists():
                context['permiso'] = True
            else: 
                context['permiso'] = False                                                                  

        return context

##### Formulario Tarjeta Pagar Congreso #####

@method_decorator(login_required,name='dispatch')
class CongresoCardForm(TemplateView):
   
    template_name= 'MedCongressApp/tarjeta.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        if CategoriaPagoCongreso.objects.filter(path=self.kwargs.get('path_categoria')).exists() and Congreso.objects.filter(path=self.kwargs.get('path_congreso')).exists():
            context['categoria']= CategoriaPagoCongreso.objects.filter(path=self.kwargs.get('path_categoria')).first()
            context['congreso']= Congreso.objects.filter(path=self.kwargs.get('path_congreso')).first()
            context['pago']= RelCongresoCategoriaPago.objects.filter(congreso=context['congreso'].pk,categoria=context['categoria'].pk,moneda=self.kwargs.get('moneda')).first()
        return context

    def get(self, request, **kwargs):
        if CategoriaPagoCongreso.objects.filter(path=self.kwargs.get('path_categoria')).exists() and Congreso.objects.filter(path=self.kwargs.get('path_congreso')).exists():
            congreso= Congreso.objects.filter(path=self.kwargs.get('path_congreso')).first()
            categoria= CategoriaPagoCongreso.objects.filter(path=self.kwargs.get('path_categoria')).first()
            if not RelCongresoCategoriaPago.objects.filter(congreso=congreso.pk,categoria=categoria,moneda=self.kwargs.get('moneda')).exists():
                return   HttpResponseRedirect(reverse('Error404'))
            if RelCongresoUser.objects.filter(user=self.request.user.pk,congreso=congreso.pk).exists() : 
                return HttpResponseRedirect(reverse('View_congreso', kwargs={'path':self.kwargs.get('path_congreso')}))

            return self.render_to_response(self.get_context_data())
        else:
             return   HttpResponseRedirect(reverse('Error404'))

    def post(self, request, **kwargs):
        
        congreso= Congreso.objects.filter(path=self.kwargs.get('path_congreso')).first()
        categoria= CategoriaPagoCongreso.objects.filter(path=self.kwargs.get('path_categoria')).first()
        pago= RelCongresoCategoriaPago.objects.get(congreso=congreso.pk,categoria=categoria.pk,moneda=self.kwargs.get('moneda'))
 
        url='https://sandbox-api.openpay.mx/v1/muq0plqu35rnjyo7sf2v/charges'
        params= {
                "source_id" : request.POST["token_id"],
                "method" : "card",
                "amount" : pago.precio,
                "currency" : self.kwargs.get('moneda'),
                "description" : "Pago del Congreso %s con la categoría %s" %(congreso.titulo, congreso.titulo),
                "device_session_id" : request.POST["deviceIdHiddenFieldName"],
                "customer" : {
                        "name" : self.request.user.first_name,
                        "last_name" : self.request.user.first_name,
                       
                        "email" : self.request.user.email
                }
            }
        headers={'Content-type': 'application/json'}
        response=requests.post(url=url,auth=HTTPBasicAuth('sk_d07c7b6ffeeb4acaaa15babdaac4101e:', ''),data=json.dumps(params),headers=headers)
        response_dic=response.json()
        if response.status_code==200:
            congreso=Congreso.objects.filter(path=self.kwargs.get('path_congreso')).first()
            categoria=CategoriaPagoCongreso.objects.filter(path=self.kwargs.get('path_categoria')).first()
            user_perfil=PerfilUsuario.objects.filter(usuario=self.request.user.pk).first()
            print(user_perfil)
            pagar_congreso=RelCongresoUser.objects.create(user=user_perfil,congreso=congreso,categoria_pago=categoria,id_transaccion=response_dic['id'],num_autorizacion_transaccion=response_dic['authorization'],num_tarjeta_tranzaccion=response_dic['card']['card_number'])

            pagar_congreso.save()
            return HttpResponseRedirect(reverse('View_congreso', kwargs={'path':self.kwargs.get('path_congreso')}))
        else:
             return HttpResponse(response.json()['error_code'])
        return HttpResponse(response.json())
        
       

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['pagar']= RelCongresoCategoriaPago.objects.filter(congreso=self.kwargs.get('pk'), categoria=self.kwargs.get('pk_cat'))
    
    #     return context

##### Formulario para registrar usuario #####

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

##### Error 404 #####

class ViewError404(TemplateView):
    template_name= 'MedCongressApp/404.html' 

##### Error 404 #####

class ViewPonencia(TemplateView):
    template_name= 'MedCongressApp/view_ponencia.html' 