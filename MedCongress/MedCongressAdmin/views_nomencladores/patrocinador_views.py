import json
from django import forms
import base64
from os import remove
from pathlib import Path
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views.defaults import page_not_found
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import JsonResponse,HttpResponse
from django.urls import reverse, reverse_lazy
from django.utils.crypto import get_random_string
from django.views.generic import CreateView, ListView, TemplateView
from django.views.generic.edit import DeleteView, FormView, UpdateView
from MedCongressAdmin.forms.nomencladores_forms import PatrocinadorForm
from MedCongressApp.models import AvalCongreso,RelCongresoAval,Congreso
from MedCongressAdmin.apps import validarUser
from django.db.models import Q      
    

class PatrocinadorListView(validarUser,ListView):
    model = AvalCongreso
    context_object_name = 'patrocinadores'
    template_name = 'nomencladores/patrocinadores/index.html'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        if self.kwargs.get('pk'):
            congreso=Congreso.objects.get(pk=self.kwargs.get('pk'))
            context['congreso']=congreso
        return context
class PatrocinadorCreateView(validarUser,CreateView):
    model=AvalCongreso
    form_class = PatrocinadorForm
    success_url = reverse_lazy('MedCongressAdmin:patrocinadores_list')
    template_name = 'nomencladores/patrocinadores/form.html'
    
    def form_valid(self, form):
        
        patrocinador=form.save(commit=False)
        image_64_encode=self.request.POST['prueba']
        campo = image_64_encode.split(",")
        image_64_decode = base64.decodestring(bytes(campo[1], encoding='utf8')) 
        chars = '0123456789'
        nombre = get_random_string(5, chars)
        image_result = open('MedCongressApp/static/patrocinadores/imagen_%s.png'%(nombre), 'wb') # create a writable image and write the decoding result
        image_result.write(image_64_decode)
        patrocinador.logo='patrocinadores/imagen_%s.png'%(nombre)
        patrocinador.save()
        if self.request.POST.get('congreso'):
            id_congreso=self.request.POST['congreso']
            congreso=Congreso.objects.get(pk=id_congreso)
            relacion=RelCongresoAval(aval=patrocinador,congreso=congreso)
            relacion.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        if self.kwargs.get('pk'):
            congreso=Congreso.objects.get(pk=self.kwargs.get('pk'))
            context['congreso']=congreso
        return context

    def get_success_url(self, **kwargs):
        if self.kwargs.get('pk'):
            congres=Congreso.objects.get(pk=self.kwargs.get('pk'))
            self.success_url =  reverse_lazy('MedCongressAdmin:Congres_patrocinadores',kwargs={'path': congres.path} )
        return self.success_url

class PatrocinadorDeletedView(validarUser,DeleteView):
    model = AvalCongreso
    success_url = reverse_lazy('MedCongressAdmin:patrocinadores_list')

    def delete(self,request, *args, **kwargs):
            
        patrocinadores=AvalCongreso.objects.get(pk=self.kwargs.get('pk'))
       
        if RelCongresoAval.objects.filter(aval=patrocinadores).exists():
            return JsonResponse({'success':False}, safe=False)
        else:
            if patrocinadores.logo:
                fileObj = Path('MedCongressApp/static/%s'%( patrocinadores.logo))
                if fileObj.is_file():
                    remove('MedCongressApp/static/%s'%( patrocinadores.logo))
            patrocinadores.delete()
            return JsonResponse({'success':True}, safe=False)

class PatrocinadorUpdateView(validarUser,UpdateView):
    form_class = PatrocinadorForm
    success_url = reverse_lazy('MedCongressAdmin:patrocinadores_list')
    template_name = 'nomencladores/patrocinadores/form.html'

    def get_queryset(self, **kwargs):
        return AvalCongreso.objects.filter(pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['update']=True
        context['logo']='/static/%s'%(self.object.logo)
        return context

    def form_valid(self, form):
        try:
            patrocinador=form.save(commit=False)
            logo=self.request.POST['prueba']
            if 'patrocinadores/' not in logo:
                image_64_encode=self.request.POST['prueba']
                campo = image_64_encode.split(",")
                chars = '0123456789'
                nombre = get_random_string(5, chars)
                image_64_decode = base64.decodestring(bytes(campo[1], encoding='utf8'))
                image_result = open('MedCongressApp/static/patrocinadores/imagen_%s.png'%(nombre), 'wb') # create a writable image and write the decoding result
                image_result.write(image_64_decode)
                if patrocinador.logo:
                    fileObj = Path('MedCongressApp/static/%s'%(  patrocinador.logo))
                    if fileObj.is_file():
                        remove('MedCongressApp/static/%s'%( patrocinador.logo))
                patrocinador.logo='patrocinadores/imagen_%s.png'%(nombre)
            patrocinador.save()
            return super().form_valid(form)
        except ( TypeError,FileNotFoundError):
                return super().form_invalid(form)
class vTableAsJSONPatrocinador(TemplateView):
    template_name = 'MedCongressAdmin/asig_congress_form.html'
    
    def get(self, request, *args, **kwargs):
        #arreglo con las columnas de la BD a filtrar
        if request.GET.get('congreso'):
            col_name_map = ['aval__nombre']
        else:
             col_name_map = ['nombre'] 
           
        #listado que muestra en dependencia de donde estes parado
        if request.GET.get('congreso'):
            object_list = RelCongresoAval.objects.filter(congreso__pk=request.GET.get('congreso'))
        else:
            object_list = AvalCongreso.objects.all() 
        
        
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
            if request.GET.get('congreso'):
                filtered_object_list = object_list.filter(Q(aval__nombre__icontains=search_text))
            else:
                filtered_object_list = object_list.filter(Q(nombre__icontains=search_text))

        #Guardar datos en un 
        enviar =[]
       
            # if objet.ponente:
            #     user= '%s %s'%(objet.ponente.first().user.usuario.first_name,objet.ponente.first().user.usuario.last_name)
           
           #Guardar datos en un dic 
        for objet in filtered_object_list[start:(start+delta)]:
            if request.GET.get('congreso'):
                nombre=objet.aval.nombre
                operaciones='''  <a id="del_'''+ str(objet.pk)+'''"
                                                        href="javascript:deleteItemCongreso('''+ str(objet.aval.pk)+''')"
                                                        title="Eliminar de este Evento">
                                                        <i class="icon icon-eliminar_vinculo"></i>
                                                    </a>'''
            else:
                nombre=objet.nombre
                operaciones=''' <a href="'''+ reverse('MedCongressAdmin:patrocinador_edit',kwargs={'pk':objet.pk})+'''"
                                                    title="Editar"><i class="icon icon-editar"></i></a>
                                                    <a id="del_'''+ str(objet.pk)+'''"
                                                        href="javascript:deleteItem('''+ str(objet.pk)+''')"
                                                        title="Eliminar" style="margin-left: 5px;">
                                                        <i class="icon-eliminar" style="padding: 15px;"></i>
                                                    </a>'''
            enviar.append({ 'nombre':nombre,
                            
                            
                            'operaciones' : operaciones,
                            
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
    

