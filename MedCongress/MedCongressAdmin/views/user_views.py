from django import forms
import json
from django.contrib import messages
from django.http import HttpResponseBadRequest, HttpResponseRedirect,HttpResponse
from django.urls import reverse_lazy,reverse
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.views.generic import ListView,CreateView,TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin,AccessMixin
from django.views.generic.edit import  DeleteView, UpdateView,FormView
from MedCongressApp.models import User,PerfilUsuario,Ubicacion
from MedCongressAdmin.forms.congres_forms import UsuarioForms
from MedCongressAdmin.apps import validarUser


# from django.views import generic
  


class UsuariosListView(validarUser,ListView):
    model = PerfilUsuario
    context_object_name = 'users'
    template_name = 'MedCongressAdmin/usuarios.html'
  
   


class UsuarioCreateView(validarUser,FormView):
    model=User
    form_class = UsuarioForms
    success_url = reverse_lazy('MedCongressAdmin:usuarios_list')
    template_name = 'MedCongressAdmin/usuario_form.html'
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
        return super(UsuarioCreateView, self).form_valid(form)

class UsuarioUpdateView(validarUser,UpdateView):
    form_class = UsuarioForms
    success_url = reverse_lazy('MedCongressAdmin:usuarios_list')
    template_name = 'MedCongressAdmin/usuario_form.html'

    def get_queryset(self, **kwargs):
        return PerfilUsuario.objects.filter(pk=self.kwargs.get('pk'))
    
    def get_form_kwargs(self):
        kwargs = super(UsuarioUpdateView, self).get_form_kwargs()
        kwargs.update(instance={
            'perfiluser': self.object,
            'user': self.object.usuario,
            'ubicacion': self.object.ubicacion,
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        if self.object.meta_og_imagen:
            context['imagen_meta']='/static/%s'%(self.object.meta_og_imagen)
        if self.object.foto:    
            context['imagen_seg_url']='/static/%s'%(self.object.foto)
        return context

class UsuarioDeletedView(validarUser,DeleteView):
    model = User
    success_url = reverse_lazy('MedCongressAdmin:usuarios_list')

class UsuarioAsigCongresoView(TemplateView):
    template_name = 'MedCongressAdmin/asig_congress_form.html'

    def get_context_data(self, **kwargs):
        ctx = super(UsuarioAsigCongresoView, self).get_context_data(**kwargs)
        usuario=PerfilUsuario.objects.get(pk=self.kwargs.get('pk'))
        ctx['usuario'] = usuario
        return ctx

class vTableAsJSON(TemplateView):
    template_name = 'MedCongressAdmin/asig_congress_form.html'
    def get(self, request, *args, **kwargs):
        # col_name_map = {
        #     '0': '%s',
        #     '1': 'date',
        #     '2': 'customer__name',
        #     '3': 'store__name',
        # }
        object_list = PerfilUsuario.objects.all()
        search_text = request.GET.get('sSearch', '').lower()
        start = int(request.GET.get('iDisplayStart', 0))
        delta = int(request.GET.get('iDisplayLength', 10))
        sort_dir = request.GET.get('sSortDir_0', 'asc')
        sort_col = int(request.GET.get('iSortCol_0', 0))
        sort_col_name = request.GET.get('mDataProp_%s' % sort_col, '1')
        sort_dir_prefix = (sort_dir == 'desc' and '-' or '')

        # if sort_col_name in col_name_map:
        #     sort_col = col_name_map[sort_col_name]
        #     object_list = object_list.order_by('%s%s' % (sort_dir_prefix, sort_col))

        filtered_object_list = object_list
        if len(search_text) > 0:
            filtered_object_list = object_list.filter_on_search(search_text)

        enviar =[]
        for objet in filtered_object_list[start:(start+delta)]:
            enviar.append({ 'nombre':'%s %s'%(objet.usuario.first_name,objet.usuario.last_name),
                            'email': objet.usuario.email,
                            'categoria' : objet.categoria.nombre,
                            'especialidad' : 'especialidad',
                            'operaciones' : ''' <a href="'''+ reverse('MedCongressAdmin:usuario_edit',kwargs={'pk':objet.pk})+'''"
                                                    title="Editar"><i class="icon icon-editar"></i></a>
                                                    <a href="'''+ reverse('MedCongressAdmin:asig_congreso',kwargs={'pk':objet.pk})+'''"
                                                    title="Asignar Congreso"><i class="icon icon-asignar_congreso"></i></a>
                                                    <a id="del_'''+ str(objet.pk) +'''"
                                                        href="javascript:deleteItem('''+ str(objet.pk) +''')"
                                                        title="Eliminar">
                                                        <i class="icon icon-eliminar"></i>
                                                    </a>''',
                            
            })
        jsoner = {
            "iTotalRecords": object_list.count(),
            "iTotalDisplayRecords": object_list.count(),
            "sEcho": request.GET.get('sEcho', 1),
            "data": enviar
        }
        data = json.dumps(jsoner)
        mimetype = "application/json"

        return HttpResponse(data, mimetype)
        

