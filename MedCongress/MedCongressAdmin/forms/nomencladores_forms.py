
from django import forms

from  MedCongressApp.models import (Genero,CategoriaPagoCongreso,AvalCongreso,CategoriaUsuario,EspecialidadCongreso,
Especialidades, TipoCongreso,SocioCongreso,Idioma)


class GeneroForm(forms.ModelForm):
   
    denominacion= forms.CharField(label='Denominación')
    class Meta:
        model=Genero
        fields=['denominacion',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['denominacion'].widget.attrs.update({'class': 'form-control'})  

class IdiomaForm(forms.ModelForm):
   
    nombre= forms.CharField(label='Idioma')
    abreviatura=forms.CharField(label='Abreviatura')
    class Meta:
        model=Idioma
        fields=['nombre','abreviatura']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['nombre'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['abreviatura'].widget.attrs.update({'class': 'form-control'})   

    
      
       

class CatPagoForm(forms.ModelForm):
   
    class Meta:
        model=CategoriaPagoCongreso
        fields=['nombre','detalle']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})  
        self.fields['detalle'].widget.attrs.update({'class': 'form-control ckeditor'})  

class PatrocinadorForm(forms.ModelForm):

    prueba=forms.CharField(required=False)
    url=forms.URLField(label='URL del Patrocinador')
    class Meta:
        model=AvalCongreso
        fields=['nombre','detalle','url','prueba']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})  
        self.fields['detalle'].widget.attrs.update({'class': 'form-control ckeditor'})  
        
        self.fields['url'].widget.attrs.update({'class': ' form-control '})

    def clean(self, *args, **kwargs):
        cleaned_data = super(PatrocinadorForm, self).clean(*args, **kwargs)
        
        logo = cleaned_data.get('prueba', None)
        if not logo :
                self.add_error('prueba', 'Debe entrar una <b>Logo </b> para este Patrocinador')
        # if AvalCongreso.objects.filter(nombre=nombre).exists():
        #    self.add_error('nombre',"Ya existe un <b>Patrocinador</b> con ese <b> Nombre</b>" )
       

class SocioForm(forms.ModelForm):

    prueba=forms.CharField(required=False)
    url=forms.URLField(label='URL del Socio')
    class Meta:
        model=SocioCongreso
        fields=['nombre','detalle','url','prueba']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})  
        self.fields['detalle'].widget.attrs.update({'class': 'form-control ckeditor'})  
        
        self.fields['url'].widget.attrs.update({'class': ' form-control '})
    def clean(self, *args, **kwargs):
        cleaned_data = super(SocioForm, self).clean(*args, **kwargs)
        logo = cleaned_data.get('prueba', None)
        if not logo :
            self.add_error('prueba', 'Debe entrar una <b>Logo </b> para este Socio')
       
class CatUsuarioForm(forms.ModelForm):
    published=forms.BooleanField(label='Publicado',required=False)
    class Meta:
        model=CategoriaUsuario
        fields=['nombre','detalle','published']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})  
        self.fields['published'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['detalle'].widget.attrs.update({'class': 'form-control ckeditor'})  

class EspEventoForm(forms.ModelForm):
   
    class Meta:
        model=EspecialidadCongreso
        fields=['nombre','detalle']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})  
        self.fields['detalle'].widget.attrs.update({'class': 'form-control ckeditor'})  

class EspUsuarioForm(forms.ModelForm):
   
    class Meta:
        model=Especialidades
        fields=['nombre','detalle']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})  
        self.fields['detalle'].widget.attrs.update({'class': 'form-control ckeditor'})  

class TipoEventoForm(forms.ModelForm):
   
    class Meta:
        model=TipoCongreso
        fields=['nombre','detalle']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})  
        self.fields['detalle'].widget.attrs.update({'class': 'form-control ckeditor'})  