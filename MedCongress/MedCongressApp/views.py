import json
import os
from collections import namedtuple
from datetime import date,datetime
import openpay
import requests
from django.template import RequestContext
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.db import connections
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import render,render_to_response
#from django.core.mail import EmailMessage
from django.template.response import TemplateResponse
from django.urls import reverse, reverse_lazy
from django.utils.crypto import get_random_string
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DetailView, FormView, ListView,
                                  TemplateView, View)
from requests.auth import HTTPBasicAuth
from django.contrib.auth.views import PasswordResetView
from random import sample
from PIL import Image, ImageDraw, ImageFont

from .forms import UserPerfilUser
from .models import (CategoriaPagoCongreso, Congreso, EspecialidadCongreso,
                     Ponencia, Ponente, RelCongresoCategoriaPago,
                     RelCongresoUser,RelPonenciaPonente,PerfilUsuario,ImagenCongreso,Taller,RelTalleresCategoriaPago,RelTallerUser,DatosIniciales,
                     CategoriaUsuario,Bloque,Moderador,RelTallerPonente,Pais,CuestionarioPregunta,CuestionarioRespuestas,RelPonenciaVotacion)
from .pager import Pager
from .cart import Cart
from django_xhtml2pdf.views import PdfMixin
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


###################
####  OpenPay  ####
###################


ID_KEY='m6ftsapwjvmo7j7y8mop'
PUBLIC_KEY='pk_0d4449445a4948899811cea14a469793'
PRIVATE_KEY='sk_34664e85b5504ca39cc19d8f9b8df8a2'
URL_PDF='https://sandbox-dashboard.openpay.mx'


# ID_KEY='muq0plqu35rnjyo7sf2v'
# PUBLIC_KEY='pk_0c7aea61d0ef4a4f8fdfbd674841981a'
# PRIVATE_KEY='sk_d07c7b6ffeeb4acaaa15babdaac4101e'
# URL_PDF='https://sandbox-dashboard.openpay.mx'


# Create your views here.

##### Inicio #####

class Email( TemplateView):
   template_name= 'MedCongressApp/recibo_pago.html' 
# class ConfigEmail(TemplateView):
#     template_name= 'MedCongressApp/confic_email.html' 
    

class Home(TemplateView):
    template_name= 'MedCongressApp/home.html' 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        datos_in=DatosIniciales.objects.all().first()
        context['datos_ini']=datos_in
        context['ponentes'] = Ponente.objects.all()
        context['especialidades'] = len(EspecialidadCongreso.objects.all())+datos_in.especialidades
        context['afiliados'] = len(User.objects.all())+datos_in.afiliados
        context['congresos']= Congreso.objects.filter(published=True).order_by('fecha_inicio')
        context['nuevo_congreso'] = Congreso.objects.filter(fecha_inicio__gt=datetime.now(),published=True).first()
        return context

class PagoExitoso(TemplateView):
    template_name= 'MedCongressApp/pago_satifactorio.html' 
@method_decorator(login_required,name='dispatch')   
class Perfil(TemplateView):
    template_name= 'MedCongressApp/perfil.html' 
    
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        congresos=RelCongresoUser.objects.filter(user=self.request.user.perfilusuario,is_pagado=True).distinct('congreso')
        context['congresos']=congresos
        congresos_pendientes=RelCongresoUser.objects.filter(user=self.request.user.perfilusuario,is_pagado=False).distinct('congreso')
        context['congresos_pendientes']=congresos_pendientes
        talleres=RelTallerUser.objects.filter(user=self.request.user.perfilusuario,is_pagado=True).distinct('taller')
        context['talleres']=talleres
        talleres_pendientes=RelTallerUser.objects.filter(user=self.request.user.perfilusuario,is_pagado=False).distinct('taller')
        context['talleres_pendientes']=talleres_pendientes
       
        if Ponente.objects.filter(user=self.request.user.perfilusuario).exists():
            ponencias=RelPonenciaPonente.objects.filter(ponente=self.request.user.perfilusuario.ponente)
            context['ponencias']=ponencias
            talleres_pon=RelTallerPonente.objects.filter(ponente=self.request.user.perfilusuario.ponente)
            context['talleres_pon']=talleres_pon
        constancias=RelCongresoUser.objects.filter(user=self.request.user.perfilusuario,is_constancia=True).values('congreso','foto_constancia').distinct()
        constancias_env=[]
        for constancia in constancias:
            congreso=Congreso.objects.get(pk=constancia['congreso'])
            constancias_env.append({'congreso':congreso})
        context['constancias']=constancias_env
        
        # context['ponentes'] = Ponente.objects.all()
        # context['especialidades'] = len(EspecialidadCongreso.objects.all())+datos_in.especialidades
        # context['afiliados'] = len(User.objects.all())+datos_in.afiliados
        # context['congresos']= Congreso.objects.filter(published=True).order_by('fecha_inicio')
        # context['nuevo_congreso'] = Congreso.objects.filter(fecha_inicio__gt=datetime.now(),published=True).first()
        return context
##### Listar Congresos #####

class CongresoListView(ListView):
    model=Congreso
    queryset=Congreso.objects.filter(published=True)
    context_object_name='congreso_list'
    paginate_by = 9

    def post(self, request, **kwargs):
        self.object_list = self.get_queryset()
        especialidades=EspecialidadCongreso.objects.filter(nombre__icontains=request.POST["especialidad"])
        id=[]
        for especialidad in especialidades:
            id.append(especialidad.pk)
        print(id)
        congreso=Congreso.objects.filter(especialidad__in=id,published=True)
        return self.render_to_response(self.get_context_data(object_list=congreso))

    # def get_context_data(self, **kwargs):
    #     context = super(CongresoListView, self).get_context_data(**kwargs)
    #     context['pager_url'] = '%sall' % self.request.path
    #     return Pager.get_paginated_context(context)


