
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

class ImagenQuienesSomosForms(forms.ModelForm):
    imagen=forms.ImageField(required=False)
    q_somos=forms.ModelChoiceField(queryset=QuienesSomos.objects.all())
    class Meta:
        model=ImagenQuienesSomos
        fields=['imagen','q_somos']       
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['imagen'].widget.attrs.update({'class': 'form-control'}) 
    def clean(self, *args, **kwargs):
        cleaned_data = super(ImagenQuienesSomosForms, self).clean(*args, **kwargs)
        imagen = cleaned_data.get('imagen', None)
       
        if imagen:
            w, h = get_image_dimensions(imagen)
            if w != 440 or h != 440:
                self.add_error('imagen',"Esta imagen tiene %s X %s pixel. Debe ser de 440 X 440 pixel" %(w,h) )
        else:
            self.add_error('imagen',"Debe subir una Imagen" )


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
    imagen=forms.ImageField(required=True)
  
    class Meta:
        model=ImagenHome
        fields=['imagen']       
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       
    def clean(self, *args, **kwargs):
        cleaned_data = super(ImagenHomeForm, self).clean(*args, **kwargs)
        imagen = cleaned_data.get('imagen', None)
       
        if imagen:
            w, h = get_image_dimensions(imagen)
            if w != 1920 or h != 1080:
                self.add_error('imagen',"Esta imagen tiene %s X %s pixel. Debe ser de 1920 X 1080 pixel" %(w,h) )
        else:
            self.add_error('imagen',"Debe subir una Imagen" )
