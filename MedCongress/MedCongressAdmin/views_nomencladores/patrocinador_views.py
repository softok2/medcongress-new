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
from MedCongressAdmin.forms.nomencladores_forms import PatrocinadorForm
from MedCongressApp.models import AvalCongreso,RelCongresoAval,Congreso


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
    

class PatrocinadorListView(validarUser,ListView):
    model = AvalCongreso
    context_object_name = 'patrocinadores'
    template_name = 'nomencladores/patrocinadores/index.html'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        if self.kwargs.get('pk'):
            congreso=Congreso.objects.get(pk=self.kwargs.get('pk'))
            context['congreso']=congreso
        return context
class PatrocinadorCreateView(validarUser,CreateView):
    model=AvalCongreso
    form_class = PatrocinadorForm
    success_url = reverse_lazy('MedCongressAdmin:patrocinadores_list')
    template_name = 'nomencladores/patrocinadores/form.html'
    
    def form_valid(self, form):
        if self.request.POST.get('congreso'):
            id_congreso=self.request.POST['congreso']
            congreso=Congreso.objects.get(pk=id_congreso)
            patrocinador=form.save(commit=True)
            relacion=RelCongresoAval(aval=patrocinador,congreso=congreso)
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
            self.success_url =  reverse_lazy('MedCongressAdmin:Congres_patrocinadores',kwargs={'path': congres.path} )
        return self.success_url

class PatrocinadorDeletedView(validarUser,DeleteView):
    model = AvalCongreso
    success_url = reverse_lazy('MedCongressAdmin:patrocinadores_list')

    def delete(self,request, *args, **kwargs):
            
        patrocinadores=AvalCongreso.objects.get(pk=self.kwargs.get('pk'))
       
        if RelCongresoAval.objects.filter(aval=patrocinadores).exists():
            return JsonResponse({'success':False}, safe=False)
        else:
            patrocinadores.delete()
            return JsonResponse({'success':True}, safe=False)

class PatrocinadorUpdateView(validarUser,UpdateView):
    form_class = PatrocinadorForm
    success_url = reverse_lazy('MedCongressAdmin:patrocinadores_list')
    template_name = 'nomencladores/patrocinadores/form.html'

    def get_queryset(self, **kwargs):
        return AvalCongreso.objects.filter(pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['update']=True
        context['logo']='/static/%s'%(self.object.logo)
        return context


