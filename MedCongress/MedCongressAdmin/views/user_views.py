from django import forms
from django.contrib import messages
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from MedCongressApp.models import User,PerfilUsuario
from MedCongressAdmin.forms.congres_forms import UsuarioForms

class validarUser(UserPassesTestMixin):
    permission_denied_message = 'No tiene permiso para acceder a la administracion'
    login_url='/admin/login/'
    def test_func(self):
       
        if self.request.user.is_staff :
            return True
        else:
            return False
    

class UsuariosListView(validarUser,ListView):
    model = PerfilUsuario
    context_object_name = 'users'
    template_name = 'MedCongressAdmin/usuarios.html'





class UsuarioCreateView(validarUser,CreateView):
    model=User
    form_class = UsuarioForms
    success_url = reverse_lazy('MedCongressAdmin:usuarios_list')
    template_name = 'MedCongressAdmin/usuario_form.html'
def form_valid(self, form):
        user = form['user'].save(commit=False)
        # email = EmailMessage('Asunto', 'esto es una prueba, como mando correos en Phyton?', to = ['dennis.molinetg@gmail.com'])
        # email.send()
        subject = 'HTML EMAIL'
        html_message = render_to_string('MedCongressApp/404.html', context={})
        plain_message = strip_tags(html_message)
        from_email = 'SOFTOK2 ME <amorell@softok2.com>'
        to = 'dennis.molinetg@gmail.com'
        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

        us=User.objects.create_user(user.username,user.email,user.password)
        ubicacion= form['ubicacion'].save(commit=True)
        perfiluser = form['perfiluser'].save(commit=False)
        categoria = form['categoria'].save(commit=False)
        if categoria.nombre !='':
            categoria.published=False
            categoria.save()
            perfiluser.categoria=categoria
        us.first_name=user.first_name
        us.last_name=user.last_name
        us.is_active = True
        group= Group.objects.get(name='Cliente')
        us.groups.add(group)
        us.save()
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        secret_key = get_random_string(20, chars)
        perfiluser.activation_key=secret_key
        perfiluser.usuario = us
        perfiluser.ubicacion=ubicacion
        perfiluser.path=us.username
        perfiluser.save()
        # datas={}
        # datas['activation_key']=secret_key
        # datas['email']=user.email
        # datas['username']=user.username
        # datas['email_path']="/ActivationEmail.txt"
        # datas['email_subject']="Activation de votre compte yourdomain"
        # #form.sendEmail(datas)
       
        return HttpResponseRedirect(reverse('Home'))



# class CountryUpdateView(validarUser,UpdateView):
#     form_class = CountryForm
#     success_url = reverse_lazy('MedCongressAdmin:country_list')
#     template_name = 'MedCongressAdmin/country_form.html'

#     def get_queryset(self, **kwargs):
#         return Pais.objects.filter(pk=self.kwargs.get('pk'))

#     def get_context_data(self, **kwargs):
#         context = super(CountryUpdateView, self).get_context_data(**kwargs)
#         context['form_title'] = 'Editar'
#         context['delete_url'] = reverse_lazy(
#             'MedCongressAdmin:country_delete', kwargs={'pk': self.object.pk})
#         return context

#     def form_invalid(self, form):
#         for error in form.errors:
#             form[error].field.widget.attrs['class'] += ' is-invalid'
#         return super(CountryUpdateView, self).form_invalid(form)


# class CountryDeleteView(validarUser,DeleteView):
#     model = Pais
#     success_url = reverse_lazy('MedCongressAdmin:country_list')
#     template_name = 'MedCongressAdmin/country_form.html'

#     def get_context_data(self, **kwargs):
#         context = super(CountryDeleteView, self).get_context_data(**kwargs)
#         context['form_title'] = 'Eliminar'
#         context['delete_value'] = self.object.denominacion
#         return context
