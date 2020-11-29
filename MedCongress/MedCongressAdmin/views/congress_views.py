import json
from django import forms
import pandas as pd
from django.contrib import messages
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse_lazy,reverse
from django.utils.crypto import get_random_string
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.views.generic import ListView,TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView,FormView
from MedCongressApp.models import (Congreso,Taller,Ponencia,RelCongresoCategoriaPago,ImagenCongreso,Ubicacion
                                    ,Bloque,RelCongresoUser,RelCongresoCategoriaPago,CuestionarioPregunta,CuestionarioRespuestas,PreguntasFrecuentes,
                                    CategoriaPagoCongreso,User,PerfilUsuario,Ponente)
from MedCongressAdmin.forms.congres_forms import CongresoForms,PonenciaForms,CongresoCategPagoForm,AsignarCongresoForms,ImagenCongForms

class validarUser(UserPassesTestMixin):
    permission_denied_message = 'No tiene permiso para acceder a la administracion'
    login_url='/admin/login/'
    def test_func(self):
       
        if self.request.user.is_staff :
            return True
        else:
            return False
    

class CongressListView(validarUser,ListView):
    model = Congreso
    context_object_name = 'congress'
    template_name = 'MedCongressAdmin/congress.html'

class CongressCreateView(validarUser,FormView):
    form_class = CongresoForms
    success_url = reverse_lazy('MedCongressAdmin:congress_list')
    template_name = 'MedCongressAdmin/congres_form.html'

    def form_valid(self, form):
    
       
        congress=form['congreso'].save(commit=False)
       
        ubic=Ubicacion.objects.filter(direccion=form['ubicacion'].instance.direccion)

        if ubic.exists():
            congress.lugar=ubic.first()
        else:
            ubicacion=form['ubicacion'].save(commit=True)
            congress.lugar=ubicacion
               
        path=congress.titulo.replace("/","").replace(" ","-").replace("?","").replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("ñ","n")
        chars = '0123456789'
        secret_key = get_random_string(5, chars)
        congress.path=path+secret_key  
        congress.save()
        return super().form_valid(form)
    