##### Visualizar Congreso #####

class CongresoDetail(TemplateView):
    # template_name= 'MedCongressApp/congreso_detail.html' 
    

    def get(self, request, **kwargs):
        congreso=Congreso.objects.filter(path=self.kwargs.get('path'),published=True).first()
        if congreso is None:
            return   HttpResponseRedirect(reverse('Error404'))
        return self.render_to_response(self.get_context_data())

    def get_template_names(self):
        congreso=Congreso.objects.filter(path=self.kwargs.get('path'),published=True).first()
        if congreso.is_openpay:
            template_name= 'MedCongressApp/congreso_detail_openpay.html'
        else:
            template_name= 'MedCongressApp/%s'%(congreso.template)
        return template_name

    def get_context_data(self, **kwargs):
        context = super(CongresoDetail, self).get_context_data(**kwargs)
        congreso=Congreso.objects.filter(path=self.kwargs.get('path'),published=True).first()
        if self.request.user.is_authenticated:
            pagado=RelCongresoUser.objects.filter(congreso=congreso,user=self.request.user.perfilusuario,is_pagado=True)
            if pagado :
                context['pagado']=True
                constancias=RelCongresoUser.objects.filter(congreso=congreso,user=self.request.user.perfilusuario)
                for constancia in constancias:
                    if constancia.is_constancia:
                        context['constancia']=True
                
        if congreso is not None:
           
            context['congreso']=congreso
            #context['dias_faltan']=date.today()-self.model.fecha_inicio
            with connections['default'].cursor() as cursor:
                    sql_query = '''SELECT DISTINCT fecha_inicio::date FROM public."MedCongressApp_ponencia" where published is TRUE  and congreso_id= '''+ str(congreso.id) +''' ORDER by fecha_inicio'''
                    cursor.execute(sql_query)
                    data2 = [row[0] for row in cursor.fetchall()]
            with connections['default'].cursor() as cursor:
                    sql_query = '''SELECT DISTINCT fecha_inicio::date FROM public."MedCongressApp_taller" where published is TRUE  and congreso_id= '''+ str(congreso.id) +''' ORDER by fecha_inicio'''
                    cursor.execute(sql_query)
                    data1 = [row[0] for row in cursor.fetchall()]
                    
            
            data=data2+[i for i in data1 if i not in data2]
           
            context['fecha_ponencias']= data
            ponencias_env=[] 
           
            for dat in context['fecha_ponencias'] :
                bloques=Bloque.objects.filter(fecha_inicio__date=dat,congreso=congreso,published=True).order_by('fecha_inicio')
                ponencias=Ponencia.objects.filter(fecha_inicio__date=dat,congreso=congreso,published=True,bloque=None).order_by('fecha_inicio')
                talleres=Taller.objects.filter(fecha_inicio__date=dat,congreso=congreso,published=True,bloque=None).order_by('fecha_inicio')
                result=[]
                for bloque in bloques: 
                    bloque_ponencias=Ponencia.objects.filter(bloque=bloque,published=True).order_by('fecha_inicio')
                    bloque_talleres=Taller.objects.filter(bloque=bloque,published=True).order_by('fecha_inicio')
                    eventos=[]
                    for ponencia in bloque_ponencias: 
                        eventos.append({
                        'id':ponencia.id,
                        'path':ponencia.path,
                        'titulo': ponencia.titulo,
                        'fecha_inicio': ponencia.fecha_inicio ,# una relación a otro modelo
                        'detalle':ponencia.detalle ,
                        'ponentes':Ponente.objects.filter(ponencia_ponente__pk=ponencia.id).distinct() ,
                        'tipo':'Ponencia',# la misma relación, otro campo
                        })
                    for taller in bloque_talleres: 
                        eventos.append({
                        'id':taller.id,
                        'path':ponencia.path,
                        'titulo': taller.titulo,
                        'fecha_inicio': taller.fecha_inicio ,# una relación a otro modelo
                        'detalle':taller.detalle ,
                        'ponentes':Ponente.objects.filter(taller_ponente__pk=taller.id).distinct() ,
                        'tipo':'Taller',# la misma relación, otro campo
                        })
                    eventos = sorted(eventos, key=lambda k: k['fecha_inicio'])
                    result.append({
                    'id':bloque.id,
                    'path':ponencia.path,
                    'moderador':Moderador.objects.filter(bloque_moderador__pk=bloque.id).distinct() ,
                    'titulo': bloque.titulo,
                    'fecha_inicio': bloque.fecha_inicio ,# una relación a otro modelo
                    'detalle':bloque.detalle ,
                    'eventos':eventos,
                    'tipo':'Bloque',# la misma relación, otro campo
                    })
                for ponencia in ponencias: 
                    result.append({
                    'id':ponencia.id,
                    'path':ponencia.path,
                    'titulo': ponencia.titulo,
                    'fecha_inicio': ponencia.fecha_inicio ,# una relación a otro modelo
                    'detalle':ponencia.detalle ,
                    'ponentes':Ponente.objects.filter(ponencia_ponente__pk=ponencia.id).distinct() ,
                    'tipo':'Ponencia',# la misma relación, otro campo
                    })
                for taller in talleres: 
                    result.append({
                    'id':taller.id,
                    'path':taller.path,
                    'titulo': taller.titulo,
                    'fecha_inicio': taller.fecha_inicio ,# una relación a otro modelo
                    'detalle':taller.detalle ,
                    'ponentes':Ponente.objects.filter(taller_ponente__pk=taller.id).distinct() ,
                    'tipo':'Taller',# la misma relación, otro campo
                    })
                result = sorted(result, key=lambda k: k['fecha_inicio'])
              
                # ponentes_env.append(Ponente.objects.filter(ponencia_ponente__pk=ponencia.id).distinct()) 
                ponencias_env.append(result)
                # for taller in talleres:
                #     ponentes_env.append(Taller.objects.filter(reltallerponente__pk=taller.id).distinct()) 
             
                #     ponencias_env.append(talleres)
            
            context['ponencias']=ponencias_env

            prueba_ponecia=Ponencia.objects.filter(congreso=congreso.pk)
            id_p=[]
            for pp in prueba_ponecia:
                id_p.append(pp.pk)

            ponentes=Ponente.objects.filter(ponencia_ponente__in=id_p).distinct()
            ponentes_env=[]
            for ponente in ponentes: 
                ponentes_env.append({
                'id':ponente.id,
                'id_user':ponente.user.pk,
                'nombre': ponente.user.usuario.first_name,
                'apellido': ponente.user.usuario.last_name ,# una relación a otro modelo
                'foto':ponente.user.foto,
                'tipo':'Ponente',# la misma relación, otro campo
                })

            prueba_taller=Taller.objects.filter(congreso=congreso.pk)
            id_t=[]
            for pp in prueba_taller:
                id_t.append(pp.pk)

            ponentes=Ponente.objects.filter(taller_ponente__in=id_t).distinct()

            for ponente in ponentes: 
                var=False
                for pon in ponentes_env:
                    if pon['id_user']==ponente.user.pk:
                        var=True
                if not var:
                    ponentes_env.append({
                    'id':ponente.id,
                    'id_user':ponente.user.pk,
                    'nombre': ponente.user.usuario.first_name,
                    'apellido': ponente.user.usuario.last_name ,# una relación a otro modelo
                    'foto':ponente.user.foto,
                    'tipo':'Ponente',# la misma relación, otro campo
                    })
            
            bloques=Bloque.objects.filter(congreso=congreso.pk)
            id_b=[]
            for pp in bloques:
              
                id_b.append(pp.pk)
            moderadores=Moderador.objects.filter(bloque_moderador__in=id_b).distinct()

            for moderador in moderadores: 
                var=False
                for pon in ponentes_env:
                    if pon['id_user']==moderador.user.pk:
                        var=True
                if not var:
                    ponentes_env.append({
                    'id':moderador.id,
                    'id_user':moderador.user.pk,
                    'nombre': moderador.user.usuario.first_name,
                    'apellido': moderador.user.usuario.last_name ,# una relación a otro modelo
                    'foto':moderador.user.foto,
                    'tipo':'Moderador',# la misma relación, otro campo
                    })


            context['ponentes_congreso']=ponentes_env
            cat_pago=RelCongresoCategoriaPago.objects.filter(congreso=congreso.pk)
            context['cat_ponente']=RelPonenciaPonente.objects.all()

            if self.request.user.is_authenticated :
                user_perfil=PerfilUsuario.objects.filter(usuario=self.request.user.pk).first()
                talleres=Taller.objects.filter(congreso=congreso.pk).order_by('fecha_inicio')
                ver=[]
                for taller in talleres:
                    if RelTalleresCategoriaPago.objects.filter(taller=taller).exists():
                        cat_pa=RelTalleresCategoriaPago.objects.filter(taller=taller)
                    else:
                        cat_pa=True
                    
                    if RelTallerUser.objects.filter(user=user_perfil.pk, taller=taller.pk).exists():
                        ver.append([taller,cat_pa,True])
                    else:
                        ver.append([taller,cat_pa,False])  
                context['talleres']=ver
                pagos = RelCongresoUser.objects.filter(user=user_perfil.pk, congreso=congreso.pk).order_by('precio')
                
                if pagos.exists():
                    pagos_p = RelCongresoUser.objects.filter(user=user_perfil.pk, congreso=congreso.pk,is_pagado=True).order_by('precio') 
                    if pagos_p.exists():
                        context['permiso'] = True
                    else:
                        context['permiso'] = True
                else: 
                    context['permiso'] = False                                                                  
            else:
                talleres=Taller.objects.filter(congreso=congreso.pk).order_by('fecha_inicio')
                ver=[]
                for taller in talleres:
                    if RelTalleresCategoriaPago.objects.filter(taller=taller).exists():
                        cat_pa=RelTalleresCategoriaPago.objects.filter(taller=taller)
                    else:
                        cat_pa=True
                    ver.append([taller,cat_pa,False])      
                context['talleres']=ver
                context['permiso'] = False  
            context['categorias_pago']=cat_pago
        return context

