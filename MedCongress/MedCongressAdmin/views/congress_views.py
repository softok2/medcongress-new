import json

import pandas as pd
from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Sum
from django.db import connections
from datetime import datetime
from django.core.mail import EmailMessage

from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseRedirect, JsonResponse)
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils.crypto import get_random_string
from django.views.generic import ListView, TemplateView
from PIL import Image, ImageDraw, ImageFont
from django.views.generic.edit import (CreateView, DeleteView, FormView,
                                       UpdateView)
from MedCongressAdmin.forms.congres_forms import (AsignarCongresoForms,
                                                  CongresoCategPagoForm,
                                                  CongresoForms,
                                                  CongresoPatrocinadorForm,
                                                  CongresoSocioForm,
                                                  ExportarExelForm,
                                                  ImagenCongForms,
                                                  PonenciaForms)
from MedCongressApp.models import (AvalCongreso, Bloque, CategoriaPagoCongreso,
                                   Congreso, CuestionarioPregunta,
                                   CuestionarioRespuestas, ImagenCongreso,
                                   PerfilUsuario, Ponencia, Ponente,
                                   PreguntasFrecuentes, RelCongresoAval,
                                   RelCongresoCategoriaPago, RelCongresoSocio,
                                   RelCongresoUser, SocioCongreso, Taller,
                                   Ubicacion, User,Moderador,RelPonenciaPonente,RelTalleresCategoriaPago,
                                   RelTallerUser)
from openpyxl import Workbook
from openpyxl.styles import (Alignment, Border, Font, PatternFill, Protection,
                             Side)
from MedCongressAdmin.apps import validarUser
from MedCongressAdmin.task import Constancia


class ReporteRelCongresoUserExcel(validarUser,TemplateView):
    
    #Usamos el método get para generar el archivo excel 
    def post(self, request):
        #Obtenemos todas las personas de nuestra base de datos
        congreso=self.request.POST['congreso']
        query= RelCongresoUser.objects.filter(congreso=congreso).values('user__usuario__first_name','user__usuario__last_name','user__usuario__email','congreso__titulo','categoria_pago__nombre').annotate(Sum('cantidad'))

		#Creamos el libro de trabajo
        wb = Workbook()
		#Definimos como nuestra hoja de trabajo, la hoja activa, por defecto la primera del libro
        ws = wb.active
       
		#En la celda B1 ponemos el texto 'REPORTE DE PERSONAS'
        ws['B1'] = 'Usuarios que han comprado el Congresos %s'%(query[0]['congreso__titulo'])
        ws['B1'].font = Font(size=12,bold=True)
        ws['B1'].alignment = Alignment(mergeCell='center',horizontal='center') 
        
		#Juntamos las celdas desde la B1 hasta la E1, formando una sola celda
        ws.merge_cells('B1:E1')
		#Creamos los encabezados desde la celda B3 hasta la E3
        ws['A3'] = 'No.'
        ws['B3'] = 'Nombre'
        ws['C3'] = 'Email'
        ws['D3'] = 'Congreso'
        ws['E3'] = 'Categoria de Pago'
        ws['F3'] = 'Cantidad'        
        cont=4
        #Recorremos el conjunto de personas y vamos escribiendo cada uno de los datos en las celdas
        for quer in query:
            ws.cell(row=cont,column=1).value = cont-3
            ws.cell(row=cont,column=2).value = '%s %s'%(quer['user__usuario__first_name'],quer['user__usuario__last_name'])
            ws.cell(row=cont,column=3).value = quer['user__usuario__email']
            ws.cell(row=cont,column=4).value = quer['congreso__titulo']
            ws.cell(row=cont,column=5).value = quer['categoria_pago__nombre']
            ws.cell(row=cont,column=6).value = quer['cantidad__sum']
            cont = cont + 1
		
        response = HttpResponse(content_type="application/ms-excel") 
        response["Content-Disposition"] = "attachment; filename=RelCongresoUser.xlsx"
        wb.save(response)
        return response

class CongressListView(validarUser,ListView):
    model = Congreso
    context_object_name = 'congress'
    template_name = 'MedCongressAdmin/congress.html'

