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
from MedCongressAdmin.forms.congres_forms import MetaPagInicioForm,MetaPagListarForm
from MedCongressApp.models import MetaPagInicio,MetaPagListCongreso


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
    

class MetaInicioListView(validarUser,ListView):
    model = MetaPagInicio
    context_object_name = 'met_inicios'
    template_name = 'metadatos/pag_inicio/index.html'

class MetaInicioCreateView(validarUser,CreateView):
    model=MetaPagInicio
    form_class = MetaPagInicioForm
    success_url = reverse_lazy('MedCongressAdmin:meta_pag_inicio_list')
    template_name = 'metadatos/pag_inicio/form.html'

class MetaInicioUpdateView(validarUser,UpdateView):
    form_class = MetaPagInicioForm
    success_url = reverse_lazy('MedCongressAdmin:meta_pag_inicio_list')
    template_name = 'metadatos/pag_inicio/form.html'

    def get_queryset(self, **kwargs):
        return MetaPagInicio.objects.filter(pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['update']=True
        if self.object.meta_og_imagen:
            context['imagen']=self.object.meta_og_imagen
        return context

    
class MetaListarListView(validarUser,ListView):
    model = MetaPagListCongreso
    context_object_name = 'met_listar'
    template_name = 'metadatos/pag_list_congresos/index.html'

class MetaListarCreateView(validarUser,CreateView):
    model=MetaPagListCongreso
    form_class = MetaPagListarForm
    success_url = reverse_lazy('MedCongressAdmin:meta_pag_listar_list')
    template_name = 'metadatos/pag_list_congresos/form.html'

class MetaListarUpdateView(validarUser,UpdateView):
    form_class = MetaPagListarForm
    success_url = reverse_lazy('MedCongressAdmin:meta_pag_listar_list')
    template_name = 'metadatos/pag_list_congresos/form.html'

    def get_queryset(self, **kwargs):
        return MetaPagListCongreso.objects.filter(pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['update']=True
        if self.object.meta_og_imagen:
            context['imagen']=self.object.meta_og_imagen
        return context

    