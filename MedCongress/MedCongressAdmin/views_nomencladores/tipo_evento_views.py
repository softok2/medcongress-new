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
from MedCongressAdmin.forms.nomencladores_forms import TipoEventoForm
from MedCongressApp.models import TipoCongreso,Congreso


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
    

class TipoEventoListView(validarUser,ListView):
    model = TipoCongreso
    context_object_name = 'tipo_eventos'
    template_name = 'nomencladores/tipo_eventos/index.html'

class TipoEventoCreateView(validarUser,CreateView):
    model=TipoCongreso
    form_class = TipoEventoForm
    success_url = reverse_lazy('MedCongressAdmin:tipo_eventos_list')
    template_name = 'nomencladores/tipo_eventos/form.html'


class TipoEventoDeletedView(validarUser,DeleteView):
    model = TipoCongreso
    success_url = reverse_lazy('MedCongressAdmin:tipo_eventos_list')
    def delete(self,request, *args, **kwargs):
           
            tipo_evento=TipoCongreso.objects.get(pk=self.kwargs.get('pk'))
            if Congreso.objects.filter(t_congreso= tipo_evento).exists():
                return JsonResponse({'success':False}, safe=False)
            else:
                tipo_evento.delete()
                return JsonResponse({'success':True}, safe=False)

class TipoEventoUpdateView(validarUser,UpdateView):
    form_class = TipoEventoForm
    success_url = reverse_lazy('MedCongressAdmin:tipo_eventos_list')
    template_name = 'nomencladores/tipo_eventos/form.html'

    def get_queryset(self, **kwargs):
        return TipoCongreso.objects.filter(pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['update']=True
        return context


