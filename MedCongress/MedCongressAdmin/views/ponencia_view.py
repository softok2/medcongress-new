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

class PonenciaListView(validarUser,TemplateView):
    model = Ponencia
    context_object_name = 'ponencias'
    template_name = 'MedCongressAdmin/ponencias.html'
    def get(self, request, **kwargs):
        if self.request.GET.get('congreso'):
            congreso=Congreso.objects.filter(path=self.request.GET.get('congreso')).first()
            if congreso is None:
                return   HttpResponseRedirect(reverse('Error404'))
        if self.request.GET.get('bloque'):
            congreso=Bloque.objects.filter(path=self.request.GET.get('bloque')).first()
            if congreso is None:
                return   HttpResponseRedirect(reverse('Error404'))
        return self.render_to_response(self.get_context_data())
    def get_context_data(self, **kwargs):
        context=super(PonenciaListView,self).get_context_data(**kwargs)
        context['search']=self.request.GET.get('search')
        context['ponencias']=Ponencia.objects.all()
        if self.request.GET.get('congreso'):
            context['congreso']=Congreso.objects.filter(path=self.request.GET.get('congreso')).first()
            context['ponencias']=Ponencia.objects.filter(congreso= context['congreso'])
        if self.request.GET.get('bloque'):
            context['bloque']=Bloque.objects.filter(path=self.request.GET.get('bloque')).first()
            context['ponencias']=Ponencia.objects.filter(bloque= context['bloque'])
            if self.request.GET.get('congreso_bloque'):
                context['congreso_bloque']=context['bloque'].congreso
        return context
class  PonenciaCreateView(validarUser,FormView):
    form_class = PonenciaForms
    success_url = reverse_lazy('MedCongressAdmin:ponencias_list')
    template_name = 'MedCongressAdmin/ponencia_form.html'

    def get(self, request, **kwargs):
        if self.request.GET.get('congreso'):
            congreso=Congreso.objects.filter(path=self.request.GET.get('congreso')).first()
            if congreso is None:
                return   HttpResponseRedirect(reverse('Error404'))
        if self.request.GET.get('bloque'):
            congreso=Bloque.objects.filter(path=self.request.GET.get('bloque')).first()
            if congreso is None:
                return   HttpResponseRedirect(reverse('Error404'))
        return self.render_to_response(self.get_context_data())

    def form_valid(self, form):
        try: 
            if not self.request.POST.getlist('ponencia_ponente-ponente'):
                messages.warning(self.request, 'Debe al menos entrar un ponente')
                return super().form_invalid(form) 
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
            
            for ponente in self.request.POST.getlist('ponencia_ponente-ponente'):
                ponente_=Ponente.objects.get(pk=ponente)
                po= RelPonenciaPonente(ponente=ponente_,ponencia=ponencia)
                po.save()
            
            return super(PonenciaCreateView, self).form_valid(form)
        except Exception as e:
            messages.warning(self.request, e)
            return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        
        context = super(PonenciaCreateView, self).get_context_data(**kwargs)
        if self.request.GET.get('congreso'):
            context['con']=Congreso.objects.filter(path=self.request.GET.get('congreso')).first()
            context['blo']=Bloque.objects.filter(congreso=context['con'])
        if self.request.GET.get('bloque'):
            context['bloque']=Bloque.objects.filter(path=self.request.GET.get('bloque')).first()
            context['congreso']=context['bloque'].congreso
            context['blo']= None
        if self.request.GET.get('congreso_bloque'):
            context['congreso_bloque']=True
        return context 
    
    def get_success_url(self):
        url=reverse_lazy('MedCongressAdmin:ponencias_list')
        self.success_url='%s?&search=%s'%(url,self.request.GET.get('search'))
        if self.request.GET.get('congreso'):
            self.success_url =  '%s?congreso=%s&search=%s'%(url,self.request.GET.get('congreso'),self.request.GET.get('search')) 
        if self.request.GET.get('bloque'): 
            self.success_url =  '%s?bloque=%s&search=%s'%(url,self.request.GET.get('bloque'),self.request.GET.get('search')) 
            if self.request.GET.get('congreso_bloque'):
                self.success_url =  '%s?bloque=%s&search=%s&congreso_bloque=true'%(url,self.request.GET.get('bloque'),self.request.GET.get('search')) 

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
        if self.request.GET.get('congreso'):
            context['congreso']=Congreso.objects.filter(path=self.request.GET.get('congreso')).first()   
        if self.request.GET.get('bloque'):
            context['bloque']=Bloque.objects.filter(path=self.request.GET.get('bloque')).first()
            if self.request.GET.get('congreso_bloque'):
                context['congreso_bloque']=context['bloque'].congreso
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
        
        url =  reverse_lazy('MedCongressAdmin:Ponencia_ponentes',kwargs={'path': self.kwargs.get('path')} )
        self.success_url='%s?&search=%s'%(url,self.request.GET.get('search'))
        if self.request.GET.get('congreso'):
            self.success_url =  '%s?congreso=%s&search=%s'%(url,self.request.GET.get('congreso'),self.request.GET.get('search')) 
        if self.request.GET.get('bloque'): 
            self.success_url =  '%s?bloque=%s&search=%s'%(url,self.request.GET.get('bloque'),self.request.GET.get('search')) 
            if self.request.GET.get('congreso_bloque'):
                self.success_url =  '%s?bloque=%s&search=%s&congreso_bloque=true'%(url,self.request.GET.get('bloque'),self.request.GET.get('search')) 

        return self.success_url  
 
    def get_context_data(self, **kwargs):
        ctx = super(PonenciaPonenteCreateView, self).get_context_data(**kwargs)
        pon=Ponencia.objects.filter(path=self.kwargs.get('path')).first()
        ctx['pon'] = pon
        ponentes=RelPonenciaPonente.objects.filter(ponencia=pon)
        id=[]
        for ponente in ponentes:
            id.append(ponente.ponente.pk)
        ctx['ponentes']=Ponente.objects.exclude(id__in=id)
        if self.request.GET.get('congreso'):
            ctx['congreso']=Congreso.objects.filter(path=self.request.GET.get('congreso')).first()   
        if self.request.GET.get('bloque'):
            ctx['bloque']=Bloque.objects.filter(path=self.request.GET.get('bloque')).first()
            if self.request.GET.get('congreso_bloque'):
                ctx['congreso_bloque']=ctx['bloque'].congreso   
        return ctx

