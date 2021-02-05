
from django import forms
from django.core.files.images import get_image_dimensions
from  MedCongressApp.models import (Documento)


class RepositorioForm(forms.ModelForm):
   
    
    class Meta:
        model=Documento
        fields=['titulo','documento']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['titulo'].widget.attrs.update({'class': 'form-control'})  
    def clean(self, *args, **kwargs):
        cleaned_data = super(RepositorioForm, self).clean(*args, **kwargs)
        documento = cleaned_data.get('documento', None)
        if documento:
            filename = documento.name
            
            if( not filename.endswith(".zip") and not filename.endswith(".rar") and
                not filename.endswith(".doc") and not filename.endswith(".docx") and
                not filename.endswith(".pdf") and not filename.endswith(".jpg") and
                not filename.endswith(".png") and not filename.endswith(".txt")) :
                self.add_error('documento',"No está <b> permitido </b> subir ese <b>tipo de archivo</b>. Los permitidos son <b> .zip, .rar, .doc, .docx, .txt, .pdf, .jpg, .png</b>."  )

# class OfrecemosForm(forms.ModelForm):

#     class Meta:
#         model=Ofrecemos
#         fields=['titulo','icono','texto']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         self.fields['titulo'].widget.attrs.update({'class': 'form-control'})  
#         self.fields['icono'].widget.attrs.update({'class': 'form-control'})  
#         self.fields['texto'].widget.attrs.update({'class': 'form-control ckeditor'})  

#     def clean(self, *args, **kwargs):
#         cleaned_data = super(OfrecemosForm, self).clean(*args, **kwargs)
#         texto = cleaned_data.get('texto', None)
#         if not texto:
#             self.add_error('texto',"El campo <b>Texto </b> es Obligatorio"  )

# class ImagenQuienesSomosForms(forms.ModelForm):
#     imagen=forms.ImageField(required=False,label='Imagen')
#     q_somos=forms.ModelChoiceField(queryset=QuienesSomos.objects.all())
#     class Meta:
#         model=ImagenQuienesSomos
#         fields=['imagen','q_somos']       
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['imagen'].widget.attrs.update({ 'data-toggle':"tooltip",'data-popup':"tooltip-custom", 'data-original-title':"La Imagen debe ser de 440 X 440 pixel "})  
#     def clean(self, *args, **kwargs):
#         cleaned_data = super(ImagenQuienesSomosForms, self).clean(*args, **kwargs)
#         imagen = cleaned_data.get('imagen', None)
       
#         if imagen:
#             w, h = get_image_dimensions(imagen)
#             if w != 440 or h != 440:
#                 self.add_error('imagen',"Esta <b>Imagen</b> tiene %s X %s pixel. Debe ser de<b> 440 X 440 pixel</b>" %(w,h) )
#         else:
#             self.add_error('imagen',"Debe subir una Imagen" )


# class FooterForm(forms.ModelForm):
   
    
#     class Meta:
#         model=Footer
#         fields=['direccion','email','telefono','whatsapp']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         self.fields['direccion'].widget.attrs.update({'class': 'form-control'})  
#         self.fields['email'].widget.attrs.update({'class': 'form-control'})  
#         self.fields['telefono'].widget.attrs.update({'class': 'form-control'})  
#         self.fields['whatsapp'].widget.attrs.update({'class': 'form-control'})  

# class ImagenHomeForm(forms.ModelForm):
#     imagen=forms.ImageField(required=True,label='Imagen')
  
#     class Meta:
#         model=ImagenHome
#         fields=['imagen']       
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['imagen'].widget.attrs.update({ 'data-toggle':"tooltip",'data-popup':"tooltip-custom", 'data-original-title':"La Imagen debe ser de 1920 X 1080 pixel "})  


       
#     def clean(self, *args, **kwargs):
#         cleaned_data = super(ImagenHomeForm, self).clean(*args, **kwargs)
#         imagen = cleaned_data.get('imagen', None)
       
#         if imagen:
#             w, h = get_image_dimensions(imagen)
#             if w != 1920 or h != 1080:
#                 self.add_error('imagen',"Esta <b>Imagen</b> tiene %s X %s pixel. Debe ser de <b>1920 X 1080 pixel</b>" %(w,h) )
#         else:
#             self.add_error('imagen',"Debe subir una <b> Imagen</b>" )
