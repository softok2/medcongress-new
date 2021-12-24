from django import forms
from .models import Pais,PerfilUsuario,Ubicacion,CategoriaUsuario,Genero,Session
from django.contrib.auth.models import Group, User
from betterforms.multiform import MultiModelForm
from django.contrib.auth.forms import PasswordResetForm,SetPasswordForm,AuthenticationForm
from django.utils.html import strip_tags
from django.core import mail
from django.contrib.auth import authenticate
import re

class EmailValidationOnForgotPassword(PasswordResetForm):

    def clean_email(self):
        email = self.cleaned_data['email']
        user=User.objects.filter(email__iexact=email)
        if not user.exists(): 
            self.add_error('email', 'No existe usuario con este Email')
        else:  
            if not user.first().is_active:
                subject = 'Bienvenido a MedCongress'
        # html_message = render_to_string('MedCongressApp/email.html', context={'token':secret_key})
                plain_message = strip_tags('Aviso..... Usted se ha creado un usuario en MedCongress entre a esta dirección https://medcongress.com.mx/habilitar_user/%s  para validar su cuenta en MedCongres'%(user.first().perfilusuario.activation_key))
                from_email = ''
                to = email
                mail.send_mail(subject, plain_message, from_email, [to])  
                self.add_error('email', 'Su usuario no esta activado se le ha enviado un correo para su activación')
        return email

class PasswordChangeOnForgotPassword(SetPasswordForm):

   def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                self.add_error('new_password2', 'No coinciden las contraseñas. Intente de Nuevo')
        return password2
        
class UserForm(forms.ModelForm):
    first_name=forms.CharField(
               label = 'Nombre'
               )
    last_name=forms.CharField(
                label = 'Apellidos',
                )
    
    password = forms.CharField(widget=forms.PasswordInput,label='Contraseña')
    password1 = forms.CharField(widget=forms.PasswordInput,label='Rectifique contraseña')
    class Meta:
        model=User
        fields=['password','password1','first_name','last_name','email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

       
        self.fields['password'].widget.attrs.update({'class': 'form-control','placeholder':'Contraseña'}) 
        self.fields['password1'].widget.attrs.update({'class': 'form-control','placeholder':'Confirmar Contraseña'}) 
          
        self.fields['first_name'].widget.attrs.update({'class': 'form-control','placeholder':'Nombre'})   
        self.fields['last_name'].widget.attrs.update({'class': 'form-control','placeholder':'Apellidos'})   
        self.fields['email'].widget.attrs.update({'class': 'form-control','placeholder':'Correo'}) 
        

    def clean(self, *args, **kwargs):
        cleaned_data = super(UserForm, self).clean(*args, **kwargs)    
        password = cleaned_data.get('password', None)
        password1 = cleaned_data.get('password1', None)
        if password!=password1 :
            self.add_error('password1', 'No coinciden las contraseñas ')
        email = cleaned_data.get('email', None)
        username= cleaned_data.get('username',None)
        if User.objects.filter(email=email).exclude(username=username).count():
            self.add_error('email', 'Ya existe un usuario con ese Correo ') 
        nombre = cleaned_data.get('first_name', None)
        apellido = cleaned_data.get('last_name', None)

        if not re.match(r"^[A-Za-zñÑáéíóúÁÉÍÓÚ. ]+$",nombre):
           self.add_error('first_name', 'El Campo <b> Nombre</b> solo admite letras ')
        if not re.match(r"^[A-Za-zñÑáéíóúÁÉÍÓÚ. ]+$",apellido):
           self.add_error('first_name', 'El Campo <b> Apellidos</b> solo admite letras ')  
       
class UserFormEdit(forms.ModelForm):
    first_name=forms.CharField(
               label = 'Nombre',
               )
    last_name=forms.CharField(
                label = 'Apellidos',
                )
    username= forms.CharField(
               label = 'Usuario',
               )         
    
    class Meta:
        model=User
        fields=['username','first_name','last_name','email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({'class': 'form-control'})   
        self.fields['first_name'].widget.attrs.update({'class': 'form-control','placeholder':'Nombre'})   
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})   
        self.fields['email'].widget.attrs.update({'class': 'form-control'})     

    def clean(self, *args, **kwargs):
        cleaned_data = super(UserFormEdit, self).clean(*args, **kwargs)
        email = cleaned_data.get('email', None)
        username= cleaned_data.get('username',None)
        if User.objects.filter(email=email).exclude(username=username).count():
            self.add_error('email', 'Ya existe un usuario con ese Correo ')  
        nombre = cleaned_data.get('first_name', None)
        apellido = cleaned_data.get('last_name', None)                                                      
        if not re.match(r"^[A-Za-zñÑáéíóúÁÉÍÓÚ. ]+$",nombre):
            self.add_error('first_name', 'El Campo <b> Nombre</b> solo admite letras ')
        if not re.match(r"^[A-Za-zñÑáéíóúÁÉÍÓÚ. ]+$",apellido):
            self.add_error('first_name', 'El Campo <b> Apellidos</b> solo admite letras ')  
       