##### Formulario Tarjeta Pagar Congreso #####

@method_decorator(login_required,name='dispatch')
class CongresoCardForm(TemplateView):
   
    template_name= 'MedCongressApp/tarjeta.html'
    def get_context_data(self, **kwargs):
        context = super(CongresoCardForm, self).get_context_data(**kwargs)
        context['id_key']=ID_KEY
        context['public_key']=PUBLIC_KEY
        return context

    def post(self, request, **kwargs):
        
        # congreso= Congreso.objects.filter(path=self.kwargs.get('path_congreso')).first()
        # categoria= CategoriaPagoCongreso.objects.filter(path=self.kwargs.get('path_categoria')).first()
        # pago= RelCongresoCategoriaPago.objects.get(congreso=congreso.pk,categoria=categoria.pk,moneda=self.kwargs.get('moneda'))
        user_perfil=PerfilUsuario.objects.filter(usuario=self.request.user.pk).first()
        pagar_efectivo= self.request.POST['pagar_efectivo']


        descripcion =''
        for cart in self.request.session["cart"][1]:
            descripcion= descripcion + 'Pago del %s %s . '%(cart['tipo_evento'],cart['nombre_congreso'])
        
        if pagar_efectivo == '0':
            if request.POST["deviceIdHiddenFieldName"] is None:
                self.request.session["error_opempay"]= 'Error de Conección con Openpay'
                return HttpResponseRedirect(reverse('Error_openpay'))

            url='https://sandbox-api.openpay.mx/v1/%s/charges'%(ID_KEY)
            params= {
                    "source_id" : request.POST["token_id"],
                    "method" : "card",
                    "amount" : self.request.session["cart"][0]['cant'],
                    "currency" : 'MXN',
                    "description" :  descripcion,
                    "device_session_id" : request.POST["deviceIdHiddenFieldName"],
                    "customer" : {
                            "name" : self.request.user.first_name,
                            "last_name" : self.request.user.last_name,
                            "email" : self.request.user.email
                    },
                    "use_3d_secure":True,
                    "redirect_url":'https://medcongress.com.mx/transaccion_exitosa',
                }

                
            headers={'Content-type': 'application/json'}
            response=requests.post(url=url,auth=HTTPBasicAuth('%s:'%(PRIVATE_KEY), ''),data=json.dumps(params),headers=headers)
            response_dic=response.json()
            if response.status_code==200:
                ##### EMAIL #####
                subject = 'Comprobante de Pago de MedCongress'
                html_message = render_to_string('MedCongressApp/recibo_pago.html', context={'car':self.request.session["cart"],'date':response_dic['operation_date'],'numero':response_dic['authorization'],'importe':response_dic['amount'],'card':response_dic['card']['card_number'],'orden_id':response_dic['order_id']})
                plain_message = strip_tags('Aviso..... Usted se a comprado eventos en MedCongres')
                from_email = ' Contacto MedCongress <contacto@medcongress.com.mx>'
                to = self.request.user.email
                mail.send_mail(subject, plain_message, from_email, [to],html_message=html_message)
                ####END EMAIL ######
                for cart in self.request.session["cart"][1]:
                    if str(cart['tipo_evento']) == 'Congreso':
                        congreso=Congreso.objects.filter(id=cart['id_congreso']).first()
                        categoria=CategoriaPagoCongreso.objects.filter(id=cart['id_cat_pago']).first()
                        pagar_congreso=RelCongresoUser.objects.create(user=user_perfil,congreso=congreso,categoria_pago=categoria,id_transaccion=response_dic['id'],num_autorizacion_transaccion=response_dic['authorization'],num_tarjeta_tranzaccion=response_dic['card']['card_number'],is_pagado=True,cantidad=cart['cantidad'])
                        pagar_congreso.save()
                    if str(cart['tipo_evento']) == 'Taller':
                        taller=Taller.objects.filter(id=cart['id_congreso']).first()
                        categoria=CategoriaPagoCongreso.objects.filter(id=cart['id_cat_pago']).first()
                        pagar_congreso=RelTallerUser.objects.create(user=user_perfil,taller=taller,categoria_pago=categoria,id_transaccion=response_dic['id'],num_autorizacion_transaccion=response_dic['authorization'],num_tarjeta_tranzaccion=response_dic['card']['card_number'],is_pagado=True,cantidad=cart['cantidad'])
                        pagar_congreso.save()
                car=Cart(self.request)
                car.clear() 
                return HttpResponseRedirect(reverse('transaccion_exitosa'))

            else:
                self.request.session["error_opempay"]=response.json()['description']
                return HttpResponseRedirect(reverse('Error_openpay'))
        
        else:
            
            try:
                url='https://sandbox-api.openpay.mx/v1/%s/charges'%(ID_KEY)
                params= {
                        
                        "method" : "store",
                        "amount" : self.request.session["cart"][0]['cant'],
                        "currency" : 'MXN',
                        "description" :  descripcion,
                        "customer" : {
                                "name" : self.request.user.first_name,
                                "last_name" : self.request.user.last_name,
                                "email" : self.request.user.email
                        }
                    }
                headers={'Content-type': 'application/json'}
                response=requests.post(url=url,auth=HTTPBasicAuth('%s:'%(PRIVATE_KEY), ''),data=json.dumps(params),headers=headers)
              
                response_dic=response.json()
                if response.status_code==200:
                    for cart in self.request.session["cart"][1]:
                        if str(cart['tipo_evento']) == 'Congreso':
                            congreso=Congreso.objects.filter(id=cart['id_congreso']).first()
                            categoria=CategoriaPagoCongreso.objects.filter(id=cart['id_cat_pago']).first()
                            pagar_congreso=RelCongresoUser.objects.create(user=user_perfil,congreso=congreso,categoria_pago=categoria,is_pagado=False,cantidad=cart['cantidad'])
                            pagar_congreso.save()
                        if str(cart['tipo_evento']) == 'Taller':
                            taller=Taller.objects.filter(id=cart['id_congreso']).first()
                            categoria=CategoriaPagoCongreso.objects.filter(id=cart['id_cat_pago']).first()
                            pagar_congreso=RelTallerUser.objects.create(user=user_perfil,taller=taller,categoria_pago=categoria,is_pagado=False,cantidad=cart['cantidad'])
                            pagar_congreso.save()
                    car=Cart(self.request)
                    car.clear() 
                    return HttpResponseRedirect('%s/paynet-pdf/%s/%s'%(URL_PDF,ID_KEY,response_dic['payment_method']['reference']) )
                else:
                    self.request.session["error_opempay"]=response.json()['description']
                    return HttpResponseRedirect(reverse('Error_openpay'))
            except openpay.APIConnectionError as e:
                self.request.session["error_opempay"]='Error de Conección con Openpay'
                return HttpResponseRedirect(reverse('Error_openpay'))
            except openpay.AuthenticationError as e:
                self.request.session["error_opempay"]='Error en la autentificación en openpay '
                return HttpResponseRedirect(reverse('Error_openpay'))
            except openpay.APIError as e:
                self.request.session["error_opempay"]=e.json_body['description']
                return HttpResponseRedirect(reverse('Error_openpay'))
            except openpay.InvalidRequestError as e:
                
                if isinstance(e,dict):
                    self.request.session["error_opempay"]=e.json_body['description']
                else:
                    self.request.session["error_opempay"]='Póngase en contacto con el Admin'
               
                return HttpResponseRedirect(reverse('Error_openpay'))


