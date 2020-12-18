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
from MedCongressAdmin.forms.inicio_forms import QuienesSomosForm,ImagenQuienesSomosForms
from MedCongressApp.models import QuienesSomos, ImagenQuienesSomos


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
    

class QuienesSomosListView(validarUser,ListView):
    model = QuienesSomos
    context_object_name = 'quienes_somoss'
    template_name = 'inicio/quienes_somos/index.html'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['imagenes']=ImagenQuienesSomos.objects.all()
        return context

class QuienesSomosCreateView(validarUser,CreateView):
    model=QuienesSomos
    form_class = QuienesSomosForm
    success_url = reverse_lazy('MedCongressAdmin:quienes_somos_list')
    template_name = 'inicio/quienes_somos/form.html'

class QuienesSomosUpdateView(validarUser,UpdateView):
    form_class = QuienesSomosForm
    success_url = reverse_lazy('MedCongressAdmin:quienes_somos_list')
    template_name = 'inicio/quienes_somos/form.html'

    def get_queryset(self, **kwargs):
        return QuienesSomos.objects.filter(pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['update']=True
        return context

    
class QuienesSomosImagenCreateView(validarUser,FormView):
    form_class = ImagenQuienesSomosForms
    success_url = reverse_lazy('MedCongressAdmin:quienes_somos_list')
    template_name = 'inicio/quienes_somos/form_imagen.html'

    def form_valid(self, form):
        imagen=form.save(commit=True)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super(QuienesSomosImagenCreateView, self).get_context_data(**kwargs)
        cong=QuienesSomos.objects.filter().first()
        ctx['cong'] = cong
        return ctx

class QuienesSomosImagenDeletedView(validarUser,DeleteView):
    model = ImagenQuienesSomos
    success_url = reverse_lazy('MedCongressAdmin:cat_usuarios_list')