class CongressCreateView(validarUser,FormView):
    form_class = CongresoForms
    success_url = reverse_lazy('MedCongressAdmin:congress_list')
    template_name = 'MedCongressAdmin/congres_form.html'

    def form_valid(self, form):
        try:
            congress=form['congreso'].save(commit=False)
            imagen=form['imagen_congreso'].save(commit=False)
            ubic=Ubicacion.objects.filter(direccion=form['ubicacion'].instance.direccion)
            if ubic.exists():
                congress.lugar=ubic.first()
            else:
                ubicacion=form['ubicacion'].save(commit=True)
                congress.lugar=ubicacion    
            path=congress.titulo.replace("/","").replace(" ","-").replace("?","").replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("ñ","n")
            congress.path=path  
            congress.save()
            imagen.congreso=congress
            imagen.save()
            return super().form_valid(form)
        except Exception as e:
            messages.warning(self.request, e)
            return super().form_invalid(form)

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
            'imagen_congreso':ImagenCongreso.objects.filter(congreso=self.object).first()
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        imagen=ImagenCongreso.objects.filter(congreso=self.object).first()
        context['update']=True
        if imagen:
            context['imagen']=imagen.imagen
        if self.object.imagen_seg:
            context['imagen_seg_url']='/static/%s'%(self.object.imagen_seg)
        if self.object.programa:
            context['programa']=self.object.programa
        if self.object.meta_og_imagen:
            context['imagen_meta']='/static/%s'%(self.object.meta_og_imagen)
        if self.object.foto_constancia:
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
    template_name= 'MedCongressAdmin/talleres.html' 
    
    def get(self, request, **kwargs):
        congreso=Congreso.objects.filter(path=self.kwargs.get('path')).first()
        if congreso is None:
            return   HttpResponseRedirect(reverse('Error404'))
        return self.render_to_response(self.get_context_data())    
    def get_context_data(self, **kwargs):
        context = super(CongressTalleresListView, self).get_context_data(**kwargs)
        congreso=Congreso.objects.filter(path=self.kwargs.get('path')).first()
        context['congres']=congreso
        context['talleres']=Taller.objects.filter(congreso=congreso)
        return context


########## Vista de las Ponencias de un Congreso #############

class CongressPonenciasListView(validarUser,TemplateView):
    template_name= 'MedCongressAdmin/ponencias.html' 

    def get(self, request, **kwargs):
        congreso=Congreso.objects.filter(path=self.kwargs.get('path')).first()
        if congreso is None:
            return   HttpResponseRedirect(reverse('Error404'))
        return self.render_to_response(self.get_context_data())
         
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        congreso=Congreso.objects.filter(path=self.kwargs.get('path')).first()
        context['congres']=congreso
        context['ponencias']=Ponencia.objects.filter(congreso=congreso)
        context['all_ponencias']=Ponencia.objects.filter(published=True).exclude(congreso=congreso)
        return context

########## Vista del cuestionario de un Congreso #############

class CongressCuestionarioListView(validarUser,TemplateView):
    template_name= 'MedCongressAdmin/cuestionarios.html' 
    def get(self, request, **kwargs):
        congreso=Congreso.objects.filter(path=self.kwargs.get('path')).first()
        if congreso is None:
            return   HttpResponseRedirect(reverse('Error404'))
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
       
        return context
    
########## Vista de las Categorias de Pago de un Congreso #############

class CongressCategPagosListView(validarUser,TemplateView):
    template_name= 'MedCongressAdmin/congres_cat_pagos.html' 
    

    def get(self, request, **kwargs):
        congreso=Congreso.objects.filter(path=self.kwargs.get('path')).first()
        if congreso is None:
            return   HttpResponseRedirect(reverse('Error404'))
        return self.render_to_response(self.get_context_data())    
    def get_context_data(self, **kwargs):
        context = super(CongressCategPagosListView, self).get_context_data(**kwargs)
        congreso=Congreso.objects.filter(path=self.kwargs.get('path')).first()
        context['congres']=congreso
        context['cat_pagos']=RelCongresoCategoriaPago.objects.filter(congreso=congreso)
        return context        
        
