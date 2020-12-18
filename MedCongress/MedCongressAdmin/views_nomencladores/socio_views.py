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
from MedCongressAdmin.forms.nomencladores_forms import SocioForm
from MedCongressApp.models import SocioCongreso,RelCongresoSocio,Congreso


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
    

class SocioListView(validarUser,ListView):
    model = SocioCongreso
    context_object_name = 'socios'
    template_name = 'nomencladores/socios/index.html'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        if self.kwargs.get('pk'):
            congreso=Congreso.objects.get(pk=self.kwargs.get('pk'))
            context['congreso']=congreso
        return context

class SocioCreateView(validarUser,CreateView):
    model=SocioCongreso
    form_class = SocioForm
    success_url = reverse_lazy('MedCongressAdmin:socios_list')
    template_name = 'nomencladores/socios/form.html'
    
    def form_valid(self, form):
        if self.request.POST.get('congreso'):
            id_congreso=self.request.POST['congreso']
            congreso=Congreso.objects.get(pk=id_congreso)
            socios=form.save(commit=True)
            relacion=RelCongresoSocio(socio=socios,congreso=congreso)
            relacion.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        if self.kwargs.get('pk'):
            congreso=Congreso.objects.get(pk=self.kwargs.get('pk'))
            context['congreso']=congreso
        return context

    def get_success_url(self, **kwargs):
        if self.kwargs.get('pk'):
            congres=Congreso.objects.get(pk=self.kwargs.get('pk'))
            self.success_url =  reverse_lazy('MedCongressAdmin:Congres_socios',kwargs={'path': congres.path} )
        return self.success_url

class SocioDeletedView(validarUser,DeleteView):
    model = SocioCongreso
    success_url = reverse_lazy('MedCongressAdmin:socios_list')

    def delete(self,request, *args, **kwargs):
            
        socios=SocioCongreso.objects.get(pk=self.kwargs.get('pk'))
       
        if RelCongresoSocio.objects.filter(socio=socios).exists():
            return JsonResponse({'success':False}, safe=False)
        else:
            socios.delete()
            return JsonResponse({'success':True}, safe=False)

class SocioUpdateView(validarUser,UpdateView):
    form_class = SocioForm
    success_url = reverse_lazy('MedCongressAdmin:socios_list')
    template_name = 'nomencladores/socios/form.html'

    def get_queryset(self, **kwargs):
        return SocioCongreso.objects.filter(pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['update']=True
        context['logo']='/static/%s'%(self.object.logo)
        return context


