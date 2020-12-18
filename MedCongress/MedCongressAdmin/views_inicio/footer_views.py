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
from MedCongressAdmin.forms.inicio_forms import FooterForm
from MedCongressApp.models import Footer


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
    

class FooterListView(validarUser,ListView):
    model = Footer
    context_object_name = 'footer'
    template_name = 'inicio/footer/index.html'

class FooterCreateView(validarUser,CreateView):
    model=Footer
    form_class = FooterForm
    success_url = reverse_lazy('MedCongressAdmin:footer_list')
    template_name = 'inicio/footer/form.html'

class FooterUpdateView(validarUser,UpdateView):
    form_class = FooterForm
    success_url = reverse_lazy('MedCongressAdmin:footer_list')
    template_name = 'inicio/footer/form.html'

    def get_queryset(self, **kwargs):
        return Footer.objects.filter(pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['update']=True
        return context

    
