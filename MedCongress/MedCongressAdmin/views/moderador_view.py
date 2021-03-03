from django import forms
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http import HttpResponseBadRequest, HttpResponseRedirect, JsonResponse,HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView,TemplateView,FormView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from MedCongressApp.models import Moderador,PerfilUsuario, RelBloqueModerador,User,Ubicacion
from MedCongressAdmin.forms.congres_forms import ModeradorForm,UsuarioForms
from MedCongressAdmin.apps import validarUser
from django.db.models import Q
import json   

class ModeradoresListView(validarUser,ListView):
    model = Moderador
    context_object_name = 'moderadores'
    template_name = 'MedCongressAdmin/moderadores.html'

    def get_context_data(self, **kwargs):
        context=super(ModeradoresListView,self).get_context_data(**kwargs)
        context['search']=self.request.GET.get('search')
        return context
class  ModeradorCreateView(validarUser,CreateView):
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
           
            enviar.append({ 'nombre':'%s %s'%(objet.user.usuario.first_name,objet.user.usuario.last_name),
                            'email': objet.user.usuario.email,
                            'operaciones' : ''' <a id="del_'''+ str(objet.pk) +'''"
                                                        href="javascript:deleteItem('''+ str(objet.pk) +''')"
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
