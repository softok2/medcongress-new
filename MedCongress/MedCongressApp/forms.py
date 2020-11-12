from django import forms
from .models import Pais,PerfilUsuario,Ubicacion,CategoriaUsuario,Genero
from django.contrib.auth.models import Group, User
from betterforms.multiform import MultiModelForm

        
class UserForm(forms.ModelForm):
    first_name=forms.CharField(
               label = 'Nombre',
               )
    last_name=forms.CharField(
                label = 'Apellidos',
                )
    username= forms.CharField(
               label = 'Usuario',
               )         
    password = forms.CharField(widget=forms.PasswordInput,label='Contraseña')
    password1 = forms.CharField(widget=forms.PasswordInput,label='Rectifique contraseña')
    class Meta:
        model=User
        fields=['username','password','password1','first_name','last_name','email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({'class': 'form-control'}) 
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

class PerfilUserForm(forms.ModelForm):
    cel_profecional=forms.CharField(
               label = 'Cédula Profesional',
                required=False
               )
    is_ponente=forms.BooleanField(
                label = 'Desearía ser ponente en un evento   ',
                required=False
               
               )
    genero=forms.ModelChoiceField(queryset=Genero.objects.all(), label='Género')
    categoria=forms.ModelChoiceField(queryset=CategoriaUsuario.objects.filter(published=True),label='Categoría')
   
    class Meta:
        model=PerfilUsuario
        fields=['cel_profecional','categoria','genero','especialidad','is_ponente']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
         
        self.fields['cel_profecional'].widget.attrs.update({'class': 'form-control'})   
        self.fields['categoria'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['genero'].widget.attrs.update({'class': 'form-control'}) 
       
       
        
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
        print(longitud)
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
        'ubicacion':Ubicacion,
        'categoria':Categoria
    }