##### Formulario para registrar usuario #####

class PerfilUserCreate(CreateView):
    model=User
    form_class= UserPerfilUser
    template_name='MedCongressApp/registrarse.html'
    success_url = reverse_lazy('Home')
    def get_context_data(self, **kwargs):
        context = super(PerfilUserCreate, self).get_context_data(**kwargs)
        context['aviso_privacidad']=DatosIniciales.objects.all().first()
        return context
    def form_valid(self, form):

        
        user = form['user'].save(commit=False)
        # email = EmailMessage('Asunto', 'esto es una prueba, como mando correos en Phyton?', to = ['dennis.molinetg@gmail.com'])
        # email.send()
        

        us=User.objects.create_user(user.username,user.email,user.password)
        ubicacion= form['ubicacion'].save(commit=True)
        perfiluser = form['perfiluser'].save(commit=False)
        categoria = form['categoria'].save(commit=False)
        if categoria.nombre !='':
            categoria.published=False
            categoria.save()
            perfiluser.categoria=categoria
        us.first_name=user.first_name
        us.last_name=user.last_name
        us.is_active = False
        group= Group.objects.get(name='Cliente')
        us.groups.add(group)
        us.save()
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
        secret_key = get_random_string(60, chars)
        perfiluser.activation_key=secret_key

        subject = 'Bienvenido a MedCongress'
        html_message = render_to_string('MedCongressApp/email.html', context={'token':secret_key})
        plain_message = strip_tags('Aviso..... Usted se a creado un usuario en MedCongress')
        from_email = ' Contacto MedCongress <contacto@medcongress.com.mx>'
        to = user.email
        mail.send_mail(subject, plain_message, from_email, [to],html_message=html_message)

        perfiluser.usuario = us
        perfiluser.ubicacion=ubicacion
        perfiluser.path=us.username
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

