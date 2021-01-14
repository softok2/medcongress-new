import json
from django import forms
from django.contrib import messages
from django.http import HttpResponseBadRequest, HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy,reverse
from django.views.generic import ListView,TemplateView,FormView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from MedCongressApp.models import Ponencia,RelPonenciaPonente,Ubicacion,Congreso,Bloque,Ponente,RelPonenciaPonente
from MedCongressAdmin.forms.congres_forms import PonenciaForms,PonentePonenciaForm
from django.utils.crypto import get_random_string
from MedCongressAdmin.apps import validarUser
from django.db.models import Q

class PonenciaListView(validarUser,ListView):
    model = Ponencia
    context_object_name = 'ponencias'
    template_name = 'MedCongressAdmin/ponencias.html'

class  PonenciaCreateView(validarUser,FormView):
    form_class = PonenciaForms
    success_url = reverse_lazy('MedCongressAdmin:ponencias_list')
    template_name = 'MedCongressAdmin/ponencia_form.html'
    def form_valid(self, form):
        try: 
            ponencia=form['ponencia'].save(commit=False)
            ubic=Ubicacion.objects.filter(direccion=form['ubicacion'].instance.direccion)
            relacion=form['ponencia_ponente'].save(commit=False)
            if ubic.exists():
                ponencia.lugar=ubic.first()
            else:
                ubicacion=form['ubicacion'].save(commit=True)
                ponencia.lugar=ubicacion
            path=ponencia.titulo.replace("/","").replace(" ","-").replace("?","").replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("ñ","n")
            chars = '0123456789'
            secret_key = get_random_string(5, chars)
            ponencia.path=path+secret_key
            id_video=['']
            if ponencia.cod_video:
                id_video=ponencia.cod_video.split(sep='https://player.vimeo.com/video/')
                id_video=id_video[-1].split(sep='"')
            ponencia.id_video=id_video[0]
            
            ponencia.save()
            relacion.ponencia=ponencia
            relacion.save()

            return super(PonenciaCreateView, self).form_valid(form)
        except Exception as e:
            messages.warning(self.request, e)
            return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        
        context = super(PonenciaCreateView, self).get_context_data(**kwargs)
        if self.kwargs.get('path'):
            context['con']=Congreso.objects.filter(path=self.kwargs.get('path')).first()
            context['blo']=Bloque.objects.filter(congreso=context['con'])
        if self.kwargs.get('pk_block'):
            context['bloque']=Bloque.objects.get(pk=self.kwargs.get('pk_block'))
            context['congreso']=context['bloque'].congreso
            context['blo']= None
        return context 
    
    def get_success_url(self):
        if self.kwargs.get('pk'):
            congreso=Congreso.objects.get(pk=self.kwargs.get('pk'))
            self.success_url =  reverse_lazy('MedCongressAdmin:Congres_ponencias',kwargs={'path': congreso.path} )
        if self.kwargs.get('pk_block'):
            block=Bloque.objects.get(pk=self.kwargs.get('pk_block'))
            self.success_url =  reverse_lazy('MedCongressAdmin:Bloque_ponencias',kwargs={'path': block.path} )
        return self.success_url   
 
########## Vista de las Categorias de Pago de un Congreso #############

class PonenciaPonenteListView(validarUser,TemplateView):
    template_name= 'MedCongressAdmin/ponencia_ponentes.html' 
    def get(self, request, **kwargs):
        ponencia=Ponencia.objects.filter(path=self.kwargs.get('path')).first()
        if ponencia is None:
            return   HttpResponseRedirect(reverse('Error404'))
        return self.render_to_response(self.get_context_data())    
    def get_context_data(self, **kwargs):
        context = super(PonenciaPonenteListView, self).get_context_data(**kwargs)
        ponencia=Ponencia.objects.filter(path=self.kwargs.get('path')).first()
        context['ponencia']=ponencia
        context['ponentes']=RelPonenciaPonente.objects.filter(ponencia=ponencia)
        return context        