class PonencicaUpdateView(validarUser,FormView):
    form_class = PonenciaForms
    success_url = reverse_lazy('MedCongressAdmin:ponencias_list')
    template_name = 'MedCongressAdmin/ponencia_form.html'

    def get(self, request, **kwargs):
        if self.request.GET.get('congreso'):
            congreso=Congreso.objects.filter(path=self.request.GET.get('congreso')).first()
            if congreso is None:
                return   HttpResponseRedirect(reverse('Error404'))
        if self.request.GET.get('bloque'):
            congreso=Bloque.objects.filter(path=self.request.GET.get('bloque')).first()
            if congreso is None:
                return   HttpResponseRedirect(reverse('Error404'))
        return self.render_to_response(self.get_context_data())
    def get_queryset(self, **kwargs):
        ponencia=Ponencia.objects.get(pk=self.kwargs.get('pk'))
        self.object=ponencia
        return ponencia
    
    def get_form_kwargs(self):
        ponencia=Ponencia.objects.get(pk=self.kwargs.get('pk'))
        self.object=ponencia
        kwargs = super(PonencicaUpdateView, self).get_form_kwargs()
        kwargs.update(instance={
            'ponencia': self.object,
            'ubicacion': self.object.lugar,
            # 'ponencia_ponente':RelPonenciaPonente.objects.filter(ponencia=self.object)
        })
        return kwargs

    def get_context_data(self, **kwargs):
        ponencia=Ponencia.objects.get(pk=self.kwargs.get('pk'))
        self.object=ponencia
        context=super().get_context_data(**kwargs)
        if self.object.imagen:
            context['imagen_seg_url']='/static/%s'%(self.object.imagen)
        if self.object.meta_og_imagen:
            context['imagen_meta']='/static/%s'%(self.object.meta_og_imagen)
        context['bloque_update']=self.object.bloque
        context['update']='update'
        context['ponencia']=self.object
        context['is_info']=self.object.is_info
        ponentes=Ponente.objects.all()
        relaciones=RelPonenciaPonente.objects.filter(ponencia=self.object)
        ponentes_env=[]
        activo=False
        for ponente in ponentes:
            activo=False
            for relacion in relaciones:
                if relacion.ponente.pk==ponente.id:
                    activo=True
                
            ponentes_env.append({'id':ponente.id,
            'nombre':'%s %s <%s>'%(ponente.user.usuario.first_name,ponente.user.usuario.last_name,ponente.user.usuario.email),
            'activo':activo})
        context['ponentes_alls']=ponentes_env
        context['ponentes']=relaciones
       
        if self.request.GET.get('congreso'):
            context['con']=Congreso.objects.filter(path=self.request.GET.get('congreso')).first()
            context['blo']=Bloque.objects.filter(congreso=context['con'])
        if self.request.GET.get('bloque'):
            context['bloque']=Bloque.objects.filter(path=self.request.GET.get('bloque')).first()
            context['congreso']=context['bloque'].congreso
            context['blo']= None
        if self.request.GET.get('congreso_bloque'):
            context['congreso_bloque']=True
        return context 
      

    def get_success_url(self):
        url=reverse_lazy('MedCongressAdmin:ponencias_list')
        self.success_url='%s?&search=%s'%(url,self.request.GET.get('search'))
        if self.request.GET.get('congreso'):
            self.success_url =  '%s?congreso=%s&search=%s'%(url,self.request.GET.get('congreso'),self.request.GET.get('search')) 
        if self.request.GET.get('bloque'): 
            self.success_url =  '%s?bloque=%s&search=%s'%(url,self.request.GET.get('bloque'),self.request.GET.get('search')) 
            if self.request.GET.get('congreso_bloque'):
                self.success_url =  '%s?bloque=%s&search=%s&congreso_bloque=true'%(url,self.request.GET.get('bloque'),self.request.GET.get('search')) 

        return self.success_url       
  

    def form_valid(self, form):
        try:
            if not self.request.POST.getlist('ponencia_ponente-ponente'):
                messages.warning(self.request, 'Debe al menos entrar un ponente')
                return super().form_invalid(form) 
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
            relaciones=RelPonenciaPonente.objects.filter(ponencia=ponencia)
            relaciones.delete()
            for ponente in self.request.POST.getlist('ponencia_ponente-ponente'):
                ponente_=Ponente.objects.get(pk=ponente)
                po= RelPonenciaPonente(ponente=ponente_,ponencia=ponencia)
                po.save()
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
            object_list = Ponencia.objects.filter(congreso__path=request.GET.get('path'))
        if request.GET.get('tipo')=='bloque':
            object_list = Ponencia.objects.filter(bloque__path=request.GET.get('path'))
        
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
            operaciones=''' <a href="'''+ reverse('MedCongressAdmin:ponencia_edit',kwargs={'pk':objet.pk})+'''?search='''+request.GET.get('search')+'''"
                                                    title="Editar"><i class="icon icon-editar"></i></a>
                                                    <a id="del_'''+ str(objet.pk) +'''"
                                                        href="javascript:deleteItem('''+ str(objet.pk) +''')"
                                                        title="Eliminar">
                                                        <i class="icon icon-eliminar"></i>
                                                    </a>'''
            if request.GET.get('tipo')=='nada':
                operaciones=''' <a href="'''+ reverse('MedCongressAdmin:ponencia_edit',kwargs={'pk':objet.pk})+'''?search='''+request.GET.get('search')+'''"
                                                    title="Editar"><i class="icon icon-editar"></i></a>
                                                    <a id="del_'''+ str(objet.pk) +'''"
                                                        href="javascript:deleteItem('''+ str(objet.pk) +''')"
                                                        title="Eliminar">
                                                        <i class="icon icon-eliminar"></i>
                                                    </a>'''
            if request.GET.get('tipo')=='congreso':
                
                operaciones=''' <a href="'''+ reverse('MedCongressAdmin:ponencia_edit',kwargs={'pk':objet.pk})+'''?search='''+request.GET.get('search')+'''&congreso='''+request.GET.get('path')+'''"
                                                    title="Editar"><i class="icon icon-editar"></i></a>
                                                    <a id="del_'''+ str(objet.pk) +'''"
                                                        href="javascript:deleteItem('''+ str(objet.pk) +''')"
                                                        title="Eliminar">
                                                        <i class="icon icon-eliminar"></i>
                                                    </a>'''
            if request.GET.get('tipo')=='bloque':
                if request.GET.get('congreso_bloque'):
                    operaciones=''' <a href="'''+ reverse('MedCongressAdmin:ponencia_edit',kwargs={'pk':objet.pk})+'''?search='''+request.GET.get('search')+'''&bloque='''+request.GET.get('path')+'''&congreso_bloque=true"
                                                    title="Editar"><i class="icon icon-editar"></i></a>
                                                    <a id="del_'''+ str(objet.pk) +'''"
                                                        href="javascript:deleteItem('''+ str(objet.pk) +''')"
                                                        title="Eliminar">
                                                        <i class="icon icon-eliminar"></i>
                                                    </a>'''
                else:
                    operaciones=''' <a href="'''+ reverse('MedCongressAdmin:ponencia_edit',kwargs={'pk':objet.pk})+'''?search='''+request.GET.get('search')+'''&bloque='''+request.GET.get('path')+'''"
                                                    title="Editar"><i class="icon icon-editar"></i></a>
                                                    <a id="del_'''+ str(objet.pk) +'''"
                                                        href="javascript:deleteItem('''+ str(objet.pk) +''')"
                                                        title="Eliminar">
                                                        <i class="icon icon-eliminar"></i>
                                                    </a>'''
                
            ponentes=''
            ponentes=''' <a  href="'''+ reverse('MedCongressAdmin:Ponencia_ponentes',kwargs={'path':objet.path})+'''"
                                                        title="Ponentes">
                                                        <i class="icon icon-ponente " style= "color: blue;" ></i>
                                                    </a>'''
            if request.GET.get('tipo')=='nada':
                ponentes=''' <a  href="'''+ reverse('MedCongressAdmin:Ponencia_ponentes',kwargs={'path':objet.path})+'''"
                                                        title="Ponentes">
                                                        <i class="icon icon-ponente " style= "color: blue;" ></i>
                                                    </a>'''
            if request.GET.get('tipo')=='congreso':
                ponentes=''' <a  href="'''+ reverse('MedCongressAdmin:Ponencia_ponentes',kwargs={'path':objet.path})+'''?congreso='''+request.GET.get('path')+'''"
                                                        title="Ponentes">
                                                        <i class="icon icon-ponente " style= "color: blue;" ></i>
                                                    </a>'''
                
                
            if request.GET.get('tipo')=='bloque':
                if request.GET.get('congreso_bloque'):
                    ponentes=''' <a  href="'''+ reverse('MedCongressAdmin:Ponencia_ponentes',kwargs={'path':objet.path})+'''?bloque='''+request.GET.get('path')+'''&congreso_bloque=true"
                                                        title="Ponentes">
                                                        <i class="icon icon-ponente " style= "color: blue;" ></i>
                                                    </a>'''
                    
                else:
                    ponentes=''' <a  href="'''+ reverse('MedCongressAdmin:Ponencia_ponentes',kwargs={'path':objet.path})+'''?bloque='''+request.GET.get('path')+'''"
                                                        title="Ponentes">
                                                        <i class="icon icon-ponente " style= "color: blue;" ></i>
                                                    </a>'''
                    
                
           #Guardar datos en un dic 
            
            enviar.append({ 'nombre':objet.titulo,
                            'congreso': objet.congreso.titulo,
                            'ponentes':ponentes,
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
