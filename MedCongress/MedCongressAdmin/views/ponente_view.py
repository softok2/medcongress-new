from django import forms
from django.contrib import messages
from django.http import HttpResponseBadRequest, HttpResponseRedirect,JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView,FormView
from MedCongressApp.models import Ponente,PerfilUsuario,RelPonenciaPonente,User,Ubicacion
from MedCongressAdmin.forms.congres_forms import PonenteForm,UsuarioForms
from MedCongressAdmin.apps import validarUser


class PonentesListView(validarUser,ListView):
    model = Ponente
    context_object_name = 'ponentes'
    template_name = 'MedCongressAdmin/ponentes.html'

class  PonentesCreateView(validarUser,CreateView):
    form_class = PonenteForm
    success_url = reverse_lazy('MedCongressAdmin:Ponentes_list')
    template_name = 'MedCongressAdmin/ponente_form.html'

    def form_valid(self, form):
        
        taller=form.save(commit=False)
        taller.save()

        return super(PonentesCreateView, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        
        context = super(PonentesCreateView, self).get_context_data(**kwargs)
        ponentes=Ponente.objects.all()
        id=[]
        for ponente in ponentes:
            id.append(ponente.user.pk)
        context['users']=PerfilUsuario.objects.exclude(id__in=id)
        return context

class PonenteDeletedView(validarUser,DeleteView):
    model = Ponente
    success_url = reverse_lazy('MedCongressAdmin:talleres_list')
    def delete(self,request, *args, **kwargs):
           
            ponente=Ponente.objects.get(pk=self.kwargs.get('pk'))
            if RelPonenciaPonente.objects.filter(ponente=ponente).exists():
                return JsonResponse({'success':False}, safe=False)
            else:
                ponente.delete()
                return JsonResponse({'success':True}, safe=False)


class UserPonenteCreateView(validarUser,FormView):
    model=User
    form_class = UsuarioForms
    success_url = reverse_lazy('MedCongressAdmin:Ponentes_list')
    template_name = 'MedCongressAdmin/usuario_form.html'

    def get_context_data(self, **kwargs):
        context = super(UserPonenteCreateView, self).get_context_data(**kwargs)
        context['ponente']=True
        return context

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
        ponente=Ponente(user=perfiluser) 
        ponente.save()
        return super(UserPonenteCreateView, self).form_valid(form)