class PerfilUserForm(forms.ModelForm):
    cel_profecional=forms.CharField(
               label = 'Cédula Profesional',
                required=False
               )
    class Meta:
        model=PerfilUsuario
        fields=['cel_profecional','categoria','especialidad','puesto']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
         
        self.fields['cel_profecional'].widget.attrs.update({'class': 'form-control ','placeholder':'Cédula Profesional'}) 
        self.fields['puesto'].widget.attrs.update({'class': 'form-control ','placeholder':'Hospital/Lugar de trabajo','rows':'2'})     
        self.fields['categoria'].widget.attrs.update({'class': 'form-select','placeholder':'Categoría'})
              
        self.fields['especialidad'].widget.attrs.update({'class': 'form-select ','placeholder':'Especialidad'}) 
        
       
        
class Ubicacion(forms.ModelForm):
    direccion=forms.CharField(
               label = 'Localidad',
               )
    longitud=forms.FloatField(required=False)
    latitud=forms.FloatField(required=False)
    class Meta:
        model=Ubicacion
        fields=['direccion','latitud','longitud']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['direccion'].widget.attrs.update({'class': 'form-control','placeholder':'Ciudad de residencia', 'data-bs-toggle':'tooltip', 'data-bs-placement':'top', 'title':'Escriba y seleccione su ciudad'}) 
        self.fields['longitud'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['latitud'].widget.attrs.update({'class': 'form-control'}) 
    def clean(self, *args, **kwargs):
        cleaned_data = super(Ubicacion, self).clean(*args, **kwargs)
        longitud = cleaned_data.get('longitud', None)
        latitud = cleaned_data.get('latitud', None)
        
        if longitud is None :
            self.add_error('direccion', 'Debe seleccionar una dirección')
    

class Categoria(forms.ModelForm):

    nombre= forms.CharField(
        label='Nueva Categoría',
        required=False
    )

    class Meta:
        model=CategoriaUsuario
        fields=['nombre']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['nombre'].widget.attrs.update({'class': 'form-control','placeholder':'Nueva Categoría'}) 
       



class UserPerfilUser(MultiModelForm):
    form_classes = {
        'user': UserForm,
        'perfiluser': PerfilUserForm,
        'categoria':Categoria,
        'ubicacion':Ubicacion,
    }

class UserPerfilUserEditar(MultiModelForm):
    form_classes = {
        'user': UserFormEdit,
        'perfiluser': PerfilUserForm,
        'ubicacion':Ubicacion,
        'categoria':Categoria
    }

class CambiarPassForm(forms.ModelForm):
         
    password = forms.CharField(widget=forms.PasswordInput,label='Contraseña')
    password1 = forms.CharField(widget=forms.PasswordInput,label='Rectifique contraseña')
    class Meta:
        model=User
        fields=['password','password1']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

       
        self.fields['password'].widget.attrs.update({'class': 'form-control  border-0','placeholder':'Nueva Contraseña'}) 
        self.fields['password1'].widget.attrs.update({'class': 'form-control border-0','placeholder':'Confirme la Nueva Contraseña'}) 
       

    def clean(self, *args, **kwargs):
        cleaned_data = super(CambiarPassForm, self).clean(*args, **kwargs)    
        password = cleaned_data.get('password', None)
        password1 = cleaned_data.get('password1', None)
        if password!=password1 :
            self.add_error('password1', 'No coinciden las contraseñas ')

class ExtAuthenticationForm(AuthenticationForm):
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        try:
            if username and password:
                usuario=User.objects.get(email=username)
                if usuario.check_password(password):
                    # if Session.objects.filter(usuario=usuario).exists():
                    #     self.add_error('username', 'Este <b>Usuario</b> ya esta autentificado en otro dispositivo')
                    #     return self.cleaned_data
                    self.user_cache = authenticate(username=username,
                                           password=password,request=self.request)
                    if self.user_cache is None:
                        self.add_error('username', 'Ese <b>Usuario</b> no Existe')
                        return self.cleaned_data

                    else:
                        self.confirm_login_allowed(self.user_cache)
                else:
                    self.add_error('username', 'Entró mal la <b>Contraseña </b>de este Usuario')
                    return self.cleaned_data  
            else:
                self.add_error('username', 'Estos campos son obligatorios')
                return self.cleaned_data 
        except User.DoesNotExist:
            self.add_error('username', 'Ese <b>Usuario</b> no Existe')
            return self.cleaned_data   
