from os import remove
from django import forms
from django.contrib import messages
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse_lazy,reverse
from django.views.generic import ListView,CreateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.edit import  DeleteView, UpdateView,FormView
from MedCongressApp.models import Documento
from MedCongressAdmin.forms.repositorio_form import RepositorioForm
from MedCongressAdmin.apps import validarUser
from django.http import JsonResponse


class DocumentosListView(validarUser,ListView):
    model = Documento
    context_object_name = 'documentos'
    template_name = 'MedCongressAdmin/repositorio_list.html'
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['documentos']=Documento.objects.all()
        context['host']=self.request.get_host()
        return context


class DocumentoCreateView(validarUser,CreateView):
    model=Documento
    form_class = RepositorioForm
    success_url = reverse_lazy('MedCongressAdmin:documentos_list')
    template_name = 'MedCongressAdmin/repositorio_form.html'

#     # def form_valid(self, form):

    #     user = form['user'].save(commit=False)
    #     perfiluser = form['perfiluser'].save(commit=False)
    #     ubic=Ubicacion.objects.filter(direccion=form['ubicacion'].instance.direccion)
        
    #     if ubic.exists():
    #         perfiluser.ubicacion=ubic.first()
    #     else:
    #         ubicacion=form['ubicacion'].save(commit=True)
    #         perfiluser.ubicacion=ubicacion
       
    #     us=User.objects.create_user(user.username,user.email,user.password)  
    #     us.first_name=user.first_name
    #     us.last_name=user.last_name
    #     us.is_active = True
    #     us.save()
    #     perfiluser.usuario = us
    #     perfiluser.path=us.username
    #     perfiluser.save() 
    #     return super(UsuarioCreateView, self).form_valid(form)

# class OtroUpdateView(validarUser,UpdateView):
#     form_class = OtrosForm
#     success_url = reverse_lazy('MedCongressAdmin:otros_list')
#     template_name = 'MedCongressAdmin/otros_form.html'

#     def get_queryset(self, **kwargs):
#         return DatosIniciales.objects.filter(pk=self.kwargs.get('pk'))
    
#     def get_form_kwargs(self):
#         kwargs = super(UsuarioUpdateView, self).get_form_kwargs()
#         kwargs.update(instance={
#             'perfiluser': self.object,
#             'user': self.object.usuario,
#             'ubicacion': self.object.ubicacion,
#         })
#         return kwargs

#     def get_context_data(self, **kwargs):
#         context=super().get_context_data(**kwargs)
#         context['imagen_seg_url']='/static/%s'%(self.object.foto)
#         return context

class DocumentoDeletedView(validarUser,DeleteView):
    model = Documento
    success_url = reverse_lazy('MedCongressAdmin:documentos_list')

    def delete(self,request, *args, **kwargs):

        try:    
            documento=Documento.objects.get(pk=self.kwargs.get('pk'))
            remove('MedCongressApp/static/%s'%(documento.documento))
            documento.delete()
            
            return JsonResponse({'success':True}, safe=False)
        except FileNotFoundError :
            return JsonResponse({'success':False,'mensaje':'No se pudo eliminar este Documento'}, safe=False)
        # if RelCongresoAval.objects.filter(aval=patrocinadores).exists():
        #     return JsonResponse({'success':False}, safe=False)
        # else:
        #     patrocinadores.delete()
        #     