########## Vista de las Imagenes de un Congreso #############

class CongressImagenesListView(validarUser,TemplateView):
    template_name= 'MedCongressAdmin/congres_imagenes.html' 
    

    def get(self, request, **kwargs):
        congreso=Congreso.objects.filter(path=self.kwargs.get('path')).first()
        if congreso is None:
            return   HttpResponseRedirect(reverse('Error404'))
        return self.render_to_response(self.get_context_data())    
    def get_context_data(self, **kwargs):
        context = super(CongressImagenesListView, self).get_context_data(**kwargs)
        congreso=Congreso.objects.filter(path=self.kwargs.get('path')).first()
        context['congres']=congreso
        context['imagenes']=ImagenCongreso.objects.filter(congreso=congreso)
        return context    

##### Adicionar ponencia al congreso a Carrito de Compra #####

class AddPonenciaCongreso(validarUser,TemplateView):
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
        pon=Congreso.objects.filter(path=self.kwargs.get('path')).first()
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
        pon=Congreso.objects.filter(path=self.kwargs.get('path')).first()
        ctx['cong'] = pon
        return ctx

class CongressBloquesListView(validarUser,TemplateView):
    template_name= 'MedCongressAdmin/bloques.html'  

    def get(self, request, **kwargs):
        congreso=Congreso.objects.filter(path=self.kwargs.get('path')).first()
        if congreso is None:
            return   HttpResponseRedirect(reverse('Error404'))
        return self.render_to_response(self.get_context_data())    
    def get_context_data(self, **kwargs):
        context = super(CongressBloquesListView, self).get_context_data(**kwargs)
        congreso=Congreso.objects.filter(path=self.kwargs.get('path')).first()
        context['congres']=congreso
        context['bloques']=Bloque.objects.filter(congreso=congreso)
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

class AsignarCongressListView(validarUser,ListView,FormView):
    model = RelCongresoUser
    context_object_name = 'congress'
    template_name = 'MedCongressAdmin/asignar_congreso.html'
    form_class=ExportarExelForm
    
    def form_valid(self, form):
        return super().form_valid(form)
    # def post(self, form):

    #     id_congreso=self.request.POST['congreso']
    #     query= RelCongresoUser.objects.filter(congreso=id_congreso).values('user__usuario__first_name','user__usuario__last_name','user__usuario__email','congreso__titulo','categoria_pago__nombre').annotate(Sum('cantidad'))
        
    #     print(query)
	# 	#Creamos el libro de trabajo
    #     wb = Workbook()
	# 	#Definimos como nuestra hoja de trabajo, la hoja activa, por defecto la primera del libro
    #     ws = wb.active
       
	# 	#En la celda B1 ponemos el texto 'REPORTE DE PERSONAS'
    #     ws['B1'] = 'Usuarios que han comprado Congresos'
    #     ws['B1'].font = Font(size=12,bold=True)
    #     ws['B1'].alignment = Alignment(mergeCell='center',horizontal='center') 
        
	# 	#Juntamos las celdas desde la B1 hasta la E1, formando una sola celda
    #     ws.merge_cells('B1:E1')
	# 	#Creamos los encabezados desde la celda B3 hasta la E3
    #     ws['A3'] = 'No.'
    #     ws['B3'] = 'Nombre'
    #     ws['C3'] = 'Email'
    #     ws['D3'] = 'Congreso'
    #     ws['E3'] = 'Categoria de Pago'
    #     ws['F3'] = 'Cantidad'        
    #     cont=4
    #     #Recorremos el conjunto de personas y vamos escribiendo cada uno de los datos en las celdas
    #     for quer in query:
    #         ws.cell(row=cont,column=1).value = cont-3
    #         ws.cell(row=cont,column=2).value ='%s %s'%(quer['user__usuario__first_name'],quer['user__usuario__last_name']) 
    #         ws.cell(row=cont,column=3).value = quer['user__usuario__email']
    #         ws.cell(row=cont,column=4).value = quer['congreso__titulo']
    #         ws.cell(row=cont,column=5).value = quer['categoria_pago__nombre']
    #         ws.cell(row=cont,column=6).value = quer['cantidad__sum']
    #         cont = cont + 1
		
    #     response = HttpResponse(content_type="application/ms-excel") 
    #     response["Content-Disposition"] = "attachment; filename=RelCongresoUser.xlsx"
    #     wb.save(response)
    #     return response

