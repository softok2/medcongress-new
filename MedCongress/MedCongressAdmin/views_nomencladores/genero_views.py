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
from MedCongressAdmin.forms.nomencladores_forms import GeneroForm
from MedCongressApp.models import Genero,PerfilUsuario
from MedCongressAdmin.apps import validarUser
from django.db.models import Q    

class GeneroListView(validarUser,ListView):
    model = Genero
    context_object_name = 'generos'
    template_name = 'nomencladores/genero/index.html'

class GeneroCreateView(validarUser,CreateView):
    model=Genero
    form_class = GeneroForm
    success_url = reverse_lazy('MedCongressAdmin:generos_list')
    template_name = 'nomencladores/genero/form.html'
    

class GeneroDeletedView(validarUser,DeleteView):
    model = Genero
    success_url = reverse_lazy('MedCongressAdmin:generos_list')

    def delete(self,request, *args, **kwargs):
            
        genero=Genero.objects.get(pk=self.kwargs.get('pk'))
       
        if PerfilUsuario.objects.filter(genero=genero).exists():
            return JsonResponse({'success':False}, safe=False)
        else:
            genero.delete()
            return JsonResponse({'success':True}, safe=False)

class GeneroUpdateView(validarUser,UpdateView):
    form_class = GeneroForm
    success_url = reverse_lazy('MedCongressAdmin:generos_list')
    template_name = 'nomencladores/genero/form.html'

    def get_queryset(self, **kwargs):
        return Genero.objects.filter(pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['update']=True
        return context

class vTableAsJSONGenero(TemplateView):
    template_name = 'MedCongressAdmin/asig_congress_form.html'
    
    def get(self, request, *args, **kwargs):
        #arreglo con las columnas de la BD a filtrar
        col_name_map = ['denominacion']
           
        #listado que muestra en dependencia de donde estes parado
        object_list = Genero.objects.all()
        
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
            filtered_object_list = object_list.filter(Q(denominacion__icontains=search_text))

        #Guardar datos en un 
        enviar =[]
       
            # if objet.ponente:
            #     user= '%s %s'%(objet.ponente.first().user.usuario.first_name,objet.ponente.first().user.usuario.last_name)
           
           #Guardar datos en un dic 
        for objet in filtered_object_list[start:(start+delta)]:
            
            enviar.append({ 'denominacion':objet.denominacion,
                            'operaciones' : 
                                                    ''' <a href="'''+ reverse('MedCongressAdmin:genero_edit',kwargs={'pk':objet.pk})+'''"
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
