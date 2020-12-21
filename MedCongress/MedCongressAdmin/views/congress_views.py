import json

import pandas as pd
from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Sum
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseRedirect, JsonResponse)
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils.crypto import get_random_string
from django.views.generic import ListView, TemplateView
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
                                   Ubicacion, User)
from openpyxl import Workbook
from openpyxl.styles import (Alignment, Border, Font, PatternFill, Protection,
                             Side)


class ReporteRelCongresoUserExcel(TemplateView):
    
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
        try:
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
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['imagen_seg_url']='/static/%s'%(self.object.imagen_seg)
        if self.object.meta_og_imagen:
            context['imagen_meta']='/static/%s'%(self.object.meta_og_imagen)
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
        cong=Congreso.objects.filter(pk=self.kwargs.get('pk'),published=True).first()
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

########## Vista de las Patrocinadores de un Congreso #############

class CongressPatrocinadorListView(TemplateView):
    template_name= 'nomencladores/patrocinadores/index.html' 
    

    def get(self, request, **kwargs):
        congreso=Congreso.objects.filter(path=self.kwargs.get('path'),published=True).first()
        if congreso is None:
            return   HttpResponseRedirect(reverse('Error404'))
        return self.render_to_response(self.get_context_data())    
    def get_context_data(self, **kwargs):
        context = super(CongressPatrocinadorListView, self).get_context_data(**kwargs)
        congreso=Congreso.objects.filter(path=self.kwargs.get('path'),published=True).first()
        context['congreso']=congreso
        rel_patroc_usuarios=RelCongresoAval.objects.filter(congreso=congreso)
        patrocinadores_env=[]
        for relacion in rel_patroc_usuarios:
            patrocinadores_env.append(relacion.aval)
        context['patrocinadores']=patrocinadores_env
        return context    

# class CongressPatrocinadorCreateView(validarUser,FormView):
#     form_class = ImagenCongForms
#     success_url = reverse_lazy('MedCongressAdmin:Congres_patrocinador')
#     template_name = 'MedCongressAdmin/imagen_congress_form.html'

#     def form_valid(self, form):
#         imagen=form.save(commit=True)

#         return super().form_valid(form)

#     def get_context_data(self, **kwargs):
#         ctx = super(CongressImagenCreateView, self).get_context_data(**kwargs)
#         cong=Congreso.objects.filter(pk=self.kwargs.get('pk'),published=True).first()
#         ctx['cong'] = cong
#         return ctx
#     def get_success_url(self):
#         congreso=Congreso.objects.get(pk=self.kwargs.get('pk'))
#         self.success_url =  reverse_lazy('MedCongressAdmin:Congres_imagenes',kwargs={'path': congreso.path} )
#         return self.success_url

# class PatrocinadorSeleccionarView(validarUser,TemplateView):
#     template_name='MedCongressAdmin/congress_patrocinador_form.html'
#     form_class=CongresoPatrocinadorForm
    
#     def get_context_data(self, **kwargs):
#         ctx = super().get_context_data(**kwargs)
#         cong=Congreso.objects.filter(pk=self.kwargs.get('pk'),published=True).first()
#         ctx['cong'] = cong
#         return ctx

#     def get(self, request, **kwargs):
#         congreso=Congreso.objects.filter(path=self.kwargs.get('path'),published=True).first()
#         if congreso is None:
#             return   HttpResponseRedirect(reverse('Error404'))
#         return self.render_to_response(self.get_context_data())   
   
class  PatrocinadorSeleccionarView(validarUser,FormView):
    
    model=RelCongresoAval
    form_class = CongresoPatrocinadorForm
    # success_url = reverse_lazy('MedCongressAdmin:ponencias_list')
    template_name='MedCongressAdmin/congress_patrocinador_form.html'
   
    def get(self, request, **kwargs):
        congreso=Congreso.objects.filter(path=self.kwargs.get('path'),published=True).first()
        if congreso is None:
            return   HttpResponseRedirect(reverse('Error404'))    
        return self.render_to_response(self.get_context_data()) 
    def get_success_url(self):
           self.success_url =  reverse_lazy('MedCongressAdmin:Congres_patrocinadores',kwargs={'path': self.kwargs.get('path')} )
           return self.success_url

    def get_context_data(self, **kwargs):
        context = super(PatrocinadorSeleccionarView, self).get_context_data(**kwargs)
        
        pon=Congreso.objects.filter(path=self.kwargs.get('path'),published=True).first()
       
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

        
        congreso=Congreso.objects.filter(path=self.kwargs.get('path'),published=True).first()
        if congreso is None:
            return   HttpResponseRedirect(reverse('Error404'))
             
        return self.render_to_response(self.get_context_data()) 
    def get_success_url(self):
           self.success_url =  reverse_lazy('MedCongressAdmin:Congres_socios',kwargs={'path': self.kwargs.get('path')} )
           return self.success_url

    def get_context_data(self, **kwargs):
        context = super(SocioSeleccionarView, self).get_context_data(**kwargs)
        
        pon=Congreso.objects.filter(path=self.kwargs.get('path'),published=True).first()
       
        context['congreso'] = pon
        return context
    def form_valid(self, form):
    
       
        relacion_aval=form.save(commit=True)
       
        return super().form_valid(form)


########## Vista de las Patrocinadores de un Congreso #############

class CongressSocioListView(TemplateView):
    template_name= 'nomencladores/socios/index.html' 
    

    def get(self, request, **kwargs):
        congreso=Congreso.objects.filter(path=self.kwargs.get('path'),published=True).first()
        if congreso is None:
            return   HttpResponseRedirect(reverse('Error404'))
        return self.render_to_response(self.get_context_data())    
    def get_context_data(self, **kwargs):
        context = super(CongressSocioListView, self).get_context_data(**kwargs)
        congreso=Congreso.objects.filter(path=self.kwargs.get('path'),published=True).first()
        context['congreso']=congreso
        rel_patroc_usuarios=RelCongresoSocio.objects.filter(congreso=congreso)
        patrocinadores_env=[]
        for relacion in rel_patroc_usuarios:
            patrocinadores_env.append(relacion.socio)
        context['socios']=patrocinadores_env
        return context 