class AsignarCongressAddViews(validarUser,FormView):
    form_class = AsignarCongresoForms
    success_url = reverse_lazy('MedCongressAdmin:asig_congress_list')
    template_name = 'MedCongressAdmin/asig_congress_form.html'

    def form_valid(self, form):
        congress=form.save(commit=True)
        
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super(AsignarCongressAddViews, self).get_context_data(**kwargs)
        if self.kwargs.get('pk'):
            usuario=PerfilUsuario.objects.get(pk=self.kwargs.get('pk'))
            ctx['usuario'] = usuario

       
        return ctx    

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
        cong=Congreso.objects.filter(pk=self.kwargs.get('pk')).first()
        ctx['cong'] = cong
        return ctx
    def get_success_url(self):
        congreso=Congreso.objects.get(pk=self.kwargs.get('pk'))
        self.success_url =  reverse_lazy('MedCongressAdmin:Congres_imagenes',kwargs={'path': congreso.path} )
        return self.success_url

class CongressImagenDeletedView(validarUser,DeleteView):
    model = ImagenCongreso
    success_url = reverse_lazy('MedCongressAdmin:cat_usuarios_list')

    
########## Vista del Preguntas Frecuentes de un Congreso #############

class CongressPregFrecuenteListView(validarUser,TemplateView):
    template_name= 'MedCongressAdmin/preg_frecuentes.html' 
    def get(self, request, **kwargs):
        congreso=Congreso.objects.filter(path=self.kwargs.get('path')).first()
        if congreso is None:
            return   HttpResponseRedirect(reverse('Error404'))
        return self.render_to_response(self.get_context_data()) 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        congreso=Congreso.objects.filter(path=self.kwargs.get('path')).first()
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

class Ver_Exel(validarUser,TemplateView):

    template_name='MedCongressAdmin/ver_exel.html'

class Exportar_usuarios(validarUser,TemplateView):
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

class Usuarios_pagaron(validarUser,TemplateView):
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

########## Vista de las Patrocinadores de un Congreso #############

class CongressPatrocinadorListView(validarUser,TemplateView):
    template_name= 'nomencladores/patrocinadores/index.html' 
    

    def get(self, request, **kwargs):
        congreso=Congreso.objects.filter(path=self.kwargs.get('path')).first()
        if congreso is None:
            return   HttpResponseRedirect(reverse('Error404'))
        return self.render_to_response(self.get_context_data())    
    def get_context_data(self, **kwargs):
        context = super(CongressPatrocinadorListView, self).get_context_data(**kwargs)
        congreso=Congreso.objects.filter(path=self.kwargs.get('path')).first()
        context['congreso']=congreso
        rel_patroc_usuarios=RelCongresoAval.objects.filter(congreso=congreso)
        patrocinadores_env=[]
        for relacion in rel_patroc_usuarios:
            patrocinadores_env.append(relacion.aval)
        context['patrocinadores']=patrocinadores_env
        return context    


   
class  PatrocinadorSeleccionarView(validarUser,FormView):
    
    model=RelCongresoAval
    form_class = CongresoPatrocinadorForm
    # success_url = reverse_lazy('MedCongressAdmin:ponencias_list')
    template_name='MedCongressAdmin/congress_patrocinador_form.html'
   
    def get(self, request, **kwargs):
        congreso=Congreso.objects.filter(path=self.kwargs.get('path')).first()
        if congreso is None:
            return   HttpResponseRedirect(reverse('Error404'))    
        return self.render_to_response(self.get_context_data()) 
    def get_success_url(self):
           self.success_url =  reverse_lazy('MedCongressAdmin:Congres_patrocinadores',kwargs={'path': self.kwargs.get('path')} )
           return self.success_url

    def get_context_data(self, **kwargs):
        context = super(PatrocinadorSeleccionarView, self).get_context_data(**kwargs)
        
        pon=Congreso.objects.filter(path=self.kwargs.get('path')).first()
       
        context['congreso'] = pon
        return context
    def form_valid(self, form):
    
       
        relacion_aval=form.save(commit=True)
       
        return super().form_valid(form)