class ViewErrorOpenpay(TemplateView):
    template_name= 'MedCongressApp/Error_openpay.html' 
##### Error 404 #####

class ViewPonencia(TemplateView):
    template_name= 'MedCongressApp/view_ponencia.html' 

    def get(self, request, **kwargs):
        ponencia=Ponencia.objects.filter(path=self.kwargs.get('path'),published=True).first()
        if ponencia is None:
            return   HttpResponseRedirect(reverse('Error404'))
        return self.render_to_response(self.get_context_data())    

    def get_context_data(self, **kwargs):
        context = super(ViewPonencia, self).get_context_data(**kwargs)
        ponencia=Ponencia.objects.filter(path=self.kwargs.get('path'),published=True).first() 
        if self.request.user.is_authenticated:
            context['is_pagado']=RelCongresoUser.objects.filter(congreso=ponencia.congreso,user=self.request.user.perfilusuario,is_pagado=True).exists()
       
       
            if RelPonenciaVotacion.objects.filter(ponencia=ponencia,user=self.request.user).exists():
                votacio=RelPonenciaVotacion.objects.filter(ponencia=ponencia,user=self.request.user).first()
                context['is_evaluado']=votacio.votacion
        else:
            context['is_pagado']=False
        context['ponencia']=ponencia
        return context


##### Autocompletar Especialidades #####

def EspecialdiadesAutocomplete(request):
    if request.is_ajax():
        query = request.GET.get("term", "")
        especialidades = EspecialidadCongreso.objects.filter(nombre__icontains=query)
        results = []
        for especialidad in especialidades:
            place_json = especialidad.nombre
            results.append(place_json)
        data = json.dumps(results)
    mimetype = "application/json"
    return HttpResponse(data, mimetype)

##### Pagar en efectivo #####
@method_decorator(login_required,name='dispatch')
class PagarEfectivo(TemplateView):

    template_name= 'MedCongressApp/tarjeta.html'


    def post(self, request, **kwargs):
        congreso= Congreso.objects.filter(path=self.kwargs.get('path_congreso')).first()
        categoria= CategoriaPagoCongreso.objects.filter(path=self.kwargs.get('path_categoria')).first()
        pago= RelCongresoCategoriaPago.objects.get(congreso=congreso.pk,categoria=categoria.pk,moneda=self.kwargs.get('moneda'))
        user_perfil=PerfilUsuario.objects.filter(usuario=self.request.user.pk).first()
        

