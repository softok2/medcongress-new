from django import forms
from .models import Pais,PerfilUsuario,Ubicacion,CategoriaUsuario,Genero
from django.contrib.auth.models import Group, User
from betterforms.multiform import MultiModelForm
from django.contrib.auth.forms import PasswordResetForm,SetPasswordForm
from django.utils.html import strip_tags
from django.core import mail

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
               label = 'Nombre',
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

       
        self.fields['password'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['password1'].widget.attrs.update({'class': 'form-control'}) 
          
        self.fields['first_name'].widget.attrs.update({'class': 'form-control','placeholder':'Nombre'})   
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})   
        self.fields['email'].widget.attrs.update({'class': 'form-control'})     

    def clean(self, *args, **kwargs):
        cleaned_data = super(UserForm, self).clean(*args, **kwargs)    
        password = cleaned_data.get('password', None)
        password1 = cleaned_data.get('password1', None)
        if password!=password1 :
            self.add_error('password1', 'No coinciden los password ')
        email = cleaned_data.get('email', None)
        username= cleaned_data.get('username',None)
        if User.objects.filter(email=email).exclude(username=username).count():
            self.add_error('email', 'Ese Email ya existe! ')                                                    
            
       
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
            self.add_error('email', 'Ese Email ya existe! ')                                                    
            
       
class PerfilUserForm(forms.ModelForm):
    cel_profecional=forms.CharField(
               label = 'Cédula Profesional',
                required=False
               )
   

    categoria=forms.ModelChoiceField(queryset=CategoriaUsuario.objects.filter(published=True),label='Categoría')
   
    class Meta:
        model=PerfilUsuario
        fields=['cel_profecional','categoria','especialidad']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
         
        self.fields['cel_profecional'].widget.attrs.update({'class': 'form-control'})   
        self.fields['categoria'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['especialidad'].widget.attrs.update({'class': 'form-control'}) 
        
       
        
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
        
        self.fields['nombre'].widget.attrs.update({'class': 'form-control'}) 
       



class UserPerfilUser(MultiModelForm):
    form_classes = {
        'user': UserForm,
        'perfiluser': PerfilUserForm,
        'categoria':Categoria
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

       
        self.fields['password'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['password1'].widget.attrs.update({'class': 'form-control'}) 
       

    def clean(self, *args, **kwargs):
        cleaned_data = super(CambiarPassForm, self).clean(*args, **kwargs)    
        password = cleaned_data.get('password', None)
        password1 = cleaned_data.get('password1', None)
        if password!=password1 :
            self.add_error('password1', 'No coinciden los password ')