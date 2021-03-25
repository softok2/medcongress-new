import json
from os import remove
from django import forms
from django.contrib import messages
from django.http import HttpResponseBadRequest, HttpResponseRedirect,HttpResponse
from django.urls import reverse_lazy,reverse
from django.views.generic import ListView,CreateView,TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.edit import  DeleteView, UpdateView,FormView
from MedCongressApp.models import Documento
from MedCongressAdmin.forms.repositorio_form import RepositorioForm
from MedCongressAdmin.apps import validarUser
from django.http import JsonResponse
from  MedCongressApp.claves import URL_SITE
from django.db.models import Q  


class DocumentosListView(validarUser,ListView):
    model = Documento
    context_object_name = 'documentos'
    template_name = 'MedCongressAdmin/repositorio_list.html'
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['documentos']=Documento.objects.all().order_by('pk')
        context['host']=URL_SITE
        return context


class DocumentoCreateView(validarUser,CreateView):
    model=Documento
    form_class = RepositorioForm
    success_url = reverse_lazy('MedCongressAdmin:documentos_list')
    template_name = 'MedCongressAdmin/repositorio_form.html'

#  
class DocumentoDeletedView(validarUser,DeleteView):
    model = Documento
    success_url = reverse_lazy('MedCongressAdmin:documentos_list')

    def delete(self,request, *args, **kwargs):

        try:    
            documento=Documento.objects.get(pk=self.kwargs.get('pk'))
            remove('MedCongressApp/static/%s'%(documento.documento))
            documento.delete()
            
            return JsonResponse({'success':True}, safe=False)
        except FileNotFoundError :
            return JsonResponse({'success':False,'mensaje':'No se pudo eliminar este Documento'}, safe=False)
        # if RelCongresoAval.objects.filter(aval=patrocinadores).exists():
        #     return JsonResponse({'success':False}, safe=False)
        # else:
        #     patrocinadores.delete()
        #     

class vTableAsJSONRepositorio(TemplateView):
    template_name = 'MedCongressAdmin/asig_congress_form.html'
    
    def get(self, request, *args, **kwargs):
        #arreglo con las columnas de la BD a filtrar
        col_name_map = ['titulo']
           
        #listado que muestra en dependencia de donde estes parado
        object_list = Documento.objects.all()
        
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
            filtered_object_list = object_list.filter(Q(titulo__icontains=search_text))

        #Guardar datos en un 
        enviar =[]
       
            # if objet.ponente:
            #     user= '%s %s'%(objet.ponente.first().user.usuario.first_name,objet.ponente.first().user.usuario.last_name)
           
           #Guardar datos en un dic 
        for objet in filtered_object_list[start:(start+delta)]:
          
            enviar.append({ 'nombre':objet.titulo,
                            'url':'''<p id="doc_'''+ str(objet.pk)+'''" class="text"  >'''+URL_SITE+'''/static/'''+str(objet.documento)+'''</p>''',
                            'operaciones' : ''' <a id="del_'''+ str(objet.pk)+'''"
                                                    href="javascript:copiarAlPortapapeles('doc_'''+ str(objet.pk)+'''')"
                                                    title="Copiar URL">
                                                    <i class="icon icon-copy_link"></i> </a>
                                                     <a id="" target="_blank"
                                                    href="'''+URL_SITE+'''/static/'''+str(objet.documento)+'''"
                                                        title="Descargar" style="margin-left: 5px;">
                                                        <i class="icon icon-downloads" > </i>
                                                    </a> 
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
    