def PatrocinadorSeleccionarDeleted( request):
        
    if request.is_ajax():
        id_aval =request.GET.get("pk")
        patrocinador=AvalCongreso.objects.get(pk=id_aval)
        id_congreso=request.GET.get("pk_congreso")
        congreso=Congreso.objects.get(pk=id_congreso)
        relacion= RelCongresoAval.objects.filter(congreso=congreso,aval=patrocinador)
       
        if relacion.exists():
            relacion.first().delete()
            return JsonResponse({'success':True}, safe=False)
    return JsonResponse({'success':False}, safe=False)

def SocioSeleccionarDeleted( request):
        
    if request.is_ajax():
        id_socio =request.GET.get("pk")
        socio=SocioCongreso.objects.get(pk=id_socio)
        id_congreso=request.GET.get("pk_congreso")
        congreso=Congreso.objects.get(pk=id_congreso)
        relacion= RelCongresoSocio.objects.filter(congreso=congreso,socio=socio)
        if relacion.exists():
            relacion.first().delete()
            return JsonResponse({'success':True}, safe=False)
    return JsonResponse({'success':False}, safe=False)


class  SocioSeleccionarView(validarUser,FormView):
    
    model=RelCongresoSocio
    form_class = CongresoSocioForm
    # success_url = reverse_lazy('MedCongressAdmin:ponencias_list')
    template_name='MedCongressAdmin/congress_socio_form.html'
   
    def get(self, request, **kwargs):

        
        congreso=Congreso.objects.filter(path=self.kwargs.get('path')).first()
        if congreso is None:
            return   HttpResponseRedirect(reverse('Error404'))
             
        return self.render_to_response(self.get_context_data()) 
    def get_success_url(self):
           self.success_url =  reverse_lazy('MedCongressAdmin:Congres_socios',kwargs={'path': self.kwargs.get('path')} )
           return self.success_url

    def get_context_data(self, **kwargs):
        context = super(SocioSeleccionarView, self).get_context_data(**kwargs)
        
        pon=Congreso.objects.filter(path=self.kwargs.get('path')).first()
       
        context['congreso'] = pon
        return context
    def form_valid(self, form):
    
       
        relacion_aval=form.save(commit=True)
       
        return super().form_valid(form)


########## Vista de las Patrocinadores de un Congreso #############

class CongressSocioListView(validarUser,TemplateView):
    template_name= 'nomencladores/socios/index.html' 
    

    def get(self, request, **kwargs):
        congreso=Congreso.objects.filter(path=self.kwargs.get('path')).first()
        if congreso is None:
            return   HttpResponseRedirect(reverse('Error404'))
        return self.render_to_response(self.get_context_data())    
    def get_context_data(self, **kwargs):
        context = super(CongressSocioListView, self).get_context_data(**kwargs)
        congreso=Congreso.objects.filter(path=self.kwargs.get('path')).first()
        context['congreso']=congreso
        rel_patroc_usuarios=RelCongresoSocio.objects.filter(congreso=congreso)
        patrocinadores_env=[]
        for relacion in rel_patroc_usuarios:
            patrocinadores_env.append(relacion.socio)
        context['socios']=patrocinadores_env
        return context 

