from django import forms
from django.contrib import messages
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse_lazy,reverse
from django.views.generic import ListView,CreateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.edit import  DeleteView, UpdateView,FormView
from MedCongressApp.models import User,PerfilUsuario,Ubicacion
from MedCongressAdmin.forms.congres_forms import UsuarioForms

class validarUser(UserPassesTestMixin):
    permission_denied_message = 'No tiene permiso para acceder a la administracion'
    login_url='/admin/login/'
    def test_func(self):
       
        if self.request.user.is_staff :
            return True
        else:
            return False
    

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
       
        us=User.objects.create_user(user.username,user.email,user.password)  
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
        context['imagen_seg_url']='/static/%s'%(self.object.foto)
        return context

class UsuarioDeletedView(validarUser,DeleteView):
    model = PerfilUsuario
    success_url = reverse_lazy('MedCongressAdmin:usuarios_list')


