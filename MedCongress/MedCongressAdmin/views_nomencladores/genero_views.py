from django import forms
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views.defaults import page_not_found
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
from django.utils.crypto import get_random_string
from django.views.generic import CreateView, ListView, TemplateView
from django.views.generic.edit import DeleteView, FormView, UpdateView
from MedCongressAdmin.forms.nomencladores_forms import GeneroForm
from MedCongressApp.models import Genero,PerfilUsuario


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
    

class GeneroListView(validarUser,ListView):
    model = Genero
    context_object_name = 'generos'
    template_name = 'nomencladores/genero/index.html'

class GeneroCreateView(validarUser,CreateView):
    model=Genero
    form_class = GeneroForm
    success_url = reverse_lazy('MedCongressAdmin:generos_list')
    template_name = 'nomencladores/genero/form.html'
    

class GeneroDeletedView(validarUser,DeleteView):
    model = Genero
    success_url = reverse_lazy('MedCongressAdmin:generos_list')

    def delete(self,request, *args, **kwargs):
            
        genero=Genero.objects.get(pk=self.kwargs.get('pk'))
       
        if PerfilUsuario.objects.filter(genero=genero).exists():
            return JsonResponse({'success':False}, safe=False)
        else:
            genero.delete()
            return JsonResponse({'success':True}, safe=False)

class GeneroUpdateView(validarUser,UpdateView):
    form_class = GeneroForm
    success_url = reverse_lazy('MedCongressAdmin:generos_list')
    template_name = 'nomencladores/genero/form.html'

    def get_queryset(self, **kwargs):
        return Genero.objects.filter(pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['update']=True
        return context