class CongresoDetail(validarUser,TemplateView):
    # template_name= 'MedCongressApp/congreso_detail.html' 
    

    def get(self, request, **kwargs):
        congreso=Congreso.objects.filter(path=self.kwargs.get('path')).first()
        if congreso is None:
            return   HttpResponseRedirect(reverse('Error404'))
        return self.render_to_response(self.get_context_data())

    def get_template_names(self):
        congreso=Congreso.objects.filter(path=self.kwargs.get('path')).first()
        if congreso.is_openpay:
            template_name= 'MedCongressApp/congreso_detail_openpay.html'
        else:
            template_name= 'MedCongressApp/%s'%(congreso.template)
        return template_name

    def get_context_data(self, **kwargs):
        context = super(CongresoDetail, self).get_context_data(**kwargs)
        congreso=Congreso.objects.filter(path=self.kwargs.get('path')).first()
        context['patrocinadores']=RelCongresoAval.objects.filter(congreso=congreso)
        context['socios']=RelCongresoSocio.objects.filter(congreso=congreso)
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
                        'ver_ponencia':ponencia.cod_video,
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
                    'ver_ponencia':ponencia.cod_video,
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

            prueba_ponecia=Ponencia.objects.filter(congreso=congreso.pk,published=True)
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
                'apellido': ponente.user.usuario.last_name ,
                'foto':ponente.user.foto,
                'tipo':'Ponente',
                })
            ponencias_video_env=[]

            fechas_ponencias_video=Ponencia.objects.filter(congreso=congreso.pk,published=True).exclude(cod_video='').distinct('fecha_inicio__date').values('fecha_inicio__date')
            fechas_talleres_video=Taller.objects.filter(congreso=congreso.pk,published=True).exclude(cod_video='').distinct('fecha_inicio__date').values('fecha_inicio__date')
            
            fechas=[]
            for fecha_ponencia in fechas_ponencias_video:
                fechas.append(fecha_ponencia['fecha_inicio__date'])
            for fechas_tallere in fechas_talleres_video:
                fechas.append(fechas_tallere['fecha_inicio__date'])
            
            fechas=set(fechas)
            fechas_final=sorted(fechas)
            
            for j in range(0, len(fechas_final)):
                ponencias_video= Ponencia.objects.filter(congreso=congreso.pk,published=True,fecha_inicio__date=fechas_final[j]).exclude(cod_video='')
                talleres_video= Taller.objects.filter(congreso=congreso.pk,published=True,fecha_inicio__date=fechas_final[j]).exclude(cod_video='')
                ponencias_video_env.append({'fecha':fechas_final[j],
                                            'ponencias':ponencias_video,
                                            'talleres':talleres_video})
            context['ponencias_video']=ponencias_video_env
            prueba_taller=Taller.objects.filter(congreso=congreso.pk,published=True)
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
                    'apellido': ponente.user.usuario.last_name ,
                    'foto':ponente.user.foto,
                    'tipo':'Ponente',
                    })
            
            bloques=Bloque.objects.filter(congreso=congreso.pk,published=True)
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
                    'apellido': moderador.user.usuario.last_name ,
                    'foto':moderador.user.foto,
                    'tipo':'Moderador',
                    })


            context['ponentes_congreso']=ponentes_env
            cat_pago=RelCongresoCategoriaPago.objects.filter(congreso=congreso.pk)
            context['cat_ponente']=RelPonenciaPonente.objects.all()

            if self.request.user.is_authenticated :
                user_perfil=PerfilUsuario.objects.filter(usuario=self.request.user.pk).first()
                talleres=Taller.objects.filter(congreso=congreso.pk,published=True).order_by('fecha_inicio')
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
                talleres=Taller.objects.filter(congreso=congreso.pk,published=True).order_by('fecha_inicio')
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

            context['preg_frecuentes']=PreguntasFrecuentes.objects.filter(congreso=congreso,published=True)

        return context

