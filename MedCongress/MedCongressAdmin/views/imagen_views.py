from django import forms
from django.contrib import messages
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from MedCongressApp.models import ImagenCongreso
from MedCongressAdmin.forms.congres_forms import ImagenCongresoForms
from MedCongressAdmin.apps import validarUser
    


class ImagenCreateView(validarUser,CreateView):
    form_class = ImagenCongresoForms
    success_url = reverse_lazy('MedCongressAdmin:congress_list')
    template_name = 'MedCongressAdmin/congres_form.html'

    def post(self, request, **kwargs):
        if request.is_ajax:
            query =request.FILES
            print(query)
            imagen=ImagenCongreso(imagen=query)
            imagen.save()
            print(imagen.pk)