class CongressUpdateView(validarUser,UpdateView):
    form_class = CongresoForms
    success_url = reverse_lazy('MedCongressAdmin:congress_list')
    template_name = 'MedCongressAdmin/congres_form.html'

    def get_queryset(self, **kwargs):
        return Congreso.objects.filter(pk=self.kwargs.get('pk'))
    
    def get_form_kwargs(self):
        kwargs = super(CongressUpdateView, self).get_form_kwargs()
        kwargs.update(instance={
            'congreso': self.object,
            'ubicacion': self.object.lugar,
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['imagen_seg_url']='/static/%s'%(self.object.imagen_seg)
        context['foto_constancia']='/static/%s'%(self.object.foto_constancia)
        return context

    # def get_context_data(self, **kwargs):
    #     context = super(CountryUpdateView, self).get_context_data(**kwargs)
    #     context['form_title'] = 'Editar'
    #     context['delete_url'] = reverse_lazy(
    #         'MedCongressAdmin:country_delete', kwargs={'pk': self.object.pk})
    #     return context

    # def form_invalid(self, form):
    #     for error in form.errors:
    #         form[error].field.widget.attrs['class'] += ' is-invalid'
    #     return super(CountryUpdateView, self).form_invalid(form)

########## Vista de los talleres de un Congreso #############

class CongressTalleresListView(validarUser,TemplateView):
    template_name= 'MedCongressAdmin/congres_talleres.html' 
    

    def get(self, request, **kwargs):
        congreso=Congreso.objects.filter(path=self.kwargs.get('path'),published=True).first()
        if congreso is None:
            return   HttpResponseRedirect(reverse('Error404'))
        return self.render_to_response(self.get_context_data())    
    def get_context_data(self, **kwargs):
        context = super(CongressTalleresListView, self).get_context_data(**kwargs)
        congreso=Congreso.objects.filter(path=self.kwargs.get('path'),published=True).first()
        context['congres']=congreso
        context['talleres']=Taller.objects.filter(congreso=congreso,published=True)
        return context


########## Vista de las Ponencias de un Congreso #############

class CongressPonenciasListView(validarUser,TemplateView):
    template_name= 'MedCongressAdmin/congres_ponencias.html' 
    form_class = PonenciaForms
    def get(self, request, **kwargs):
        congreso=Congreso.objects.filter(path=self.kwargs.get('path'),published=True).first()
        if congreso is None:
            return   HttpResponseRedirect(reverse('Error404'))
        return self.render_to_response(self.get_context_data())
         
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        congreso=Congreso.objects.filter(path=self.kwargs.get('path'),published=True).first()
        context['congres']=congreso
        context['ponencias']=Ponencia.objects.filter(congreso=congreso)
        context['all_ponencias']=Ponencia.objects.filter(published=True).exclude(congreso=congreso)
        return context

########## Vista del cuestionario de un Congreso #############

class CongressCuestionarioListView(validarUser,TemplateView):
    template_name= 'MedCongressAdmin/cuestionarios.html' 
    def get(self, request, **kwargs):
        congreso=Congreso.objects.filter(path=self.kwargs.get('path'),published=True).first()
        if congreso is None:
            return   HttpResponseRedirect(reverse('Error404'))
        return self.render_to_response(self.get_context_data()) 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        congreso=Congreso.objects.filter(path=self.kwargs.get('path'),published=True).first()
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
       
        return context
    
########## Vista de las Categorias de Pago de un Congreso #############

class CongressCategPagosListView(TemplateView):
    template_name= 'MedCongressAdmin/congres_cat_pagos.html' 
    

    def get(self, request, **kwargs):
        congreso=Congreso.objects.filter(path=self.kwargs.get('path'),published=True).first()
        if congreso is None:
            return   HttpResponseRedirect(reverse('Error404'))
        return self.render_to_response(self.get_context_data())    
    def get_context_data(self, **kwargs):
        context = super(CongressCategPagosListView, self).get_context_data(**kwargs)
        congreso=Congreso.objects.filter(path=self.kwargs.get('path'),published=True).first()
        context['congres']=congreso
        context['cat_pagos']=RelCongresoCategoriaPago.objects.filter(congreso=congreso)
        return context        
        
########## Vista de las Imagenes de un Congreso #############

class CongressImagenesListView(TemplateView):
    template_name= 'MedCongressAdmin/congres_imagenes.html' 
    

    def get(self, request, **kwargs):
        congreso=Congreso.objects.filter(path=self.kwargs.get('path'),published=True).first()
        if congreso is None:
            return   HttpResponseRedirect(reverse('Error404'))
        return self.render_to_response(self.get_context_data())    
    def get_context_data(self, **kwargs):
        context = super(CongressImagenesListView, self).get_context_data(**kwargs)
        congreso=Congreso.objects.filter(path=self.kwargs.get('path'),published=True).first()
        context['congres']=congreso
        context['imagenes']=ImagenCongreso.objects.filter(congreso=congreso)
        return context    

##### Adicionar ponencia al congreso a Carrito de Compra #####

class AddPonenciaCongreso(TemplateView):
    def get(self, request):
        
        if request.is_ajax:
            
            id_ponencia =request.GET.get("id_ponencia")
            congreso_path =request.GET.get("congreso")
            
            congreso=Congreso.objects.get(path=congreso_path)
            ponencia=Ponencia.objects.get(id=id_ponencia)
            ponencia.congreso=congreso
            ponencia.save()
            return JsonResponse({'succes':True}, safe=False)
        return TemplateResponse(request, reverse('home'))



class  CongressCategPagosCreateView(validarUser,CreateView):
    info_sended =Congreso()
    form_class = CongresoCategPagoForm
    # success_url = reverse_lazy('MedCongressAdmin:ponencias_list')
    template_name = 'MedCongressAdmin/congreso_cat_pago_form.html'
    def form_valid(self, form):
        congreso=form.save(commit=False)
  
        congreso.save()
        return super(CongressCategPagosCreateView, self).form_valid(form)

    def get_success_url(self):
           self.success_url =  reverse_lazy('MedCongressAdmin:Congres_pagos',kwargs={'path': self.kwargs.get('path')} )
           return self.success_url

    def get_context_data(self, **kwargs):
        ctx = super(CongressCategPagosCreateView, self).get_context_data(**kwargs)
        pon=Congreso.objects.filter(path=self.kwargs.get('path'),published=True).first()
        ctx['cong'] = pon
        return ctx

class CongressDeletedView(validarUser,DeleteView):
    model = Congreso
    success_url = reverse_lazy('MedCongressAdmin:congress_list')
    # template_name = 'MedCongressAdmin/country_form.html'

   
class  CongressPonenteCreateView(validarUser,CreateView):
   
    form_class = CongresoCategPagoForm
    # success_url = reverse_lazy('MedCongressAdmin:ponencias_list')
    template_name = 'MedCongressAdmin/congreso_ponencia_form.html'
    def form_valid(self, form):
        ponencia=form.save(commit=False)
        ponencia.save()
        return super(CongressPonenteCreateView, self).form_valid(form)

    def get_success_url(self):
           self.success_url =  reverse_lazy('MedCongressAdmin:Congres_pagos',kwargs={'id': self.kwargs.get('path')} )
           return self.success_url

    def get_context_data(self, **kwargs):
        ctx = super(CongressCategPagosCreateView, self).get_context_data(**kwargs)
        pon=Congreso.objects.filter(path=self.kwargs.get('path'),published=True).first()
        ctx['cong'] = pon
        return ctx

class CongressBloquesListView(validarUser,TemplateView):
    template_name= 'MedCongressAdmin/congres_bloques.html'  

    def get(self, request, **kwargs):
        congreso=Congreso.objects.filter(path=self.kwargs.get('path'),published=True).first()
        if congreso is None:
            return   HttpResponseRedirect(reverse('Error404'))
        return self.render_to_response(self.get_context_data())    
    def get_context_data(self, **kwargs):
        context = super(CongressBloquesListView, self).get_context_data(**kwargs)
        congreso=Congreso.objects.filter(path=self.kwargs.get('path'),published=True).first()
        context['congres']=congreso
        context['bloques']=Bloque.objects.filter(congreso=congreso,published=True)
        return context

def GetBloques(request):
    if request.is_ajax():
        query = request.POST['congreso_id']
        bloques=Bloque.objects.filter(congreso=Congreso.objects.get(pk=query))
        results = []
        for bloque in bloques:
            results.append({'titulo':bloque.titulo,'id':bloque.pk})
            data = json.dumps(results)
    mimetype = "application/json"
    return HttpResponse(data, mimetype)
def GetPagos(request):
    if request.is_ajax():
        query = request.POST['congreso_id']
        categoria=RelCongresoCategoriaPago.objects.filter(congreso=Congreso.objects.get(pk=query))
       
        results = []
        for cat in categoria:
            results.append({'nombre':cat.categoria.nombre,'id':cat.categoria.pk})
            data = json.dumps(results)
    mimetype = "application/json"
    return HttpResponse(data, mimetype)   

class AsignarCongressListView(validarUser,ListView):
    model = RelCongresoUser
    context_object_name = 'congress'
    template_name = 'MedCongressAdmin/asignar_congreso.html'


class AsignarCongressAddViews(validarUser,FormView):
    form_class = AsignarCongresoForms
    success_url = reverse_lazy('MedCongressAdmin:asig_congress_list')
    template_name = 'MedCongressAdmin/asig_congress_form.html'

    def form_valid(self, form):
        congress=form.save(commit=True)
        return super().form_valid(form)

class AsignarCongressDeletedViews(validarUser,DeleteView):
    model = RelCongresoUser
    success_url = reverse_lazy('MedCongressAdmin:asig_congress_list')
    
class CongressImagenCreateView(validarUser,FormView):
    form_class = ImagenCongForms
    success_url = reverse_lazy('MedCongressAdmin:Congres_imagenes')
    template_name = 'MedCongressAdmin/imagen_congress_form.html'

    def form_valid(self, form):
        imagen=form.save(commit=True)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super(CongressImagenCreateView, self).get_context_data(**kwargs)
        cong=Congreso.objects.filter(pk=self.kwargs.get('pk'),published=True).first()
        ctx['cong'] = cong
        return ctx
    def get_success_url(self):
        congreso=Congreso.objects.get(pk=self.kwargs.get('pk'))
        self.success_url =  reverse_lazy('MedCongressAdmin:Congres_imagenes',kwargs={'path': congreso.path} )
        return self.success_url


########## Vista del Preguntas Frecuentes de un Congreso #############

class CongressPregFrecuenteListView(validarUser,TemplateView):
    template_name= 'MedCongressAdmin/preg_frecuentes.html' 
    def get(self, request, **kwargs):
        congreso=Congreso.objects.filter(path=self.kwargs.get('path'),published=True).first()
        if congreso is None:
            return   HttpResponseRedirect(reverse('Error404'))
        return self.render_to_response(self.get_context_data()) 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        congreso=Congreso.objects.filter(path=self.kwargs.get('path'),published=True).first()
        preguntas_env=[]
        preguntas=PreguntasFrecuentes.objects.filter(congreso=congreso)
        context['preguntas']=preguntas
        context['congreso']=congreso
       
        return context

class Ver_usuarios (validarUser,TemplateView):

    template_name='MedCongressAdmin/ver_usuarios.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        congresos=Congreso.objects.all()
        cat_pago=CategoriaPagoCongreso.objects.all()
        context['congresos']=congresos
        context['cat_pagos']=cat_pago
       
        return context

    def post(self, request, **kwargs):

        id_congreso=self.request.POST['congresos']
        id_cat_pago=self.request.POST['cat_pago']
        cat_pago= CategoriaPagoCongreso.objects.get(pk=id_cat_pago)
        congreso= Congreso.objects.get(pk=id_congreso)
        archivo_excel = pd.read_excel(self.request.FILES['exel'])
        values = archivo_excel['Correo'].values
        ###################
        sin_pagar=[]
        for value in values:
            user=User.objects.filter(email=value).first()
            if PerfilUsuario.objects.filter(usuario=user).exists():
                if user :
                    relacion=RelCongresoUser.objects.filter(congreso=congreso,user=user.perfilusuario).first()
                    if relacion:
                        relacion.is_pagado=True
                        relacion.cantidad=1
                        relacion.save()
                    else:
                        rel=RelCongresoUser(congreso=congreso,user=user.perfilusuario,is_pagado=True,cantidad=1,categoria_pago=cat_pago)
                        rel.save()
                else:
                    sin_pagar.append(value)
            else:
                sin_pagar.append(value)
        data = {'Usuarios que no se han Autentificado': sin_pagar}
        df = pd.DataFrame(data, columns = ['Usuarios que no se han Autentificado'])
        df.to_excel('MedCongressApp/static/patrocinadores/example.xlsx', sheet_name='example')
       
        ###################

        return HttpResponseRedirect(reverse('MedCongressAdmin:Ver_exel' ))

class Ver_Exel(TemplateView):

    template_name='MedCongressAdmin/ver_exel.html'

class Exportar_usuarios(TemplateView):
    template_name='MedCongressAdmin/view_exportar_usuario.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        usuarios=  PerfilUsuario.objects.all()
        email=[]
        nombre=[]
        for usuario in usuarios:
            if Ponente.objects.filter(user=usuario).exists():
                email=email
            else:
                email.append(usuario.usuario.email)
                nombre.append('%s %s'%(usuario.usuario.first_name,usuario.usuario.last_name))
        data = {'Nombre y Apellidos':nombre,'Email': email}
        df = pd.DataFrame(data, columns = ['Nombre y Apellidos','Email'])
        df.to_excel('MedCongressApp/static/patrocinadores/user_registrados.xlsx', sheet_name='example')
        return context

class Usuarios_pagaron(TemplateView):
    template_name='MedCongressAdmin/view_pagaron_usuario.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        usurios_pagaron= RelCongresoUser.objects.all().distinct('user')
        email=[]
        nombre=[]
        for usuario in usurios_pagaron:
                email.append(usuario.user.usuario.email)
                nombre.append('%s %s'%(usuario.user.usuario.first_name,usuario.user.usuario.last_name))
        data = {'Nombre y Apellidos':nombre,'Email': email}
        df = pd.DataFrame(data, columns = ['Nombre y Apellidos','Email'])
        df.to_excel('MedCongressApp/static/patrocinadores/user_pagaron.xlsx', sheet_name='example')
        return context