##### Adicionar Congreso a Carrito de Compra #####
@method_decorator(login_required,name='dispatch')
class AddCart(TemplateView):

    def get(self, request):
        if request.is_ajax:
            query =request.GET.get("id")
            cant =request.GET.get("cant")
            prueba=RelCongresoCategoriaPago.objects.filter(id=query).first()
            car=Cart(self.request)
            result=car.add_evento(relCongresoCategoriaPago=prueba,cant=cant)
            return JsonResponse({'succes':result}, safe=False)
        return TemplateResponse(request, reverse('dashboard'))
   

##### Adicionar Taller a Carrito de Compra #####
@method_decorator(login_required,name='dispatch')
class AddCartTaller(TemplateView):
    

    def get(self, request):
        if request.is_ajax:
            query =request.GET.get("id")
            cant =request.GET.get("cant")
            prueba=RelTalleresCategoriaPago.objects.filter(id=query).first()
            car=Cart(self.request)
            result=car.add_taller(relTallerCategoriaPago=prueba,cant=cant)
            return JsonResponse({'succes':result}, safe=False)
        return TemplateResponse(request, reverse('dashboard'))

##### Deleted Evento Carrito de Compra #####
@method_decorator(login_required,name='dispatch')
class DeletedCart(TemplateView):

    def get(self, request):
        if request.is_ajax:
            id =request.GET.get("id")
          
            car=Cart(self.request)
            result=car.remove(id=id) 
            return JsonResponse({'succes':result}, safe=False)
        return TemplateResponse(request, reverse('dashboard'))

##### Confirmar Evento Carrito de Compra #####
@method_decorator(login_required,name='dispatch')
class ConfCart(TemplateView):

    def get(self, request):
        if request.is_ajax:
            id =request.GET.get("id")
            cant =request.GET.get("cant")
            car=Cart(self.request)
            result=car.confirmar(id=id,cant=cant)
            return JsonResponse({'succes':result}, safe=False)
        return TemplateResponse(request, reverse('dashboard'))

class AvisoPrivacidad(TemplateView):
    template_name= 'MedCongressApp/aviso_privacidad.html' 
    def get_context_data(self, **kwargs):
        context = super(AvisoPrivacidad, self).get_context_data(**kwargs)
        context['aviso_privacidad']=DatosIniciales.objects.all().first()
        return context


class HabilitarUser(TemplateView):
    template_name= 'MedCongressApp/confic_email.html' 
    def get(self, request, **kwargs):
        usuario=PerfilUsuario.objects.filter(activation_key=self.kwargs.get('token')).first()
        if usuario is None:
            return   HttpResponseRedirect(reverse('Error404'))
        else:
            usuario.usuario.is_active=True
            usuario.usuario.save()
            usuario.save()
            return self.render_to_response(self.get_context_data()) 

class GetPerfil(TemplateView):
    def get(self, request):
        if request.is_ajax:
            query =request.GET.get("pk")
            usuario=PerfilUsuario.objects.get(pk=query)
            especialidad_env=''
            if usuario.especialidad:
                especialidad_env=usuario.especialidad.nombre
            ced_env=''
            if usuario.cel_profecional:
                ced_env=usuario.cel_profecional
            publicaciones_env=''
            if usuario.publicaciones:
                publicaciones_env=usuario.publicaciones
            constancia_env=''
            if usuario.detalle:
                constancia_env=usuario.detalle
            datos_env=''
            if usuario.datos_interes:
                datos_env=usuario.datos_interes 
            puesto_env=''
            if usuario.puesto:
                puesto_env=usuario.puesto 
            ######### Ponencias #######
            ponencias_env=[]
            if Ponente.objects.filter(user=usuario).exists():
                ponencias=Ponencia.objects.filter(ponente=usuario.ponente)
                for ponencia in ponencias:
                    ponencias_env.append({'nombre':ponencia.titulo,
                                            'congreso':ponencia.congreso.titulo})
            
            ###### END Ponencias#######
             ######### Talleres#######
            talleres_env=[]
            if Ponente.objects.filter(user=usuario).exists():
                talleres=Taller.objects.filter(ponente=usuario.ponente)
                for taller in talleres:
                    talleres_env.append({'nombre':taller.titulo,
                                            'congreso':taller.congreso.titulo})
            
            ###### END Talleres#######
            bandera=''
            if Pais.objects.filter(denominacion=(usuario.ubicacion.direccion.split(',')[-1]).strip()).exists():
                pais=Pais.objects.filter(denominacion=(usuario.ubicacion.direccion.split(',')[-1]).strip()).first()
                bandera=str(pais.banderas)
            usuario_json={'nombre_completo':usuario.usuario.first_name+' '+usuario.usuario.last_name,
                            'nombre':usuario.usuario.first_name,
                            'email':usuario.usuario.email,
                            'foto':str(usuario.foto),
                            'pais':usuario.ubicacion.direccion.split(',')[-1],
                            'localidad':usuario.ubicacion.direccion,
                            'bandera':bandera,
                            'constancias':constancia_env,
                            'publicaciones':publicaciones_env,
                            'especialidad':especialidad_env,
                            'youtube':usuario.youtube,
                            'linkedin':usuario.linkedin,
                            'twitter':usuario.twitter,
                            'facebook':usuario.facebook,
                            'puesto':puesto_env,
                            'ponencias':ponencias_env,
                            'talleres':talleres_env}
            return JsonResponse(usuario_json, safe=False)
        return TemplateResponse(request, reverse('dashboard'))

