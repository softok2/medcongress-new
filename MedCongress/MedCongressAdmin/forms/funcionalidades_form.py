from django import forms
from django.core.files.images import get_image_dimensions
from  MedCongressApp.models import (QuienesSomos,Ofrecemos,ImagenQuienesSomos,Footer,ImagenHome,Congreso,Organizador)


class EnviarCorreosForms(forms.Form):
   
    asunto=forms.CharField(label='Asunto',error_messages={'required':'Debe entrar el <b>Asunto</b> del Correo'})
    adjunto=forms.FileField(label='Adjunto',required=False)
    mensaje=forms.CharField(widget=forms.Textarea,label='Mensaje',error_messages={'required':'Debe entrar el <b> Mensaje </b> del Correo'})
    congreso=forms.ModelChoiceField(queryset=Congreso.objects.all(),label='Congreso',error_messages={'required':'Debe seleccionar un <b>Congreso</b>'})
    class Meta:
        
        fields=['asunto','adjunto','mensaje','congreso']

    def __init__(self,user, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not user.is_staff:
            self.fields['congreso'].choices=[(None, "-----------")]+[(c.congreso.pk, c.congreso.titulo) for c in Organizador.objects.filter(user=user.perfilusuario)]
        self.fields['asunto'].widget.attrs.update({'class': 'form-control'})  
        self.fields['adjunto'].widget.attrs.update({'class': 'form-control'})  
        self.fields['mensaje'].widget.attrs.update({'class': 'form-control ckeditor'}) 
        self.fields['congreso'].widget.attrs.update({'class': 'form-control select2'})

    # def clean(self, *args, **kwargs):
    #     cleaned_data = super(EnviarCorreosForms, self).clean(*args, **kwargs)
    #     congreso = cleaned_data.get('congreso', None)
    #     if not congreso:
    #         self.add_error('congreso',"Debe seleccionar un <b> Congreso </b>"  )