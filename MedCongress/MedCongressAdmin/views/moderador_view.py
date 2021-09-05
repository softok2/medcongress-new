from django import forms
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http import HttpResponseBadRequest, HttpResponseRedirect, JsonResponse,HttpResponse
from django.urls import reverse_lazy,reverse
from django.views.generic import ListView,TemplateView,FormView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from MedCongressApp.models import Moderador,PerfilUsuario,Organizador, RelBloqueModerador,User,Ubicacion,Bloque,Congreso
from MedCongressAdmin.forms.congres_forms import ModeradorForm,UsuarioForms,ModeradorBloqueForm
from MedCongressAdmin.apps import validarUser,validarOrganizador
from django.db.models import Q
import json   

class ModeradoresListView(validarOrganizador,TemplateView):
    template_name = 'MedCongressAdmin/moderador/listar.html'

    def get_context_data(self, **kwargs):
        context=super(ModeradoresListView,self).get_context_data(**kwargs)
        if self.request.GET.get('bloque'):
            bloque=Bloque.objects.filter(path=self.request.GET.get('bloque')).first()
            if not bloque:
                return   HttpResponseRedirect(reverse('Error404'))
            context['bloque']=bloque
        if self.request.GET.get('congreso'):
            congreso=Congreso.objects.filter(path=self.request.GET.get('congreso')).first()
            context['congreso']=congreso
        context['search']=self.request.GET.get('search')
        return context
     
    def get(self, request, **kwargs):
        if self.request.GET.get('bloque') and self.request.GET.get('congreso'):
            print(self.request.GET.get('congreso'))
            bloque=Bloque.objects.filter(path=self.request.GET.get('bloque')).first()
            if bloque is None:
                return   HttpResponseRedirect(reverse('Error404'))
            if not Organizador.objects.filter(user=self.request.user.perfilusuario,congreso=bloque.congreso).exists() and not self.request.user.is_staff: 
                return   HttpResponseRedirect(reverse('Error403'))
            congreso=Congreso.objects.filter(path=self.request.GET.get('congreso')).first()
            if not congreso:
                return   HttpResponseRedirect(reverse('Error404'))
            if not Organizador.objects.filter(user=self.request.user.perfilusuario,congreso=congreso).exists() and not self.request.user.is_staff: 
                return   HttpResponseRedirect(reverse('Error403'))
        elif self.request.GET.get('bloque'):
            bloque=Bloque.objects.filter(path=self.request.GET.get('bloque')).first()
            if bloque is None:
                return   HttpResponseRedirect(reverse('Error404'))
            if not Organizador.objects.filter(user=self.request.user.perfilusuario,congreso=bloque.congreso).exists() and not self.request.user.is_staff: 
                return   HttpResponseRedirect(reverse('Error403'))
        elif self.request.GET.get('congreso'):
            congreso=Congreso.objects.filter(path=self.request.GET.get('congreso')).first()
            if not congreso:
                return   HttpResponseRedirect(reverse('Error404'))
        else:
            if not request.user.is_staff:
                return   HttpResponseRedirect(reverse('Error403'))
        return self.render_to_response(self.get_context_data()) 

