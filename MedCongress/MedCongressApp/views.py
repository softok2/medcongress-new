import json
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

from .forms import UserPerfilUser
from .models import (CategoriaPagoCongreso, Congreso, EspecialidadCongreso,
                     Ponencia, Ponente, RelCongresoCategoriaPago,
                     RelCongresoUser,RelPonenciaPonente,PerfilUsuario,ImagenCongreso,Taller,RelTalleresCategoriaPago,RelTallerUser,DatosIniciales,
                     CategoriaUsuario)
from .pager import Pager
from .cart import Cart

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


# Create your views here.

##### Inicio #####

class Home(TemplateView):
    template_name= 'MedCongressApp/home.html' 
    
    def get_context_data(self, **kwargs):
        self.request.session['my_car'] = [{'tipo':'congreso','id':'23','cat_pago':'21','precio':'250','nombre':'Nombre','cantidad':'2'},{'tipo':'Taller','id':'23','cat_pago':'21','precio':'250','nombre':'Nombre Taller','cantidad':'1'},{'total':'500'}]
        
        context = super().get_context_data(**kwargs)
        datos_in=DatosIniciales.objects.all().first()
        context['datos_ini']=datos_in
        context['ponentes'] = Ponente.objects.all()
        context['especialidades'] = len(EspecialidadCongreso.objects.all())+datos_in.especialidades
        context['afiliados'] = len(User.objects.all())+datos_in.afiliados
        context['congresos']= Congreso.objects.filter(published=True).order_by('fecha_inicio')
        context['nuevo_congreso'] = Congreso.objects.filter(fecha_inicio__gt=datetime.now(),published=True).first()
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
                    data2 = [row[0] for row in cursor.fetchall()]
            with connections['default'].cursor() as cursor:
                    sql_query = '''SELECT DISTINCT fecha_inicio::date FROM public."MedCongressApp_taller" where published is TRUE  and congreso_id= '''+ str(congreso.id) +''' ORDER by fecha_inicio'''
                    cursor.execute(sql_query)
                    data1 = [row[0] for row in cursor.fetchall()]
                    
            
            data=data2+[i for i in data1 if i not in data2]
            print(data)
            context['fecha_ponencias']= data
            ponencias_env=[] 
            ponentes_env=[]
            for dat in context['fecha_ponencias'] :
                ponencias=Ponencia.objects.filter(fecha_inicio__date=dat,congreso=congreso,published=True).order_by('fecha_inicio')
                talleres=Taller.objects.filter(fecha_inicio__date=dat,congreso=congreso,published=True).order_by('fecha_inicio')
                result=[]
                for ponencia in ponencias: 
                    result.append({
                    'id':ponencia.id,
                    'titulo': ponencia.titulo,
                    'fecha_inicio': ponencia.fecha_inicio ,# una relación a otro modelo
                    'detalle':ponencia.detalle ,
                    'ponentes':Ponente.objects.filter(ponencia_ponente__pk=ponencia.id).distinct() ,
                    'tipo':'Ponencia',# la misma relación, otro campo
                    })
                for taller in talleres: 
                    result.append({
                    'id':taller.id,
                    'titulo': taller.titulo,
                    'fecha_inicio': taller.fecha_inicio ,# una relación a otro modelo
                    'detalle':taller.detalle ,
                    'ponentes':Ponente.objects.filter(taller_ponente__pk=taller.id).distinct() ,
                    'tipo':'Taller',# la misma relación, otro campo
                    })
                result = sorted(result, key=lambda k: k['fecha_inicio'])
                print(result)
                # ponentes_env.append(Ponente.objects.filter(ponencia_ponente__pk=ponencia.id).distinct()) 
                ponencias_env.append(result)
                # for taller in talleres:
                #     ponentes_env.append(Taller.objects.filter(reltallerponente__pk=taller.id).distinct()) 
             
                #     ponencias_env.append(talleres)
            
            context['ponencias']=ponencias_env

            prueba_ponecia=Ponencia.objects.filter(congreso=congreso.pk)
            id=[]
            for pp in prueba_ponecia:
                id.append(pp.pk)

            pon=Ponente.objects.filter(ponencia_ponente__in=id).distinct()
           
            context['ponentes_congreso']=pon
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
                    "currency" : self.kwargs.get('moneda'),
                    "description" :  descripcion,
                    "device_session_id" : request.POST["deviceIdHiddenFieldName"],
                    "customer" : {
                            "name" : self.request.user.first_name,
                            "last_name" : self.request.user.first_name,
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
                        pagar_congreso=RelCongresoUser.objects.create(user=user_perfil,congreso=congreso,categoria_pago=categoria,id_transaccion=response_dic['id'],num_autorizacion_transaccion=response_dic['authorization'],num_tarjeta_tranzaccion=response_dic['card']['card_number'],is_pagado=True)
                        pagar_congreso.save()
                    if str(cart['tipo_evento']) == 'Taller':
                        taller=Taller.objects.filter(id=cart['id_congreso']).first()
                        categoria=CategoriaPagoCongreso.objects.filter(id=cart['id_cat_pago']).first()
                        pagar_congreso=RelTallerUser.objects.create(user=user_perfil,taller=taller,categoria_pago=categoria,id_transaccion=response_dic['id'],num_autorizacion_transaccion=response_dic['authorization'],num_tarjeta_tranzaccion=response_dic['card']['card_number'],is_pagado=True)
                        pagar_congreso.save()
                car=Cart(self.request)
                car.clear() 
                return HttpResponseRedirect(reverse('Home'))
            else:
                self.request.session["error_opempay"]=response.json()['description']
                return HttpResponseRedirect(reverse('Error_openpay'))
                #return HttpResponse(response.json()['error_code'])
                #return HttpResponse(response.content)

            return HttpResponse(response.json())
        
        else:
            
            try:
                # openpay.api_key = "sk_d07c7b6ffeeb4acaaa15babdaac4101e"
                # openpay.verify_ssl_certs = False
                # openpay.merchant_id = "muq0plqu35rnjyo7sf2v"

                openpay.api_key = PRIVATE_KEY
                openpay.verify_ssl_certs = False
                openpay.merchant_id = ID_KEY
                
            
                if user_perfil.id_openpay :
                    customer = openpay.Customer.retrieve(user_perfil.id_openpay)
                
                else:
                    customer = openpay.Customer.create(
                        name=self.request.user.first_name,
                        email=self.request.user.email,
                        last_name=self.request.user.last_name,    
                    )
                    user_perfil.id_openpay=customer.id
                    user_perfil.save()

                ver=customer.charges.create( method="store", amount=self.request.session["cart"][0]['cant'], description=descripcion, capture=False)
                for cart in self.request.session["cart"][1]:
                    if str(cart['tipo_evento']) == 'Congreso':
                        congreso=Congreso.objects.filter(id=cart['id_congreso']).first()
                        categoria=CategoriaPagoCongreso.objects.filter(id=cart['id_cat_pago']).first()
                        pagar_congreso=RelCongresoUser.objects.create(user=user_perfil,congreso=congreso,categoria_pago=categoria)
                        pagar_congreso.save()
                    if str(cart['tipo_evento']) == 'Taller':
                        taller=Taller.objects.filter(id=cart['id_congreso']).first()
                        categoria=CategoriaPagoCongreso.objects.filter(id=cart['id_cat_pago']).first()
                        pagar_congreso=RelTallerUser.objects.create(user=user_perfil,taller=taller,categoria_pago=categoria)
                        pagar_congreso.save()
                car=Cart(self.request)
                car.clear() 
                return HttpResponseRedirect('%s/paynet-pdf/%s/%s'%(URL_PDF,ID_KEY,ver.payment_method.reference) )
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
    def form_valid(self, form):

        
        user = form['user'].save(commit=False)
        # email = EmailMessage('Asunto', 'esto es una prueba, como mando correos en Phyton?', to = ['dennis.molinetg@gmail.com'])
        # email.send()
        subject = 'HTML EMAIL'
        html_message = render_to_string('MedCongressApp/404.html', context={})
        plain_message = strip_tags(html_message)
        from_email = 'SOFTOK2 ME <amorell@softok2.com>'
        to = 'dennis.molinetg@gmail.com'
        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

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
        us.is_active = True
        group= Group.objects.get(name='Cliente')
        us.groups.add(group)
        us.save()
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        secret_key = get_random_string(20, chars)
        perfiluser.activation_key=secret_key
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

class DeletedCart(TemplateView):

    def get(self, request):
        if request.is_ajax:
            id =request.GET.get("id")
          
            car=Cart(self.request)
            result=car.remove(id=id) 
            return JsonResponse({'succes':result}, safe=False)
        return TemplateResponse(request, reverse('dashboard'))

##### Confirmar Evento Carrito de Compra #####

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
# HTTP Error 400
# def bad_request(request,exception):
#     response = render_to_response(
#         '400.html',
#         context_instance=RequestContext(request)
#         )

#     response.status_code = 400

#     return response

# def permission_denied(request,exception):
#     response = render_to_response(
#         '403.html',
#         context_instance=RequestContext(request)
#         )

#     response.status_code = 400

#     return response

# def page_not_found(request,exception):
#     response = render_to_response(
#         '404.html',
#         context_instance=RequestContext(request)
#         )

#     response.status_code = 400

#     return response

# def server_error(request):
#     response = render_to_response(
#         '400.html',
#         context_instance=RequestContext(request)
#         )

#     response.status_code = 400

#     return response

