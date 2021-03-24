import json
from django import forms
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views.defaults import page_not_found
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import JsonResponse,HttpResponse
from django.urls import reverse, reverse_lazy
from django.utils.crypto import get_random_string
from django.views.generic import CreateView, ListView, TemplateView
from django.views.generic.edit import DeleteView, FormView, UpdateView
from MedCongressAdmin.forms.nomencladores_forms import CatPagoForm
from MedCongressApp.models import CategoriaPagoCongreso,RelCongresoCategoriaPago
from MedCongressAdmin.apps import validarUser
from django.db.models import Q       

class CatPagoListView(validarUser,ListView):
    model = CategoriaPagoCongreso
    context_object_name = 'cat_pagos'
    template_name = 'nomencladores/cat_pago/index.html'

class CatPagoCreateView(validarUser,CreateView):
    model=CategoriaPagoCongreso
    form_class = CatPagoForm
    success_url = reverse_lazy('MedCongressAdmin:cat_pagos_list')
    template_name = 'nomencladores/cat_pago/form.html'
    
    def form_valid(self, form):

        cat_pago=form.save(commit=False)       
        path=cat_pago.nombre.replace("/","").replace(" ","-").replace("?","").replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("ñ","n")
        chars = '0123456789'
        secret_key = get_random_string(5, chars)
        cat_pago.path=path+secret_key  
        cat_pago.save()
        return super().form_valid(form)

class CatPagoDeletedView(validarUser,DeleteView):
    model = CategoriaPagoCongreso
    

    def delete(self,request, *args, **kwargs):
           
            cat_pago=CategoriaPagoCongreso.objects.get(pk=self.kwargs.get('pk'))
            if RelCongresoCategoriaPago.objects.filter(categoria= cat_pago).exists():
                return JsonResponse({'success':False}, safe=False)
            else:
                cat_pago.delete()
                return JsonResponse({'success':True}, safe=False)

class CatPagoUpdateView(validarUser,UpdateView):
    form_class = CatPagoForm
    success_url = reverse_lazy('MedCongressAdmin:cat_pagos_list')
    template_name = 'nomencladores/cat_pago/form.html'

    def get_queryset(self, **kwargs):
        return CategoriaPagoCongreso.objects.filter(pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['update']=True
        return context

class vTableAsJSONCatPago(TemplateView):
    template_name = 'MedCongressAdmin/asig_congress_form.html'
    
    def get(self, request, *args, **kwargs):
        #arreglo con las columnas de la BD a filtrar
        col_name_map = ['nombre']
           
        #listado que muestra en dependencia de donde estes parado
        object_list = CategoriaPagoCongreso.objects.all()
        
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
            filtered_object_list = object_list.filter(Q(nombre__icontains=search_text))

        #Guardar datos en un 
        enviar =[]
       
            # if objet.ponente:
            #     user= '%s %s'%(objet.ponente.first().user.usuario.first_name,objet.ponente.first().user.usuario.last_name)
           
           #Guardar datos en un dic 
        for objet in filtered_object_list[start:(start+delta)]:
            
            enviar.append({ 'nombre':objet.nombre,
                            'operaciones' : 
                                                    ''' <a href="'''+ reverse('MedCongressAdmin:cat_pago_edit',kwargs={'pk':objet.pk})+'''"
                                                    title="Editar"><i class="icon icon-editar"></i></a>
                                                    <a id="del_'''+ str(objet.pk)+'''"
                                                        href="javascript:deleteItem('''+ str(objet.pk)+''')"
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
    