class  ModeradorCreateView(validarOrganizador,CreateView):
    form_class = ModeradorForm
    success_url = reverse_lazy('MedCongressAdmin:Moderadores_list')
    template_name = 'MedCongressAdmin/moderador_form.html'
    def get_success_url(self):
        url= reverse_lazy('MedCongressAdmin:Moderadores_list')
        self.success_url='%s?search=%s'%(url,self.request.GET.get('search'))
        return self.success_url
    def form_valid(self, form):
       
        taller=form.save(commit=False)
        taller.save()
       
        return super(ModeradorCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        
        context = super(ModeradorCreateView, self).get_context_data(**kwargs)
        context['search']=self.request.GET.get('search')
        moderadores=Moderador.objects.all()
        id=[]
        for moderador in moderadores:
            id.append(moderador.user.pk)
        context['users']=PerfilUsuario.objects.exclude(id__in=id)
        return context
class ModeradorDeletedView(validarUser,DeleteView):
    model = Moderador
    success_url = reverse_lazy('MedCongressAdmin:Moderadores_list')

    def delete(self,request, *args, **kwargs):
           
            moderador=Moderador.objects.get(pk=self.kwargs.get('pk'))
            if RelBloqueModerador.objects.filter(moderador=moderador).exists():
                return JsonResponse({'success':False}, safe=False)
            else:
                moderador.delete()
                return JsonResponse({'success':True}, safe=False)

class vTableAsJSONModeradores(TemplateView):
    template_name = 'MedCongressAdmin/asig_congress_form.html'
    
    def get(self, request, *args, **kwargs):
        #arreglo con las columnas de la BD a filtrar
        col_name_map = ['user__usuario__first_name','user__usuario__email']
           
        # #listado que muestra en dependencia de donde estes parado
        if request.GET.get('path'):
            bloque=Bloque.objects.filter(path=request.GET.get('path')).first()
            object_list = bloque.moderador
        else:
            object_list = Moderador.objects.all()
        
        # #parametros 
        search_text = request.GET.get('sSearch', '').lower()# texto a buscar
        start = int(request.GET.get('iDisplayStart', 0))#por donde empezar a mostrar
        delta = int(request.GET.get('iDisplayLength', 10))#cantidad a mostrar
        sort_dir = request.GET.get('sSortDir_0', 'asc')# direccion a ordenar
        sort_col = int(request.GET.get('iSortCol_0', 0)) # numero de la columna a ordenar
        sort_col_name = request.GET.get('mDataProp_%s' % sort_col, '1')
        sort_dir_prefix = (sort_dir == 'desc' and '-' or '') #sufijo para poner en la consulta para ordenar

        # #para ordenar el listado
        
        sort_colr = col_name_map[sort_col]
        object_list = object_list.order_by('%s%s' % (sort_dir_prefix,sort_colr))

        # #para filtrar el listado
        filtered_object_list = object_list
        if len(search_text) > 0:
            filtered_object_list = object_list.filter(Q(user__usuario__last_name__icontains=search_text) | Q(user__usuario__email__icontains=search_text)|Q(user__usuario__first_name__icontains=search_text))

        # #Guardar datos en un 
        enviar =[]
       
        # if objet.ponente:
        #     user= '%s %s'%(objet.ponente.first().user.usuario.first_name,objet.ponente.first().user.usuario.last_name)
           
           #Guardar datos en un dic 
        for objet in filtered_object_list[start:(start+delta)]:
            operaciones =''' <a id="del_'''+ str(objet.pk) +'''"
                                                        href="javascript:deleteItem('''+ str(objet.pk) +''')"
                                                        title="Eliminar">
                                                        <i class="icon icon-eliminar"></i>
                                                    </a>'''
            if request.GET.get('path'):
                bloque_moderador=RelBloqueModerador.objects.filter(moderador=objet,bloque__path=request.GET.get('path')).first()
                operaciones =''' <a id="del_'''+ str(bloque_moderador.pk) +'''"
                                                        href="javascript:deleteItemVinculo('''+ str(bloque_moderador.pk) +''')"
                                                        title="Eliminar Vínculo entre Moderador y este Bloque">
                                                        <i class="icon icon-eliminar_vinculo "></i>
                                                    </a>   '''  
            enviar.append({ 'nombre':'%s %s'%(objet.user.usuario.first_name,objet.user.usuario.last_name),
                            'email': objet.user.usuario.email,
                            'operaciones' :operaciones ,
                            
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

class  BloqueModeradoresCreateView(validarOrganizador,FormView):
    
    form_class = ModeradorBloqueForm
    # success_url = reverse_lazy('MedCongressAdmin:ponencias_list')
    template_name = 'MedCongressAdmin/moderador/bloque_moderador_form.html'

    def form_valid(self, form):
        ponencia=form.save(commit=False)
        ponencia.save()
        return super(BloqueModeradoresCreateView, self).form_valid(form)

    def get_success_url(self):
        url =  reverse_lazy('MedCongressAdmin:Moderadores_list' )+'?search=%s&bloque=%s'%(self.request.GET.get('search'),self.kwargs.get('path'))
        get=''
        if self.request.GET.get('congreso'):
            get+='&congreso=%s'%(self.request.GET.get('congreso'))
        self.success_url =  url+get
        return self.success_url
    def get_context_data(self, **kwargs):
        ctx = super(BloqueModeradoresCreateView, self).get_context_data(**kwargs)
        bloq=Bloque.objects.filter(path=self.kwargs.get('path')).first()
        if self.request.GET.get('congreso'):
            ctx['congreso']=bloq.congreso
        if self.request.GET.get('search'):
            ctx['search']=self.request.GET.get('search')
        moderadores=RelBloqueModerador.objects.filter(bloque=bloq)
        id=[]

        for ponente in moderadores:
            id.append(ponente.moderador.pk)
        ctx['moderadores']=Moderador.objects.exclude(id__in=id)
        ctx['bloq'] = bloq
        return ctx
    def get(self, request, **kwargs):
        bloque=Bloque.objects.filter(path=self.kwargs.get('path')).first()
        if bloque is None:
            return   HttpResponseRedirect(reverse('Error404'))
        return self.render_to_response(self.get_context_data()) 

class UserModeradorCreateView(validarUser,FormView):
    model=User
    form_class = UsuarioForms
    success_url = reverse_lazy('MedCongressAdmin:Moderadores_list')
    template_name = 'MedCongressAdmin/usuario_form.html'

    def get_context_data(self, **kwargs):
        context = super(UserModeradorCreateView, self).get_context_data(**kwargs)
        context['search']=self.request.GET.get('search')
        context['moderador']=True
        return context
    def get_success_url(self):
        url= reverse_lazy('MedCongressAdmin:Moderadores_list')
        self.success_url='%s?search=%s'%(url,self.request.GET.get('search'))
        return self.success_url
    def form_valid(self, form):

        user = form['user'].save(commit=False)
        perfiluser = form['perfiluser'].save(commit=False)
        ubic=Ubicacion.objects.filter(direccion=form['ubicacion'].instance.direccion)
        
        if ubic.exists():
            perfiluser.ubicacion=ubic.first()
        else:
            ubicacion=form['ubicacion'].save(commit=True)
            perfiluser.ubicacion=ubicacion
       
        us=User.objects.create_user(user.email,user.email,user.password)  
        us.first_name=user.first_name
        us.last_name=user.last_name
        us.is_active = True
        us.save()
        perfiluser.usuario = us
        perfiluser.path=us.username
        perfiluser.save()
        ponente=Moderador(user=perfiluser) 
        ponente.save()
        return super(UserModeradorCreateView, self).form_valid(form)
