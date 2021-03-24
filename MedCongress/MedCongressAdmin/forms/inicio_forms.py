
from django import forms
from django.core.files.images import get_image_dimensions
from  MedCongressApp.models import (QuienesSomos,Ofrecemos,ImagenQuienesSomos,Footer,ImagenHome)


class QuienesSomosForm(forms.ModelForm):
   
    
    class Meta:
        model=QuienesSomos
        fields=['titulo','sub_titulo','texto']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['titulo'].widget.attrs.update({'class': 'form-control'})  
        self.fields['sub_titulo'].widget.attrs.update({'class': 'form-control'})  
        self.fields['texto'].widget.attrs.update({'class': 'form-control ckeditor'})  

class OfrecemosForm(forms.ModelForm):

    class Meta:
        model=Ofrecemos
        fields=['titulo','icono','texto']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['titulo'].widget.attrs.update({'class': 'form-control'})  
        self.fields['icono'].widget.attrs.update({'class': 'form-control'})  
        self.fields['texto'].widget.attrs.update({'class': 'form-control ckeditor'})  

    def clean(self, *args, **kwargs):
        cleaned_data = super(OfrecemosForm, self).clean(*args, **kwargs)
        texto = cleaned_data.get('texto', None)
        if not texto:
            self.add_error('texto',"El campo <b>Texto </b> es Obligatorio"  )

class ImagenQuienesSomosForms(forms.ModelForm):
    
    prueba=forms.CharField(required=False)
    q_somos=forms.ModelChoiceField(queryset=QuienesSomos.objects.all())
    class Meta:
        model=ImagenQuienesSomos
        fields=['q_somos','prueba']       
   
    def clean(self, *args, **kwargs):
        cleaned_data = super(ImagenQuienesSomosForms, self).clean(*args, **kwargs)
        imagenes = cleaned_data.get('prueba', None)
        if not imagenes :
            self.add_error('prueba', 'Debe entrar una <b>Imagen</b>')
       


class FooterForm(forms.ModelForm):
   
    
    class Meta:
        model=Footer
        fields=['direccion','email','telefono','whatsapp']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['direccion'].widget.attrs.update({'class': 'form-control'})  
        self.fields['email'].widget.attrs.update({'class': 'form-control'})  
        self.fields['telefono'].widget.attrs.update({'class': 'form-control'})  
        self.fields['whatsapp'].widget.attrs.update({'class': 'form-control'})  

class ImagenHomeForm(forms.ModelForm):
    prueba=forms.CharField(required=False)
  
    class Meta:
        model=ImagenHome
        fields=['prueba']       
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def clean(self, *args, **kwargs):
        cleaned_data = super(ImagenHomeForm, self).clean(*args, **kwargs)
        imagenes = cleaned_data.get('prueba', None)
        if not imagenes :
            self.add_error('prueba', 'Debe entrar una <b>Imagen</b>')   
