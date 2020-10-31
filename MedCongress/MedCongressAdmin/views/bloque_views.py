from django import forms
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views.defaults import page_not_found
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.crypto import get_random_string
from django.views.generic import CreateView, ListView, TemplateView
from django.views.generic.edit import DeleteView, FormView, UpdateView
from MedCongressAdmin.forms.congres_forms import BloqueForms,ModeradorBloqueForm
from MedCongressApp.models import Bloque, Congreso, Ponencia, Taller, RelBloqueModerador,Moderador


def page_not_found(request,exception):
    response = render_to_response(
        'MedCongressAdmin/404.html',
        context_instance=RequestContext(request)
        )
class validarUser(UserPassesTestMixin):
    permission_denied_message = 'No tiene permiso para acceder a la administracion'
    login_url='/admin/login/'
    def test_func(self):
       
        if self.request.user.is_staff :
            return True
        else:
            return False
    

class BloquesListView(validarUser,ListView):
    model = Bloque
    context_object_name = 'bloques'
    template_name = 'MedCongressAdmin/bloques.html'

class BloqueCreateView(validarUser,FormView):
    model=Bloque
    form_class = BloqueForms
    success_url = reverse_lazy('MedCongressAdmin:bloques_list')
    template_name = 'MedCongressAdmin/bloque_form.html'

    def get_context_data(self, **kwargs):
        
        context = super(BloqueCreateView, self).get_context_data(**kwargs)
        if self.kwargs.get('pk'):
            context['con']=Congreso.objects.get(pk=self.kwargs.get('pk'))
        return context 
    
    def get_success_url(self):
        if self.kwargs.get('pk'):
            congreso=Congreso.objects.get(pk=self.kwargs.get('pk'))
            self.success_url =  reverse_lazy('MedCongressAdmin:Congres_bloques',kwargs={'path': congreso.path} )
        return self.success_url 
    def form_valid(self, form):

        bloque = form.save(commit=False)
        path=bloque.titulo.replace("/","").replace(" ","-").replace("?","").replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("ñ","n")
        chars = '0123456789'
        secret_key = get_random_string(5, chars)
        bloque.path=path+secret_key  
        bloque.save()
        return super(BloqueCreateView, self).form_valid(form)

# class UsuarioUpdateView(validarUser,UpdateView):
#     form_class = UsuarioForms
#     success_url = reverse_lazy('MedCongressAdmin:usuarios_list')
#     template_name = 'MedCongressAdmin/usuario_form.html'

#     def get_queryset(self, **kwargs):
#         return PerfilUsuario.objects.filter(pk=self.kwargs.get('pk'))
    
#     def get_form_kwargs(self):
#         kwargs = super(UsuarioUpdateView, self).get_form_kwargs()
#         kwargs.update(instance={
#             'perfiluser': self.object,
#             'user': self.object.usuario,
#             'ubicacion': self.object.ubicacion,
#         })
#         return kwargs

#     def get_context_data(self, **kwargs):
#         context=super().get_context_data(**kwargs)
#         context['imagen_seg_url']='/static/%s'%(self.object.foto)
#         return context

class BloqueDeletedView(validarUser,DeleteView):
    model = Bloque
    success_url = reverse_lazy('MedCongressAdmin:bloques_list')

class BloquePonenciasListView(validarUser,TemplateView):
    template_name= 'MedCongressAdmin/bloque_ponencias.html'  

    def get(self, request, **kwargs):
        bloque=Bloque.objects.filter(path=self.kwargs.get('path'),published=True).first()
        if bloque is None:
            return   HttpResponseRedirect(reverse('Error404'))
        return self.render_to_response(self.get_context_data())    
    def get_context_data(self, **kwargs):
        context = super(BloquePonenciasListView, self).get_context_data(**kwargs)
        bloque=Bloque.objects.filter(path=self.kwargs.get('path'),published=True).first()
        context['bloque']=bloque
        context['ponencias']=Ponencia.objects.filter(bloque=bloque,published=True)
        return context

class BloqueTalleresListView(validarUser,TemplateView):
    template_name= 'MedCongressAdmin/bloque_talleres.html'  

    def get(self, request, **kwargs):
        bloque=Bloque.objects.filter(path=self.kwargs.get('path'),published=True).first()
        if bloque is None:
            return   HttpResponseRedirect(reverse('Error404'))
        return self.render_to_response(self.get_context_data())    
    def get_context_data(self, **kwargs):
        context = super(BloqueTalleresListView, self).get_context_data(**kwargs)
        bloque=Bloque.objects.filter(path=self.kwargs.get('path'),published=True).first()
        context['bloque']=bloque
        context['talleres']=Taller.objects.filter(bloque=bloque,published=True)
        return context

class BloqueUpdateView(validarUser,UpdateView):
    form_class = BloqueForms
    success_url = reverse_lazy('MedCongressAdmin:bloques_list')
    template_name = 'MedCongressAdmin/bloque_form.html'

    def get_queryset(self, **kwargs):
        return Bloque.objects.filter(pk=self.kwargs.get('pk'))

class BloqueModeradoresListView(TemplateView):
    template_name= 'MedCongressAdmin/bloque_moderadores.html' 
    def get(self, request, **kwargs):
        bloque=Bloque.objects.filter(path=self.kwargs.get('path'),published=True).first()
        if bloque is None:
            return   HttpResponseRedirect(reverse('Error404'))
        return self.render_to_response(self.get_context_data())   

    def get_context_data(self, **kwargs):
        context = super(BloqueModeradoresListView, self).get_context_data(**kwargs)
        bloque=Bloque.objects.filter(path=self.kwargs.get('path'),published=True).first()
        context['bloque']=bloque
        context['moderadores']=RelBloqueModerador.objects.filter(bloque=bloque)
        return context   

class  BloqueModeradoresCreateView(validarUser,CreateView):
    
    form_class = ModeradorBloqueForm
    # success_url = reverse_lazy('MedCongressAdmin:ponencias_list')
    template_name = 'MedCongressAdmin/bloque_moderador_form.html'

    def form_valid(self, form):
        ponencia=form.save(commit=False)
        ponencia.save()
        return super(BloqueModeradoresCreateView, self).form_valid(form)

    def get_success_url(self):
           self.success_url =  reverse_lazy('MedCongressAdmin:Moderadores_bloque',kwargs={'path': self.kwargs.get('path')} )
           return self.success_url
    def get_context_data(self, **kwargs):
        ctx = super(BloqueModeradoresCreateView, self).get_context_data(**kwargs)
        bloq=Bloque.objects.filter(path=self.kwargs.get('path'),published=True).first()
        moderadores=RelBloqueModerador.objects.filter(bloque=bloq)
        id=[]
        for ponente in moderadores:
            id.append(ponente.moderador.pk)
        ctx['moderadores']=Moderador.objects.exclude(id__in=id)
        ctx['bloq'] = bloq
        return ctx

class BloqueModeradoresDeletedView(validarUser,DeleteView):
    model = RelBloqueModerador
    success_url = reverse_lazy('MedCongressAdmin:Moderadores_list')

    


