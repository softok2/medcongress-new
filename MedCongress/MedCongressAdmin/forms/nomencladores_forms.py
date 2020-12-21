
from django import forms

from  MedCongressApp.models import (Genero,CategoriaPagoCongreso,AvalCongreso,CategoriaUsuario,EspecialidadCongreso,
Especialidades, TipoCongreso,SocioCongreso)


class GeneroForm(forms.ModelForm):
   
    denominacion= forms.CharField(label='Denominación')
    class Meta:
        model=Genero
        fields=['denominacion',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['denominacion'].widget.attrs.update({'class': 'form-control'})  

    
      
       

class CatPagoForm(forms.ModelForm):
   
    class Meta:
        model=CategoriaPagoCongreso
        fields=['nombre','detalle']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})  
        self.fields['detalle'].widget.attrs.update({'class': 'form-control ckeditor'})  

class PatrocinadorForm(forms.ModelForm):

    logo=forms.ImageField(label='Buscar Logo',required=True)
    url=forms.URLField(label='URL del Patrocinador')
    class Meta:
        model=AvalCongreso
        fields=['nombre','detalle','url','logo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})  
        self.fields['detalle'].widget.attrs.update({'class': 'form-control ckeditor'})  
        self.fields['logo'].widget.attrs.update({'class': ' form-control '}) 
        self.fields['url'].widget.attrs.update({'class': ' form-control '})

class SocioForm(forms.ModelForm):

    logo=forms.ImageField(label='Buscar Logo',required=True)
    url=forms.URLField(label='URL del Patrocinador')
    class Meta:
        model=SocioCongreso
        fields=['nombre','detalle','url','logo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})  
        self.fields['detalle'].widget.attrs.update({'class': 'form-control ckeditor'})  
        self.fields['logo'].widget.attrs.update({'class': ' form-control '}) 
        self.fields['url'].widget.attrs.update({'class': ' form-control '})

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