class  PonenciaPonenteCreateView(validarUser,CreateView):
    info_sended =Ponencia()
    form_class = PonentePonenciaForm
    # success_url = reverse_lazy('MedCongressAdmin:ponencias_list')
    template_name = 'MedCongressAdmin/ponencia_ponente_form.html'

    

    def form_valid(self, form):
        ponencia=form.save(commit=False)
  
        ponencia.save()
        return super(PonenciaPonenteCreateView, self).form_valid(form)

    def get_success_url(self):
        
           self.success_url =  reverse_lazy('MedCongressAdmin:Ponencia_ponentes',kwargs={'path': self.kwargs.get('path')} )
           return self.success_url

    # def form_invalid(self, form):
    #     for error in form.errors:
    #         print(error)
    #         form[error].field.widget.attrs['class'] += ' is-invalid'
    #     return super(PonenciaPonenteCreateView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        ctx = super(PonenciaPonenteCreateView, self).get_context_data(**kwargs)
        pon=Ponencia.objects.filter(path=self.kwargs.get('path')).first()
        ctx['pon'] = pon
        ponentes=RelPonenciaPonente.objects.filter(ponencia=pon)
        id=[]
        for ponente in ponentes:
            id.append(ponente.ponente.pk)
        ctx['ponentes']=Ponente.objects.exclude(id__in=id)
        return ctx

class PonencicaUpdateView(validarUser,FormView):
    form_class = PonenciaForms
    success_url = reverse_lazy('MedCongressAdmin:ponencias_list')
    template_name = 'MedCongressAdmin/ponencia_form.html'

    def get_queryset(self, **kwargs):
        ponencia=Ponencia.objects.get(pk=self.kwargs.get('pk'))
        self.object=ponencia
        return ponencia
    
    def get_form_kwargs(self):
        ponencia=Ponencia.objects.get(pk=self.kwargs.get('pk'))
        ponencia.ponente.first().user.usuario.email
        self.object=ponencia
        kwargs = super(PonencicaUpdateView, self).get_form_kwargs()
        kwargs.update(instance={
            'ponencia': self.object,
            'ubicacion': self.object.lugar,
            'ponencia_ponente':RelPonenciaPonente.objects.filter(ponencia=self.object).first()
        })
        return kwargs

    def get_context_data(self, **kwargs):
        ponencia=Ponencia.objects.get(pk=self.kwargs.get('pk'))
        self.object=ponencia
        context=super().get_context_data(**kwargs)
        if self.kwargs.get('path'):
            context['congres']=Congreso.objects.filter(path=self.kwargs.get('path')).first()
        if self.object.imagen:
            context['imagen_seg_url']='/static/%s'%(self.object.imagen)
        if self.object.meta_og_imagen:
            context['imagen_meta']='/static/%s'%(self.object.meta_og_imagen)
        context['bloque_update']=self.object.bloque
        context['update']='update'
        context['ponencia']=self.object
        context['ponente']=self.object.ponente.first()
        return context

    def get_success_url(self):
        if self.kwargs.get('path'):
            self.success_url =  reverse_lazy('MedCongressAdmin:Congres_ponencias',kwargs={'path':self.kwargs.get('path')} )
        if self.kwargs.get('pk_block'):
            block=Bloque.objects.get(pk=self.kwargs.get('pk_block'))
            self.success_url =  reverse_lazy('MedCongressAdmin:Bloque_ponencias',kwargs={'path': block.path} )
        return self.success_url   
  

    def form_valid(self, form):
        try:
            ponencia=Ponencia.objects.get(pk=self.kwargs.get('pk'))
            self.object=ponencia
            pon=form['ponencia'].save(commit=False)
            relacion=form['ponencia_ponente'].save(commit=False)
            ubic=Ubicacion.objects.filter(direccion=form['ubicacion'].instance.direccion)

            if ubic.exists():
                pon.lugar=ubic.first()
            else:
                ubicacion=form['ubicacion'].save(commit=True)
                pon.lugar=ubicacion
            id_video=['']
            if pon.cod_video:
                id_video=pon.cod_video.split(sep='https://player.vimeo.com/video/')
                id_video=id_video[-1].split(sep='"')
            pon.id_video=id_video[0]
            ponencia=pon
            ponencia.save()
            relacion.ponencia=ponencia
            relacion.save()
            return super(PonencicaUpdateView, self).form_valid(form)
        except Exception as e:
            messages.warning(self.request, e)
            return super().form_invalid(form)
            
class PonenciaDeletedView(validarUser,DeleteView):
    model = Ponencia
    success_url = reverse_lazy('MedCongressAdmin:ponencias_list')

class PonenciaPonenteDeletedView(validarUser,DeleteView):
    model = RelPonenciaPonente
    success_url = reverse_lazy('MedCongressAdmin:ponencias_list')
   