class CongressCategPagosUpdateView(validarUser,UpdateView):

    form_class = CongresoCategPagoForm
    success_url = reverse_lazy('MedCongressAdmin:ponencias_list')
    template_name = 'MedCongressAdmin/congreso_cat_pago_form.html'

    def get_queryset(self, **kwargs):
        return RelCongresoCategoriaPago.objects.filter(pk=self.kwargs.get('pk'))


    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['update']=True
        context['categoria']= RelCongresoCategoriaPago.objects.get(pk=self.kwargs.get('pk'))
        pon=Congreso.objects.filter(path=self.kwargs.get('path')).first()
        context['cong'] = pon
        return context
    def get_success_url(self):
           self.success_url =  reverse_lazy('MedCongressAdmin:Congres_pagos',kwargs={'path': self.kwargs.get('path')} )
           return self.success_url
    # def form_valid(self, form):
        
    #     pregunta =CuestionarioPregunta.objects.get(pk=self.request.POST['update'])   
    #     pregunta.pregunta=self.request.POST['pregunta']
    #     pregunta.published=self.request.POST['published']
    #     pregunta.save()
    #     CuestionarioRespuestas.objects.filter(pregunta=pregunta).delete()
    #     cant=0
    #     for respuesta in self.request.POST.getlist('respuesta'):
    #         resp=CuestionarioRespuestas(pregunta=pregunta,respuesta=respuesta,published=self.request.POST.getlist('published_resp')[cant],is_correcto=self.request.POST.getlist('is_correcto')[cant])
    #         resp.save() 
    #         cant=cant+1  
    #     return super(CustionarioUpdateView, self).form_valid(form)
    # def get_initial(self):
    #     initial=super().get_initial()
    #     pregunta=CuestionarioPregunta.objects.get(pk=self.kwargs.get('pk'))
    #     initial['pregunta']=pregunta.pregunta
    #     initial['published']=pregunta.published
    #     return initial

    # def get_success_url(self):
    #     if self.kwargs.get('pk'):
    #         pregunta=CuestionarioPregunta.objects.get(pk=self.kwargs.get('pk'))
            
    #         self.success_url =  reverse_lazy('MedCongressAdmin:Congres_cuestionario',kwargs={'path': pregunta.congreso.path} )
    #     return self.success_url 


class CongressCategPagosDeletedView(validarUser,DeleteView):
    model = RelCongresoCategoriaPago
    success_url = reverse_lazy('MedCongressAdmin:cat_usuarios_list')

class AsignarConstancias(validarUser,TemplateView):
    template_name = 'MedCongressAdmin/asig_constancia.html'

    def post(self, request, **kwargs):
        # congreso=Congreso.objects.filter(titulo=self.request.POST['my_congress']).first()
        # if congreso:
        #     rel_usuario_congreso=RelCongresoUser.objects.filter(congreso=congreso ).distinct('user')
           
        #     for usuario in rel_usuario_congreso:
        #             # //////////////
        #         nombre='%s %s'%(usuario.user.usuario.first_name,usuario.user.usuario.last_name)
                
        #         cont=len(nombre)
        #         comienzo=450-(cont/2*19) 
        #         base=Image.open('MedCongressApp/static/%s'%(congreso.foto_constancia)).convert('RGBA')
        #         text=Image.new('RGBA',base.size,(255,255,255,0))
        #         # nombre_font=ImageFont.truetype('calibri.ttf',40)
        #         nombre_font=ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans.ttf", 28, encoding="unic")
        #         # cong.set_variation_by_name('Italic')
        #         d=ImageDraw.Draw(text)
        #         d.text((comienzo,290),nombre,font=nombre_font,fill=(89, 85, 85))
                
                
        #         out=Image.alpha_composite(base,text)
        #         tit=congreso.titulo.replace("/","").replace(" ","-").replace("?","").replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("ñ","n")
        #         tit_nombre=nombre.replace("/","").replace(" ","-").replace("?","").replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("ñ","n")
        #         nombre_img='constancia_%s_%s'%(tit_nombre,tit)  
        #         out.save('MedCongressApp/static/congreso/img_constancia/%s.png'%(nombre_img))
        #         usuario.is_constancia=True
        #         usuario.foto_constancia='%s.png'%(nombre_img)
        #         usuario.fecha_constancia=datetime.now()
        #         usuario.save()
        #         # ////////////////
        #         if usuario.user.usuario.email =='frankhef91@gmail.com':
        #             email = EmailMessage('Constancia', 'En este correo se le adjunta la constancia de haber participado en el congreso %s.'%(congreso.titulo), to = [usuario.user.usuario.email])
        #             email.attach_file('MedCongressApp/static/congreso/img_constancia/%s.png'%(nombre_img))
        #             email.send()

        

                # ////
        return HttpResponse(Constancia.delay())

