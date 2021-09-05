from django import forms
import base64
import json
from django.contrib import messages
from os import remove
from pathlib import Path
from django.shortcuts import get_object_or_404
from django.views.defaults import page_not_found
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseBadRequest, HttpResponseRedirect,HttpResponse
from django.urls import reverse, reverse_lazy
from django.http import JsonResponse
from django.utils.crypto import get_random_string
from django.views.generic import CreateView, ListView, TemplateView
from django.views.generic.edit import DeleteView, FormView, UpdateView
from MedCongressAdmin.forms.congres_forms import BloqueForms,ModeradorBloqueForm,SelectPonencia
from MedCongressApp.models import Bloque, Congreso,RelCongresoUser, Ponencia, Taller, RelBloqueModerador,Moderador,Organizador,Sala
from MedCongressAdmin.apps import validarUser,validarOrganizador
    

class vTableAsJSONBecaCongreso(TemplateView):
    template_name = 'MedCongressAdmin/asig_congress_form.html'
    
    def get(self, request, *args, **kwargs):
        #arreglo con las columnas de la BD a filtrar
        col_name_map = ['user__usuario__first_name','user__usuario__email','congreso__titulo','cantidad','categoria_pago__nombre','is_pagado','is_constancia']
           
        #listado que muestra en dependencia de donde estes parado

        if request.user.is_staff:
            object_list = RelCongresoUser.objects.filter(is_beca=True)
        else:
            congreso_orgs=Organizador.objects.filter(user=request.user.perfilusuario)
            object_list=RelCongresoUser.objects.filter(pk=0)
            for organizador in congreso_orgs:
                object_list |=RelCongresoUser.objects.filter(is_beca=True,congreso=organizador.congreso)
        
        
        #parametros 
        search_text = request.GET.get('sSearch', '').lower()# texto a buscar
        start = int(request.GET.get('iDisplayStart', 0))#por donde empezar a mostrar
        delta = int(request.GET.get('iDisplayLength', 10))#cantidad a mostrar
        sort_dir = request.GET.get('sSortDir_0', 'asc')# direccion a ordenar
        sort_col = int(request.GET.get('iSortCol_0', 0)) # numero de la columna a ordenar
        sort_col_name = request.GET.get('mDataProp_%s' % sort_col, '1')
        sort_dir_prefix = (sort_dir == 'desc' and '-' or '') #sufijo para poner en la consulta para ordenar

        #para ordenar el listado
        
        sort_colr = col_name_map[sort_col]
        object_list = object_list.order_by('%s%s' % (sort_dir_prefix,sort_colr))

        #para filtrar el listado
        filtered_object_list = object_list
        if len(search_text) > 0:
            filtered_object_list = object_list.filter(Q(user__usuario__last_name__icontains=search_text) | Q(user__usuario__email__icontains=search_text)|Q(user__usuario__first_name__icontains=search_text)|Q(congreso__titulo__icontains=search_text)|Q(cantidad__icontains=search_text)|Q(categoria_pago__nombre__icontains=search_text))

        #Guardar datos en un 
        enviar =[]
       
            # if objet.ponente:
            #     user= '%s %s'%(objet.ponente.first().user.usuario.first_name,objet.ponente.first().user.usuario.last_name)
           
           #Guardar datos en un dic 
        for objet in filtered_object_list[start:(start+delta)]:
           
           
            constancia='Si'
            
            if objet.foto_constancia or RelCongresoUser.objects.filter(congreso=objet.congreso,user=objet.user,is_constancia=True).exists():
                        constancia='''Si'''                                         
            else:
                constancia= '''<a href="'''+ reverse('MedCongressAdmin:constancia_usuario_add',kwargs={'pk':objet.pk})+'''?search='''+request.GET.get('search')+'''"
                                                    title="Asignar Constancia">
                                                    <i class="icon icon-constancia"></i>
                                                </a>'''   
           
            enviar.append({ 'usuario':'%s %s'%(objet.user.usuario.first_name,objet.user.usuario.last_name),
                            'email':'<p class="text"  >'+ objet.user.usuario.email+'</p>',
                            'congreso' : objet.congreso.titulo,
                            'cantidad' : objet.cantidad,
                            'cat_pago':'Beca',
                            'constancia':constancia,
                            'operaciones' : 
                                                    '''<a id="del_'''+ str(objet.pk)+'''"
                                                        href="javascript:deleteItem('''+ str(objet.pk)+''')"
                                                        title="Eliminar">
                                                        <i class="icon icon-eliminar"></i>
                                                    </a>''',
                            
            })
        #parametros para la respuesta
        jsoner = {
            
            "iTotalRecords": filtered_object_list.count(),
            "iTotalDisplayRecords": filtered_object_list.count(),
            "sEcho": request.GET.get('sEcho', 1),
            "data": enviar
        }
        data = json.dumps(jsoner)
        mimetype = "application/json"
        #Enviar
        return HttpResponse(data, mimetype)    

