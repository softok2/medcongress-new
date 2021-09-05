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
from MedCongressApp.models import Bloque, Congreso, Ponencia, Taller, RelBloqueModerador,Moderador,Organizador,Sala
from MedCongressAdmin.apps import validarUser,validarOrganizador
    

class SalasListView(validarOrganizador,TemplateView):
    template_name= 'MedCongressAdmin/sala/listar.html' 
    def get(self, request, **kwargs):
        congreso=Congreso.objects.filter(path=self.kwargs.get('path')).first()
        if congreso is None:
            return   HttpResponseRedirect(reverse('Error404'))
        if not Organizador.objects.filter(user=self.request.user.perfilusuario,congreso=congreso).exists() and not self.request.user.is_staff: 
            return   HttpResponseRedirect(reverse('Error403'))
        return self.render_to_response(self.get_context_data())    
    def get_context_data(self, **kwargs):
        context = super(SalasListView, self).get_context_data(**kwargs)
        congreso=Congreso.objects.filter(path=self.kwargs.get('path')).first()
        context['congres']=congreso
        context['salas']=Sala.objects.filter(congreso=congreso).order_by('orden')
        return context          

class vTableAsJSONCongresoSalas(TemplateView):
    template_name = 'MedCongressAdmin/asig_congress_form.html'
    
    def get(self, request, *args, **kwargs):
        #arreglo con las columnas de la BD a filtrar
        col_name_map = ['orden','titulo']
        congreso=Congreso.objects.filter(path=request.GET.get('path')).first() 
        #listado que muestra en dependencia de donde estes parado
        object_list = Sala.objects.filter(congreso=congreso).order_by('orden')
        
        #parametros 
        search_text = request.GET.get('sSearch', '').lower()# texto a buscar
        # start = int(request.GET.get('iDisplayStart', 0))#por donde empezar a mostrar
        # delta = int(request.GET.get('iDisplayLength', 10))#cantidad a mostrar
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
            filtered_object_list = object_list.filter(Q(titulo__icontains=search_text))

        #Guardar datos en un 
        enviar =[]
       
            # if objet.ponente:
            #     user= '%s %s'%(objet.ponente.first().user.usuario.first_name,objet.ponente.first().user.usuario.last_name)
           
           #Guardar datos en un dic 
        for objet in filtered_object_list:

            enviar.append({ 
                            'id' : str(objet.pk),
                            'orden' : str(objet.orden),
                            'titulo':objet.titulo,         
                            'color' : str(objet.color),
                           
                            'operaciones' :'''  <a href="'''+ reverse('MedCongressAdmin:congres_sala_editar',kwargs={'path':request.GET.get('path'),'pk':objet.pk})+'''"
                                                        title="Editar" style="margin-left: 5px;"><i class="icon-editar" style="padding: 15px;"></i></a>
                                                    <a id="del_'''+str(objet.pk)+'''"
                                                        href="javascript:deleteItem('''+str(objet.pk)+''')"
                                                        title="Eliminar" style="margin-left: 5px;">
                                                        <i class="icon-eliminar" style="padding: 15px;"></i>
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

# class  CongressSalaCreateView(validarUser,CreateView):
#     info_sended =Congreso()
#     form_class = CongresoSalaForm
   
#     template_name = 'MedCongressAdmin/congreso_sala_form.html'
#     def get_form_kwargs(self, *args, **kwargs):
#         kwargs = super().get_form_kwargs(*args, **kwargs)
#         kwargs['sala'] = False
#         return kwargs
#     def form_valid(self, form):
#         congreso=form.save(commit=False)
#         if congreso.orden:
#             salas=Sala.objects.filter(orden__gte=congreso.orden,congreso=congreso.congreso)
#             for sala in salas:
#                 sala.orden=sala.orden+1
#                 sala.save()
#         else:
#             congreso.orden=Sala.objects.filter(congreso=congreso.congreso).count()+1
#         chars = '0123456789'
        
#         image_64_encode=self.request.POST['prueba_home']
#         campo = image_64_encode.split(",")
#         nombre = get_random_string(5, chars)
#         image_64_decode = base64.decodestring(bytes(campo[1], encoding='utf8'))
#         image_result = open('MedCongressApp/static/sala/imagen_%s.png'%(nombre), 'wb') # create a writable image and write the decoding result
#         image_result.write(image_64_decode) 
#         congreso.imagen='sala/imagen_%s.png'%(nombre)
#         nombre = get_random_string(3, chars)
#         path=congreso.titulo.replace("/","").replace(" ","-").replace("?","").replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("ñ","n")
#         congreso.path=path+nombre
       
#         congreso.ponencia_streamming=None
#         congreso.save()
#         return super(CongressSalaCreateView, self).form_valid(form)

#     def get_success_url(self):
#            self.success_url =  reverse_lazy('MedCongressAdmin:Congres_salas',kwargs={'path': self.kwargs.get('path')} )
#            return self.success_url

#     def get_context_data(self, **kwargs):
#         ctx = super(CongressSalaCreateView, self).get_context_data(**kwargs)
#         pon=Congreso.objects.filter(path=self.kwargs.get('path')).first()
#         ctx['cong'] = pon
#         return ctx
# class CongressSalaUpdateView(validarUser,UpdateView):

#     form_class = CongresoSalaForm
#     template_name = 'MedCongressAdmin/congreso_sala_form.html'

#     def get_queryset(self, **kwargs):
#         return Sala.objects.filter(pk=self.kwargs.get('pk'))

#     def get_form_kwargs(self, *args, **kwargs):
#         kwargs = super().get_form_kwargs(*args, **kwargs)
#         kwargs['sala'] = Sala.objects.get(pk=self.kwargs.get('pk'))
#         return kwargs

#     def form_valid(self, form):
#         congreso=form.save(commit=False)
#         if not self.request.POST.get('ponencia_streamming'):
#             congreso.ponencia_streamming=None
#         sala_update=Sala.objects.get(pk=self.kwargs.get('pk'))
#         chars = '0123456789'
#         if congreso.orden:
#             if  not Sala.objects.filter(orden=sala_update.orden,congreso=congreso.congreso).exclude(pk=self.kwargs.get('pk')).exists():
#                 if congreso.orden <= sala_update.orden:
#                     salas=Sala.objects.filter(orden__lt=sala_update.orden,orden__gte=congreso.orden,congreso=congreso.congreso)
#                     for sala in salas:
#                         sala.orden=sala.orden+1
#                         sala.save()
#                 else:
#                     salas=Sala.objects.filter(orden__lte=congreso.orden,orden__gt=sala_update.orden,congreso=congreso.congreso)
#                     for sala in salas:
#                         sala.orden=sala.orden-1
#                         sala.save()

#         else:
#             congreso.orden=sala_update.orden
            
#         imagen_prim=self.request.POST['prueba_home']
#         if 'sala/' not in imagen_prim:
#             image_64_encode=self.request.POST['prueba_home']
#             campo = image_64_encode.split(",")
#             nombre = get_random_string(5, chars)
#             image_64_decode = base64.decodestring(bytes(campo[1], encoding='utf8'))
#             image_result = open('MedCongressApp/static/sala/imagen_%s.png'%(nombre), 'wb') # create a writable image and write the decoding result
#             image_result.write(image_64_decode)
#             if  sala_update.imagen:
#                 fileObj = Path('MedCongressApp/static/%s'%( sala_update.imagen))
#                 if fileObj.is_file():
#                     remove('MedCongressApp/static/%s'%( sala_update.imagen))
#             congreso.imagen='sala/imagen_%s.png'%(nombre)

#         if not congreso.path or congreso.path=='0':
#             nombre = get_random_string(3, chars)
#             path=congreso.titulo.replace("/","").replace(" ","-").replace("?","").replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("ñ","n")
#             congreso.path=path+nombre
#         congreso.save()
#         return super(CongressSalaUpdateView, self).form_valid(form)

#     def get_context_data(self, **kwargs):
#         context=super().get_context_data(**kwargs)
#         context['update']=True
#         context['sala']= Sala.objects.get(pk=self.kwargs.get('pk'))
#         self.object = context['sala']
        
#         if self.object.meta_og_imagen:
#             context['imagen_meta']='/static/%s'%(self.object.meta_og_imagen)
        
#         context['imagen']=context['sala'].imagen
#         pon=Congreso.objects.filter(path=self.kwargs.get('path')).first()
#         context['cong'] = pon
#         return context
#     def get_success_url(self):
#            self.success_url =  reverse_lazy('MedCongressAdmin:Congres_salas',kwargs={'path': self.kwargs.get('path')} )
#            return self.success_url

# class CongressDeletedSalaView(validarUser,DeleteView):
#     model = Sala

#     def delete(self,request, *args, **kwargs):
           
#             sala=Sala.objects.get(pk=self.kwargs.get('pk'))
#             if Ponencia.objects.filter(sala= sala).exists():
#                 return JsonResponse({'success':False}, safe=False)
#             else:
#                 salas=Sala.objects.filter(orden__gt=sala.orden,congreso=sala.congreso)
#                 for sal in salas:
#                     sal.orden=sal.orden-1
#                     sal.save()
#                 sala.delete()
#                 return JsonResponse({'success':True}, safe=False)
class OrdenarSalaView(validarOrganizador,TemplateView):
    
    def post(self, request, **kwargs):
        sala=Sala.objects.get(pk=self.request.POST.get('id'))
        sala.orden=self.request.POST.get('pos')
        sala.save()
        return JsonResponse({'success':True}, safe=False)
      
       

