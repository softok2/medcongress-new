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
from MedCongressAdmin.forms.congres_forms import CuestionarioForms,PreguntaForm
from MedCongressApp.models import CuestionarioPregunta,CuestionarioRespuestas


class validarUser(UserPassesTestMixin):
    permission_denied_message = 'No tiene permiso para acceder a la administracion'
    login_url='/admin/login/'
    def test_func(self):
       
        if self.request.user.is_staff :
            return True
        else:
            return False
    

class CuestionarioListView(validarUser,ListView):
    model = CuestionarioPregunta
    context_object_name = 'cuestionarios'
    template_name = 'MedCongressAdmin/cuestionarios.html'

class PreguntaCreateView(validarUser,FormView):
    form_class = PreguntaForm
    success_url = reverse_lazy('MedCongressAdmin:ponencias_list')
    template_name = 'MedCongressAdmin/cuestionario_form.html'

    def form_valid(self, form):
        
        print('ewrretryt121212121212121212121212121212121212')
        print(form)
    
    def form_invalid(self, form):
        print('e3534t3g4545hrjh5j67k6k6')
        for error in form.errors:
            print(form[error])
        return super(PreguntaCreateView, self).form_invalid(form)
        # ubic=Ubicacion.objects.filter(direccion=form['ubicacion'].instance.direccion)

        # if ubic.exists():
        #     ponencia.lugar=ubic.first()
        # else:
        #     ubicacion=form['ubicacion'].save(commit=True)
        #     ponencia.lugar=ubicacion
        # path=ponencia.titulo.replace("/","").replace(" ","-").replace("?","").replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("ñ","n")
        # chars = '0123456789'
        # secret_key = get_random_string(5, chars)
        # ponencia.path=path+secret_key
        # ponencia.save()
        return super(PonenciaCreateView, self).form_valid(form)

    # def get_context_data(self, **kwargs):
        
    #     context = super(PonenciaCreateView, self).get_context_data(**kwargs)
    #     if self.kwargs.get('pk'):
    #         context['con']=Congreso.objects.get(pk=self.kwargs.get('pk'))
    #         context['blo']=Bloque.objects.filter(congreso=context['con'])
    #     if self.kwargs.get('pk_block'):
    #         context['bloque']=Bloque.objects.get(pk=self.kwargs.get('pk_block'))
    #         context['con']=context['bloque'].congreso
    #         context['blo']= None
    #     return context 