@method_decorator(login_required,name='dispatch')
class GetCuestionario(TemplateView):
    template_name= 'MedCongressApp/congreso_cuestionario.html' 

    def get(self, request, **kwargs):
        congreso=Congreso.objects.filter(path=self.kwargs.get('path'),published=True).first()
        if congreso is None:
            return   HttpResponseRedirect(reverse('Error404'))
        constancia=RelCongresoUser.objects.filter(congreso=congreso,user=self.request.user.perfilusuario,is_constancia=True).first()
        if  constancia :
            return   HttpResponseRedirect(reverse('Error404'))
        return self.render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super(GetCuestionario, self).get_context_data(**kwargs)
        congreso=Congreso.objects.filter(path=self.kwargs.get('path'),published=True).first()
        context['congreso']=congreso
        cuestionario=[]
        preguntas=CuestionarioPregunta.objects.filter(congreso=congreso,published=True)
        for pregunta in preguntas:
            respuestas=CuestionarioRespuestas.objects.filter(pregunta=pregunta,published=True)
            cuestionario.append({'pregunta':pregunta.pregunta,
                                'id':pregunta.pk,
                                'respuestas':respuestas})
        con=congreso.cant_preguntas
        if len(preguntas)<con:
            con=len(preguntas)
        preg=sample(cuestionario,con)
        context['preguntas']=preg
       
        return context

    def post(self, request, **kwargs):

        cant=0
        total=0
        congreso=Congreso.objects.filter(path=self.kwargs.get('path'),published=True).first()
        preguntas=CuestionarioPregunta.objects.filter(congreso=congreso,published=True)
        
        cuestionario=[]
        preg=1
        for pregunta in self.request.POST.getlist('pregunta'):
            if self.request.POST.get('respuesta_%s'%(preg)):
                respuesta=self.request.POST['respuesta_%s'%(preg)]
            else:
                respuesta=0
            cuestionario.append('%s-%s'%(pregunta,respuesta))
            preg=preg+1
        
        for resp in self.request.POST:
            if cant > 1:
                respuesta=CuestionarioRespuestas.objects.get(pk=self.request.POST[resp])
                if respuesta.is_correcto:
                    total=total+1
                
            cant=cant+1
        con=congreso.cant_preguntas
        if len(preguntas)<con:
            con=len(preguntas)
        
        preguntas=self.request.POST[resp]
        if total/con*100>congreso.aprobado:

            constancias=RelCongresoUser.objects.filter(congreso=congreso,user=self.request.user.perfilusuario)
            for constancia in constancias:
                constancia.is_constancia=True
                constancia.fecha_constancia=datetime.now()
                constancia.cuestionario=(','.join(cuestionario))
                constancia.save()

        return  HttpResponseRedirect(reverse('Resultado_Cuestionario',kwargs={'path': congreso.path}))
        


def GetFactura(request):
   
    url='https://sandbox-api.openpay.mx/v1/%s/invoices/v33'%(ID_KEY)
    params={
        "openpay_transaction_id":'tr5h2zdvk1ju0jflmpwk',
        "subtotal": 2001.75,
       
        "total": 2322.03,
        "tipo_de_cambio": 1,
        "forma_pago": "04",
        "hide_total_items": True,
        "hide_total_taxes": True,
        
        "moneda": "MXN",
        "conceptos": [
            {
                "clave": "78111500",
                "clave_unidad": "E54",
                "identificador": "6K9MVV CUAHUTEMOC BLANCO",
                "cantidad": 1,
                "unidad": "Viaje",
                "descripcion": "TRANSPORTACION AEREA DE QRO A MTY",
                "valor_unitario": 1744,
                "importe": 1744,
                "traslados": [
                    {
                        "impuesto": "002",
                        "base": 1744,
                        "tipo_factor": "Tasa",
                        "tasa": 0.16,
                        "importe": 279.04
                    }
                ]
            },
            {
                "clave": "78111500",
                "clave_unidad": "E54",
                "identificador": "6K9MVV CUAHUTEMOC BLANCO",
                "cantidad": 1,
                "unidad": "Viaje",
                "descripcion": "SEGURO DE CANCELACION",
                "valor_unitario": 257.75,
                "importe": 257.75,
                "traslados": [
                    {
                        "impuesto": "002",
                        "base": 257.75,
                        "tipo_factor": "Tasa",
                        "tasa": 0.16,
                        "importe": 41.24
                    }
                ]
            }
        ],
        "lugar_expedicion": "76090",
        "observaciones": "Si desea obtener su factura por el servicio de Asistencia TAR, ingrese a la siguiente dirección:\nhttp://masistencia.emitecliente.mx/index.php/clientefacturacion/generarFactura\nSi lo desea puede ingresar a esta dirección desde nuestro portal.",
        
        "impuestos_traslado": [
            {
                "impuesto": "002",
                "tasa": 0.16,
                "importe": 320.28,
                "tipo_factor": "Tasa"
            }
        ],
        "impuestos_retencion": [],
       
        "receptor": {
            "nombre": "Alberto Montellano Sandoval",
            "rfc": "MOSA8311152G0",
            "email": "alberto.montellano@tcpip.tech",
            "uso_cfdi": "G03"
        },
        "invoice_id":'12345',
        "metodo_pago": "PUE",
        
    }  
    headers={'Content-type': 'application/json'}
    response=requests.post(url=url,auth=HTTPBasicAuth('%s:'%(PRIVATE_KEY), ''),data=json.dumps(params),headers=headers)
    response_dic=response.json()

    url1='https://sandbox-api.openpay.mx/v1/%s/invoices/v33/%s'%(ID_KEY,response_dic['request_id'])
    print(url1)
    headers={'Content-type': 'application/json'}
    response1=requests.get(url=url1,auth=HTTPBasicAuth('%s:'%(PRIVATE_KEY), ''),headers=headers)
    return HttpResponse(response1)


