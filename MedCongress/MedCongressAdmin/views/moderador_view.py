from django import forms
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http import HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from MedCongressApp.models import Moderador,PerfilUsuario, RelBloqueModerador
from MedCongressAdmin.forms.congres_forms import ModeradorForm

class validarUser(UserPassesTestMixin):
    permission_denied_message = 'No tiene permiso para acceder a la administracion'
    login_url='accounts/login/'
    def test_func(self):
       
        if self.request.user.is_staff :
            return True
        else:
            return False
    

class ModeradoresListView(validarUser,ListView):
    model = Moderador
    context_object_name = 'moderadores'
    template_name = 'MedCongressAdmin/moderadores.html'

class  ModeradorCreateView(validarUser,CreateView):
    form_class = ModeradorForm
    success_url = reverse_lazy('MedCongressAdmin:Moderadores_list')
    template_name = 'MedCongressAdmin/moderador_form.html'

    def form_valid(self, form):
       
        taller=form.save(commit=False)
        taller.save()
       
        return super(ModeradorCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        
        context = super(ModeradorCreateView, self).get_context_data(**kwargs)
        moderadores=Moderador.objects.all()
        id=[]
        for moderador in moderadores:
            id.append(moderador.user.pk)
        context['users']=PerfilUsuario.objects.exclude(id__in=id)
        return context
class ModeradorDeletedView(validarUser,DeleteView):
    model = Moderador
    success_url = reverse_lazy('MedCongressAdmin:Moderadores_list')

    def delete(self,request, *args, **kwargs):
           
            moderador=Moderador.objects.get(pk=self.kwargs.get('pk'))
            if RelBloqueModerador.objects.filter(moderador=moderador).exists():
                return JsonResponse({'success':False}, safe=False)
            else:
                moderador.delete()
                return JsonResponse({'success':True}, safe=False)