class BecasCongressListView(validarOrganizador,ListView):
    
    template_name = 'MedCongressAdmin/becas_congreso.html'
   
    
    def post(self, request, **kwargs):
        try:
            prueba =True
            archivo=self.request.FILES['exel']
            if archivo:
                filename = archivo.name
            else:
                 raise ValidationError('Debe subir un Exel')   
            if(not filename.endswith(".xls") and not filename.endswith(".xlsx")):
                raise ValidationError('Debe subir un Exel')
               
            elif filename.endswith(".xls"):
                df = pd.read_excel(archivo)
                df=df.applymap(lambda x: {} if isnull(x) else x)
                rows=df.to_dict('records')
                if not rows[0]['Correo'] or not rows[0]['Congreso']:
                    raise ValidationError('Debe subir un Exel')
                resultado=AsignarBeca.apply_async(args=[rows])
            else: 
                df = pd.read_excel(archivo, engine='openpyxl')
                df=df.applymap(lambda x: {} if isnull(x) else x)
                rows=df.to_dict('records')
                if not rows[0]['Correo'] or not rows[0]['Congreso']:
                    raise ValidationError('Debe subir un Exel')
                resultado=AsignarBeca.apply_async(args=[rows])
            if resultado=='congreso':
                messages.warning(self.request, 'En este exel hay nombres de congreso que no existen en el sistema')
            if resultado=='usuario':
                messages.warning(self.request, 'En este exel hay correos que no son validos y no se guardaron en el sistema')
            return HttpResponseRedirect(reverse('MedCongressAdmin:asig_becas_list'))
        except ValidationError as e:
            messages.warning(self.request, 'Debe entrar un archivo <b> EXEL (*.xls o *.xlsx)</b>')
            return HttpResponseRedirect(reverse('MedCongressAdmin:asig_becas_list'))
        except OSError :
            messages.warning(self.request, 'No está entrando los datos bien en el Exel')
            return HttpResponseRedirect(reverse('MedCongressAdmin:asig_becas_list'))
        except KeyError :
            messages.warning(self.request, 'No está entrando los datos bien en el Exel')
            return HttpResponseRedirect(reverse('MedCongressAdmin:asig_becas_list'))
        except ValueError:
            messages.warning(self.request, 'El tamaño de letra del exel debe ser menor de 14')
            return HttpResponseRedirect(reverse('MedCongressAdmin:asig_becas_list'))
    def get_queryset(self):
        
        queryset=RelCongresoUser.objects.filter(is_beca=True)
       
        return queryset
    def get_context_data(self, **kwargs):
        context = super(BecasCongressListView, self).get_context_data(**kwargs)
        congresos= Congreso.objects.all()
        if self.request.GET.get('exportar'):
            congreso_evn=[]
           
            activo=False
            for congreso in congresos:
                if congreso.path == self.request.GET.get('exportar'):
                    activo=True
                else:
                    activo=False
                congreso_evn.append({ 'id':congreso.pk,
                                    'titulo':congreso.titulo,
                                        'activo':activo,

                })
            context['exportar']= congreso_evn
        context['congresos']= congresos
            
        return context  
    