class SetConstancia(TemplateView):

    template_name= 'MedCongressApp/congreso_constancia.html' 
    def get_context_data(self, **kwargs):
        
        context = super(SetConstancia, self).get_context_data(**kwargs)
        congreso=Congreso.objects.filter(path=self.kwargs.get('path'),published=True).first()
        constancias=RelCongresoUser.objects.filter(congreso=congreso,user=self.request.user.perfilusuario,is_constancia=True)
        context['congreso']=congreso
        nombre='%s %s'%(self.request.user.first_name,self.request.user.last_name)
        congreso_t= congreso.titulo
        cont=len(nombre)
        comienzo=630-(cont/2*18)
        cont=len(congreso_t)
        comienzo_t=640-(cont/2*10)
        base=Image.open('MedCongressApp/static/congreso/img_constancia/cosntancia.jpeg').convert('RGBA')
        text=Image.new('RGBA',base.size,(255,255,255,0))
        nombre_font=ImageFont.truetype('bahnschrift.ttf',40)
        congreso_font=ImageFont.truetype('calibri.ttf',25)
        fecha_font=ImageFont.truetype('calibri.ttf',25)
        # cong.set_variation_by_name('Italic')
        d=ImageDraw.Draw(text)
        d.text((comienzo,400),nombre,font=nombre_font,fill=(89, 85, 85))
        d.text((430,470),'Ha concluido satisfactoriamente el Congreso',font=congreso_font,fill=(94,196,234,255))
        d.text((comienzo_t,500),congreso_t,font=congreso_font,fill=(14,138,184,255))
        d.text((555,775),constancias.first().fecha_constancia.strftime('%d/%m/%Y'),font=fecha_font,fill=(89, 85, 85))
        out=Image.alpha_composite(base,text)
        tit=congreso.titulo.replace("/","").replace(" ","-").replace("?","").replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("ñ","n")
       
        nombre_img='constancia_%s_%s'%(self.request.user.first_name,tit) 
        for constancia in constancias:
            constancia.foto_constancia='congreso/img_constancia/%s.png'%(nombre_img)
            constancia.save()

        out.save('MedCongressApp/static/congreso/img_constancia/%s.png'%(nombre_img))

        return context

    def get(self, request, **kwargs):
        congreso=Congreso.objects.filter(path=self.kwargs.get('path'),published=True).first()
        if congreso is None:
            return   HttpResponseRedirect(reverse('Error404'))
        constancia=RelCongresoUser.objects.filter(congreso=congreso,user=self.request.user.perfilusuario,is_constancia=True).count()
        if  constancia is None :
            return   HttpResponseRedirect(reverse('Error404'))
        return self.render_to_response(self.get_context_data())

class Get_Constancia(PdfMixin,TemplateView):

    template_name= 'MedCongressApp/congreso_constancia.html' 
    def get_context_data(self, **kwargs):
        
        context = super(Get_Constancia, self).get_context_data(**kwargs)
        congreso=Congreso.objects.filter(path=self.kwargs.get('path'),published=True).first()
        constancia=RelCongresoUser.objects.filter(congreso=congreso,user=self.request.user.perfilusuario,is_constancia=True).first()
        print(constancia)
        context['congreso']=congreso
        context['constancia']=constancia
        return context

    def get(self, request, **kwargs):
        congreso=Congreso.objects.filter(path=self.kwargs.get('path'),published=True).first()
        if congreso is None:
            return   HttpResponseRedirect(reverse('Error404'))
        constancia=RelCongresoUser.objects.filter(congreso=congreso,user=self.request.user.perfilusuario,is_constancia=True).count()
        if  constancia is None :
            return   HttpResponseRedirect(reverse('Error404'))
        return self.render_to_response(self.get_context_data())


class EvaluarPonencia(TemplateView):
    template_name= 'MedCongressApp/pago_satifactorio.html'

    def get(self, request):
        if request.is_ajax:
            puntuacion =request.GET.get("puntuacion")
            usuario=request.GET.get("usuario")
            ponencia_id=request.GET.get("ponencia")
            ponencia=Ponencia.objects.get(pk=ponencia_id)
            votacion=RelPonenciaVotacion(user=self.request.user,ponencia=ponencia,votacion=puntuacion)
            votacion.save()
            usuario_json={'succes':'True'}
            return JsonResponse(usuario_json, safe=False)
        return TemplateResponse(request, reverse('dashboard')) 

class Resultado_Cuestionario(TemplateView):
    template_name='MedCongressApp/resultado_cuestionario.html'

    def get(self, request, **kwargs):
        congreso=Congreso.objects.filter(path=self.kwargs.get('path'),published=True).first()
        if congreso is None:
            return   HttpResponseRedirect(reverse('Error404'))
       
        return self.render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super(Resultado_Cuestionario, self).get_context_data(**kwargs)
        congreso=Congreso.objects.filter(path=self.kwargs.get('path'),published=True).first()
        context['congreso']=congreso
        context['aprobado']=RelCongresoUser.objects.filter(congreso=congreso,user=self.request.user.perfilusuario,is_constancia=True).exists()

        return context