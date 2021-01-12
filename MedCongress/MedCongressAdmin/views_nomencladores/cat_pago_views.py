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
from MedCongressAdmin.forms.nomencladores_forms import CatPagoForm
from MedCongressApp.models import CategoriaPagoCongreso,RelCongresoCategoriaPago
from MedCongressAdmin.apps import validarUser
    

class CatPagoListView(validarUser,ListView):
    model = CategoriaPagoCongreso
    context_object_name = 'cat_pagos'
    template_name = 'nomencladores/cat_pago/index.html'

class CatPagoCreateView(validarUser,CreateView):
    model=CategoriaPagoCongreso
    form_class = CatPagoForm
    success_url = reverse_lazy('MedCongressAdmin:cat_pagos_list')
    template_name = 'nomencladores/cat_pago/form.html'
    
    def form_valid(self, form):

        cat_pago=form.save(commit=False)       
        path=cat_pago.nombre.replace("/","").replace(" ","-").replace("?","").replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("ñ","n")
        chars = '0123456789'
        secret_key = get_random_string(5, chars)
        cat_pago.path=path+secret_key  
        cat_pago.save()
        return super().form_valid(form)

class CatPagoDeletedView(validarUser,DeleteView):
    model = CategoriaPagoCongreso
    

    def delete(self,request, *args, **kwargs):
           
            cat_pago=CategoriaPagoCongreso.objects.get(pk=self.kwargs.get('pk'))
            if RelCongresoCategoriaPago.objects.filter(categoria= cat_pago).exists():
                return JsonResponse({'success':False}, safe=False)
            else:
                cat_pago.delete()
                return JsonResponse({'success':True}, safe=False)

class CatPagoUpdateView(validarUser,UpdateView):
    form_class = CatPagoForm
    success_url = reverse_lazy('MedCongressAdmin:cat_pagos_list')
    template_name = 'nomencladores/cat_pago/form.html'

    def get_queryset(self, **kwargs):
        return CategoriaPagoCongreso.objects.filter(pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['update']=True
        return context

    
