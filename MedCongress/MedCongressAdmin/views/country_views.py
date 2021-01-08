from django import forms
from django.contrib import messages
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from MedCongressApp.models import Pais


class validarUser(UserPassesTestMixin):
    permission_denied_message = 'No tiene permiso para acceder a la administracion'
    login_url='accounts/login/'
    def test_func(self):
       
        if self.request.user.is_staff :
            return True
        else:
            return False
    

class CountryListView(validarUser,ListView):
    model = Pais
    context_object_name = 'countries'
    template_name = 'MedCongressAdmin/country.html'


class CountryForm(validarUser,forms.ModelForm):

    class Meta:
        model = Pais
        fields = ['denominacion','banderas']
        widgets = {'denominacion': forms.TextInput(
            attrs={'class': 'form-control'})}
        error_messages = {
            'denominacion':{
                'unique': 'Este nombre ya esta registrado.'
            },
        }


class CountryCreateView(validarUser,CreateView):
    form_class = CountryForm
    success_url = reverse_lazy('MedCongressAdmin:country_list')
    template_name = 'MedCongressAdmin/country_form.html'

    def get_context_data(self, **kwargs):
        context = super(CountryCreateView, self).get_context_data(**kwargs)
        context['form_title'] = 'Nuevo'
        return context

    def form_invalid(self, form):
        for error in form.errors:
            form[error].field.widget.attrs['class'] += ' is-invalid'
        return super(CountryCreateView, self).form_invalid(form)

    def form_valid(self, form):
        pais=form.save(commit=True)
        return super().form_valid(form)


class CountryUpdateView(validarUser,UpdateView):
    form_class = CountryForm
    success_url = reverse_lazy('MedCongressAdmin:country_list')
    template_name = 'MedCongressAdmin/country_form.html'

    def get_queryset(self, **kwargs):
        return Pais.objects.filter(pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super(CountryUpdateView, self).get_context_data(**kwargs)
        context['form_title'] = 'Editar'
        context['delete_url'] = reverse_lazy(
            'MedCongressAdmin:country_delete', kwargs={'pk': self.object.pk})
        return context

    def form_invalid(self, form):
        for error in form.errors:
            form[error].field.widget.attrs['class'] += ' is-invalid'
        return super(CountryUpdateView, self).form_invalid(form)


class CountryDeleteView(validarUser,DeleteView):
    model = Pais
    success_url = reverse_lazy('MedCongressAdmin:country_list')
    template_name = 'MedCongressAdmin/country_form.html'

    def get_context_data(self, **kwargs):
        context = super(CountryDeleteView, self).get_context_data(**kwargs)
        context['form_title'] = 'Eliminar'
        context['delete_value'] = self.object.denominacion
        return context