def PonenciaBloqueDeleted(request):
    if request.is_ajax():
        query = request.POST['ponencia_id']
        ponencia=Ponencia.objects.get(id=query)
        ponencia.bloque=None
        ponencia.save()
        data = json.dumps([{'titulo':ponencia.titulo}])
        
        mimetype = "application/json"
    return HttpResponse(data, mimetype)  



class vTableAsJSONPonencia(TemplateView):
    template_name = 'MedCongressAdmin/asig_congress_form.html'
    def get(self, request, *args, **kwargs):
        #arreglo con las columnas de la BD a filtrar
        col_name_map = ['titulo','congreso__titulo','','published']
           
        #listado que muestra en dependencia de donde estes parado
       
        if request.GET.get('tipo')=='nada':
            object_list = Ponencia.objects.all()
        if request.GET.get('tipo')=='congreso':
            object_list = Ponencia.objects.filter(congreso__pk=int(request.GET.get('id')))
        if request.GET.get('tipo')=='bloque':
            object_list = Ponencia.objects.filter(bloque__pk=int(request.GET.get('id')))
        
        #parametros 
        search_text = request.GET.get('sSearch', '').lower()# texto a buscar
        start = int(request.GET.get('iDisplayStart', 0))#por donde empezar a mostrar
        delta = int(request.GET.get('iDisplayLength', 10))#cantidad a mostrar
        sort_dir = request.GET.get('sSortDir_0', 'asc')# direccion a ordenar
        sort_col = int(request.GET.get('iSortCol_0', 0)) # numero de la columna a ordenar
        sort_col_name = request.GET.get('mDataProp_%s' % sort_col, '1')
        sort_dir_prefix = (sort_dir == 'desc' and '-' or '') #sufijo para poner en la consulta para ordenar

        #para ordenar el listado
        if sort_col!=4 or sort_col!=2 :# columna en la tabla para las operaciones
            sort_colr = col_name_map[sort_col]
            object_list = object_list.order_by('%s%s' % (sort_dir_prefix,sort_colr))

        #para filtrar el listado
        filtered_object_list = object_list
        if len(search_text) > 0:
            filtered_object_list = object_list.filter(Q(titulo__icontains=search_text) | Q(congreso__titulo__icontains=search_text))

        #Guardar datos en un 
        enviar =[]
        for objet in filtered_object_list[start:(start+delta)]:
            public='No'
            if objet.published:
                public='Si'
            operaciones=''
            operaciones=''' <a href="'''+ reverse('MedCongressAdmin:ponencia_edit',kwargs={'pk':objet.pk})+'''"
                                                    title="Editar"><i class="icon icon-editar"></i></a>
                                                    <a id="del_'''+ str(objet.pk) +'''"
                                                        href="javascript:deleteItem('''+ str(objet.pk) +''')"
                                                        title="Eliminar">
                                                        <i class="icon icon-eliminar"></i>
                                                    </a>'''
            if request.GET.get('tipo')=='nada':
                operaciones=''' <a href="'''+ reverse('MedCongressAdmin:ponencia_edit',kwargs={'pk':objet.pk})+'''"
                                                    title="Editar"><i class="icon icon-editar"></i></a>
                                                    <a id="del_'''+ str(objet.pk) +'''"
                                                        href="javascript:deleteItem('''+ str(objet.pk) +''')"
                                                        title="Eliminar">
                                                        <i class="icon icon-eliminar"></i>
                                                    </a>'''
            if request.GET.get('tipo')=='congreso':
                operaciones=''' <a href="'''+ reverse('MedCongressAdmin:Edit_Congreso_ponencia',kwargs={'path':objet.congreso.path,'pk':objet.pk})+'''"
                                                    title="Editar"><i class="icon icon-editar"></i></a>
                                                    <a id="del_'''+ str(objet.pk) +'''"
                                                        href="javascript:deleteItem('''+ str(objet.pk) +''')"
                                                        title="Eliminar">
                                                        <i class="icon icon-eliminar"></i>
                                                    </a>'''
            # if request.GET.get('tipo')=='bloque':
            #     object_list = Ponencia.objects.filter(bloque__pk=int(request.GET.get('id')))
                

           #Guardar datos en un dic 

            enviar.append({ 'nombre':objet.titulo,
                            'congreso': objet.congreso.titulo,
                            'ponentes':''' <a  href="'''+ reverse('MedCongressAdmin:Ponencia_ponentes',kwargs={'path':objet.path})+'''"
                                                        title="Ponentes">
                                                        <i class="icon icon-ponente " style= "color: blue;" ></i>
                                                    </a>''',
                            'public' : public,
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
