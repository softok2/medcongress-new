from django import forms
from .models import Pais,PerfilUsuario
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
               label = 'Célula Profecional',
               )
    is_ponente=forms.BooleanField(
                label = 'Desearía ser ponente en un evento   ',
                required=False
               
               )
    pais = forms.ModelChoiceField(
    queryset=Pais.objects.all().order_by('denominacion')) 
    class Meta:
        model=PerfilUsuario
        fields=['pais','ciudad','estado','cel_profecional','categoria','genero','especialidad','is_ponente']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['pais'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['ciudad'].widget.attrs.update({'class': 'form-control'})   
        self.fields['estado'].widget.attrs.update({'class': 'form-control'})   
        self.fields['cel_profecional'].widget.attrs.update({'class': 'form-control'})   
        self.fields['categoria'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['genero'].widget.attrs.update({'class': 'form-control'}) 
       
       
        

    

class UserPerfilUser(MultiModelForm):
    form_classes = {
        'user': UserForm,
        'perfiluser': PerfilUserForm,
    }