from django import forms
from datetime import date
from django.core.files.images import get_image_dimensions
from  MedCongressApp.models import (Congreso,Ubicacion,ImagenCongreso,TipoCongreso,Ponencia,Taller,
                                    Ponente,PerfilUsuario,RelPonenciaPonente,RelCongresoCategoriaPago,
                                    CategoriaPagoCongreso,RelTalleresCategoriaPago,Genero,CategoriaUsuario,
                                    RelTallerPonente,Bloque,DatosIniciales,RelCongresoUser,RelTallerUser,
                                    Moderador,RelBloqueModerador,ImagenCongreso)
                    
from django.contrib.auth.models import Group, User
from betterforms.multiform import MultiModelForm

        
class CongresForm(forms.ModelForm):
    imagen_seg=forms.ImageField(label='Buscar Imagen',required=False)
    is_openpay=forms.BooleanField(label='Pagar por OpenPay',required=False)
    titulo=forms.CharField(label='Título',initial=True)
    template=forms.CharField(label='Template del Congreso',required=False)
    published=forms.BooleanField(label='Publicado',required=False)
    sub_titulo=forms.CharField(label='Título segundario',required=False) 
    t_congreso=forms.ModelChoiceField(queryset=TipoCongreso.objects.all(),label='Tipo de Congreso')
    fecha_inicio=forms.DateTimeField(widget=forms.TextInput())
    class Meta:
        model=Congreso
        fields=['titulo','sub_titulo','imagen_seg','fecha_inicio','published','t_congreso','especialidad','is_openpay','template']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

        self.fields['titulo'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['sub_titulo'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['imagen_seg'].widget.attrs.update({'class': ' form-control '}) 
        self.fields['fecha_inicio'].widget.attrs.update({'class': 'form-control'})   
        self.fields['published'].widget.attrs.update({'class': 'form-control'})   
        self.fields['t_congreso'].widget.attrs.update({'class': 'form-control'})  
        self.fields['especialidad'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['is_openpay'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['template'].widget.attrs.update({'class': 'form-control',})                      

    def clean(self, *args, **kwargs):
        cleaned_data = super(CongresForm, self).clean(*args, **kwargs)
        imagen = cleaned_data.get('imagen_seg', None)
        w, h = get_image_dimensions(imagen)
        if w != 1140 or h != 240:
            self.add_error('imagen_seg',"Esta imagen tiene %s X %s pixel. Debe ser de 1140 X 240 pixel" %(w,h) )
   

    # def clean(self, *args, **kwargs):
    #     cleaned_data = super(UserForm, self).clean(*args, **kwargs)
    #     password = cleaned_data.get('password', None)
    #     password1 = cleaned_data.get('password1', None)
    #     if password!=password1 :
    #         self.add_error('password1', 'No coinciden los password ')

class ImagenCongresoForms(forms.ModelForm):
    imagen=forms.ImageField(required=False)
    class Meta:
        model=ImagenCongreso
        fields=['imagen']       
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['imagen'].widget.attrs.update({'class': 'form-control'}) 

class UbicacionForm(forms.ModelForm):
    direccion=forms.CharField(
               label = 'Lugar',
               )
    longitud=forms.FloatField(required=False)
    latitud=forms.FloatField(required=False)
    class Meta:
        model=Ubicacion
        fields=['direccion','latitud','longitud']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['direccion'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['longitud'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['latitud'].widget.attrs.update({'class': 'form-control'}) 
    def clean(self, *args, **kwargs):
        cleaned_data = super(UbicacionForm, self).clean(*args, **kwargs)
        longitud = cleaned_data.get('longitud', None)
        latitud = cleaned_data.get('latitud', None)
        if longitud is None :
            self.add_error('direccion', 'Debe seleccionar una dirección')

class CongresoForms(MultiModelForm):
    form_classes = {
        'congreso': CongresForm,
        'ubicacion':UbicacionForm,
        'imagen_congreso':ImagenCongresoForms
    }
  
class PonenciaForm(forms.ModelForm):
    imagen=forms.ImageField(label='Buscar Imagen',required=False)
    titulo=forms.CharField(label='Título')
    cod_video=forms.CharField(label='Código del video en Vimeo',required=False)
    fecha_inicio=forms.DateTimeField()
    published=forms.BooleanField(label='Publicado',required=False)
    class Meta:
        model=Ponencia
        fields=['titulo','duracion','detalle','fecha_inicio','imagen','published','cod_video','congreso','bloque']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

        self.fields['titulo'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['duracion'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['congreso'].widget.attrs.update({'class': 'form-control'})
        self.fields['bloque'].widget.attrs.update({'class': 'form-control'})  
        self.fields['fecha_inicio'].widget.attrs.update({'class': 'form-control'})   
        self.fields['published'].widget.attrs.update({'class': 'form-control'})   
        self.fields['cod_video'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['detalle'].widget.attrs.update({'class': 'form-control','rows':'3'})  
    
    def clean(self, *args, **kwargs):
        cleaned_data = super(PonenciaForm, self).clean(*args, **kwargs)
        fecha_inicio = cleaned_data.get('fecha_inicio', None)
        bloq = cleaned_data.get('bloque', None)
        # bloque=Bloque.objects.get(pk=int(bloq))

        if bloq and fecha_inicio.date() != bloq.fecha_inicio.date():
            self.add_error('fecha_inicio', 'La fecha de inicio no coincide  con las del bloque que pertenece %s '%(bloq.fecha_inicio.date()))
    
class TallerForm(forms.ModelForm):
    imagen=forms.ImageField(label='Buscar Imagen',required=False)
    titulo=forms.CharField(label='Título')
    fecha_inicio=forms.DateTimeField()
    published=forms.BooleanField(label='Publicado',required=False)
    class Meta:
        model=Taller
        fields=['titulo','duracion','fecha_inicio','imagen','published','congreso','detalle','bloque']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

        self.fields['titulo'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['duracion'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['congreso'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['bloque'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['fecha_inicio'].widget.attrs.update({'class': 'form-control'})   
        self.fields['published'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['detalle'].widget.attrs.update({'class': 'form-control','rows':'3'}) 

    def clean(self, *args, **kwargs):
        cleaned_data = super(TallerForm, self).clean(*args, **kwargs)
        fecha_inicio = cleaned_data.get('fecha_inicio', None)
        bloq = cleaned_data.get('bloque', None)
        # bloque=Bloque.objects.get(pk=int(bloq))

        if bloq and fecha_inicio.date() != bloq.fecha_inicio.date():
            self.add_error('fecha_inicio', 'La fecha de inicio no coincide  con las del bloque que pertenece %s '%(bloq.fecha_inicio.date()))

class PonenciaForms(MultiModelForm):
    form_classes = {
        'ponencia': PonenciaForm,
        'ubicacion':UbicacionForm,
        
    }

class TallerForms(MultiModelForm):
    form_classes = {
        'taller': TallerForm,
        'ubicacion':UbicacionForm,
        
    }

class PonenteForm(forms.ModelForm):

    class Meta:
        model=Ponente
        fields=['user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

        self.fields['user'].widget.attrs.update({'class': 'form-control'}) 

class ModeradorForm(forms.ModelForm):
   
    class Meta:
        model=Moderador
        fields=['user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

        self.fields['user'].widget.attrs.update({'class': 'form-control'}) 
                
class PonentePonenciaForm(forms.ModelForm):
    ponente=forms.ModelChoiceField(queryset=Ponente.objects.all(),label='Ponentes')
  
    class Meta:
        model=RelPonenciaPonente
        fields=['ponente','ponencia']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

        self.fields['ponente'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['ponencia'].widget.attrs.update({'class': 'form-control','style':'display:none'}) 

class PonenteTallerForm(forms.ModelForm):
    ponente=forms.ModelChoiceField(queryset=Ponente.objects.all(),label='Ponentes')
  
    class Meta:
        model=RelTallerPonente
        fields=['ponente','taller']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

        self.fields['ponente'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['taller'].widget.attrs.update({'class': 'form-control','style':'display:none'}) 

class CongresoCategPagoForm(forms.ModelForm):
    categoria=forms.ModelChoiceField(queryset=CategoriaPagoCongreso.objects.all(),label='Categoría de Pago')
    
    class Meta:
        model=RelCongresoCategoriaPago
        fields=['categoria','congreso','precio','moneda']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

        self.fields['categoria'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['congreso'].widget.attrs.update({'class': 'form-control','style':'display:none'}) 
        self.fields['precio'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['moneda'].widget.attrs.update({'class': 'form-control'}) 

class TallerCategPagoForm(forms.ModelForm):
    categoria=forms.ModelChoiceField(queryset=CategoriaPagoCongreso.objects.all(),label='Categoría de Pago')
    
    class Meta:
        model=RelTalleresCategoriaPago
        fields=['categoria','taller','precio','moneda']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

        self.fields['categoria'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['taller'].widget.attrs.update({'class': 'form-control','style':'display:none'}) 
        self.fields['precio'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['moneda'].widget.attrs.update({'class': 'form-control'}) 
      
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
    
    class Meta:
        model=User
        fields=['username','first_name','last_name','email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({'class': 'form-control'}) 
      
          
        self.fields['first_name'].widget.attrs.update({'class': 'form-control','placeholder':'Nombre'})   
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})   
        self.fields['email'].widget.attrs.update({'class': 'form-control'})     

    # def clean(self, *args, **kwargs):
    #     cleaned_data = super(UserForm, self).clean(*args, **kwargs)
    #     password = cleaned_data.get('password', None)
    #     password1 = cleaned_data.get('password1', None)
    #     if password!=password1 :
    #         self.add_error('password1', 'No coinciden los password ')

class PerfilUserForm(forms.ModelForm):
    cel_profecional=forms.CharField(
               label = 'Cédula Profecional',
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
        fields=['cel_profecional','categoria','genero','especialidad','is_ponente','foto','detalle']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
         
        self.fields['cel_profecional'].widget.attrs.update({'class': 'form-control'})   
        self.fields['categoria'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['genero'].widget.attrs.update({'class': 'form-control'})
        self.fields['especialidad'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['detalle'].widget.attrs.update({'class': 'form-control','rows':'3'})   
       
class UsuarioForms(MultiModelForm):
    form_classes = {
        'user': UserForm,
        'perfiluser': PerfilUserForm,
        'ubicacion':UbicacionForm,
    }

class BloqueForms(forms.ModelForm):
    
    titulo=forms.CharField(label='Título')
    duracion=forms.CharField(label='Duración')
    published=forms.BooleanField(label='Publicado')
    congreso=forms.ModelChoiceField(queryset=Congreso.objects.filter(published=True),label='Congreso')
   
    
    class Meta:
        model=Bloque
        fields=['titulo','duracion','detalle','fecha_inicio','published','congreso']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

        self.fields['titulo'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['duracion'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['detalle'].widget.attrs.update({'class': 'form-control','rows':'3'})   
        self.fields['fecha_inicio'].widget.attrs.update({'class': 'form-control'})   
        self.fields['published'].widget.attrs.update({'class': 'form-control'})   
        self.fields['congreso'].widget.attrs.update({'class': 'form-control'})  

class OtrosForm(forms.ModelForm):

    class Meta:
        model=DatosIniciales
        fields=['ponentes','ponencias','paises','especialidades','eventos','afiliados','talleres','aviso_privacidad','terminos_condiciones']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

        self.fields['ponentes'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['ponencias'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['paises'].widget.attrs.update({'class': 'form-control','rows':'3'})   
        self.fields['especialidades'].widget.attrs.update({'class': 'form-control'})   
        self.fields['eventos'].widget.attrs.update({'class': 'form-control'})   
        self.fields['afiliados'].widget.attrs.update({'class': 'form-control'})  
        self.fields['talleres'].widget.attrs.update({'class': 'form-control'})   
        self.fields['aviso_privacidad'].widget.attrs.update({'class': 'form-control ckeditor'})  
        self.fields['terminos_condiciones'].widget.attrs.update({'class': 'form-control ckeditor'})  


class AsignarCongresoForms(forms.ModelForm):
    user=forms.ModelChoiceField(queryset=PerfilUsuario.objects.all(),label='Usuario')
    categoria_pago=forms.ModelChoiceField(queryset=CategoriaPagoCongreso.objects.all(),label='Categoría de Pago')
    is_pagado=forms.BooleanField(label='Pagó el Congreso')
    class Meta:
        model=RelCongresoUser
        fields=['user','congreso','categoria_pago','is_pagado']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

        self.fields['user'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['congreso'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['categoria_pago'].widget.attrs.update({'class': 'form-control','rows':'3'})   
        self.fields['is_pagado'].widget.attrs.update({'class': 'form-control'})   
         
class AsignarTallerForms(forms.ModelForm):
    user=forms.ModelChoiceField(queryset=PerfilUsuario.objects.all(),label='Usuario')
    categoria_pago=forms.ModelChoiceField(queryset=CategoriaPagoCongreso.objects.all(),label='Categoría de Pago')
    is_pagado=forms.BooleanField(label='Pagó el Taller')
    class Meta:
        model=RelTallerUser
        fields=['user','taller','categoria_pago','is_pagado']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

        self.fields['user'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['taller'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['categoria_pago'].widget.attrs.update({'class': 'form-control','rows':'3'})   
        self.fields['is_pagado'].widget.attrs.update({'class': 'form-control'})   
          
class ModeradorBloqueForm(forms.ModelForm):
    moderador=forms.ModelChoiceField(queryset=Moderador.objects.all(),label='Moderador')
  
    class Meta:
        model=RelBloqueModerador
        fields=['moderador','bloque']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

        self.fields['moderador'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['bloque'].widget.attrs.update({'class': 'form-control','style':'display:none'}) 

class ImagenCongForms(forms.ModelForm):
    imagen=forms.ImageField(label='Buscar Imagen')
    class Meta:
        model=ImagenCongreso
        fields=['imagen','congreso']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

        self.fields['imagen'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['congreso'].widget.attrs.update({'class': 'form-control'}) 

    def clean(self, *args, **kwargs):
        cleaned_data = super(ImagenCongForms, self).clean(*args, **kwargs)
        imagen = cleaned_data.get('imagen', None)
        w, h = get_image_dimensions(imagen)
        if w != 1920 or h != 1080:
            self.add_error('imagen',"Esta imagen tiene %s X %s pixel. Debe ser de 1920 X 1080 pixel" %(w,h) )
        
       




