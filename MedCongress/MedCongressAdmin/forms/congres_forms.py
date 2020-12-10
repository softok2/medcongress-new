from django import forms
from datetime import date
from django.core.files.images import get_image_dimensions
from  MedCongressApp.models import (Congreso,Ubicacion,ImagenCongreso,TipoCongreso,Ponencia,Taller,
                                    Ponente,PerfilUsuario,RelPonenciaPonente,RelCongresoCategoriaPago,
                                    CategoriaPagoCongreso,RelTalleresCategoriaPago,Genero,CategoriaUsuario,
                                    RelTallerPonente,Bloque,DatosIniciales,RelCongresoUser,RelTallerUser,
                                    Moderador,RelBloqueModerador,ImagenCongreso,CuestionarioPregunta,CuestionarioRespuestas,
                                    MetaPagInicio,MetaPagListCongreso,PreguntasFrecuentes)
                    
from django.contrib.auth.models import Group, User
from betterforms.multiform import MultiModelForm

        
class CongresForm(forms.ModelForm):
    imagen_seg=forms.ImageField(label='Buscar Imagen',required=False)
    is_openpay=forms.BooleanField(label='Pagar por OpenPay',required=False)
    titulo=forms.CharField(label='Título')
    template=forms.CharField(label='Template del Congreso',required=False)
    published=forms.BooleanField(label='Publicado',required=False)
    sub_titulo=forms.CharField(label='Título segundario',required=False) 
    t_congreso=forms.ModelChoiceField(queryset=TipoCongreso.objects.all(),label='Tipo de Congreso')
    fecha_inicio=forms.DateTimeField(widget=forms.TextInput())
    score=forms.IntegerField(label='Puntuación del Congreso')
   
    class Meta:
        model=Congreso
        fields=['titulo','sub_titulo','imagen_seg','fecha_inicio','published','t_congreso','especialidad','is_openpay','template','foto_constancia','aprobado','cant_preguntas','score','streaming']

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
        self.fields['foto_constancia'].widget.attrs.update({'class': 'form-control',}) 
        self.fields['aprobado'].widget.attrs.update({'class': 'form-control',})  
        self.fields['cant_preguntas'].widget.attrs.update({'class': 'form-control',})                        
        self.fields['score'].widget.attrs.update({'class': 'form-control',})   
        self.fields['streaming'].widget.attrs.update({'class': 'form-control','rows':'3'})   
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
    fecha_inicio=forms.DateTimeField()
    published=forms.BooleanField(label='Publicado',required=False)
  
    class Meta:
        model=Ponencia
        fields=['titulo','duracion','detalle','fecha_inicio','imagen','published','cod_video','congreso','bloque','is_info']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

        self.fields['titulo'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['duracion'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['congreso'].widget.attrs.update({'class': 'form-control'})
        self.fields['bloque'].widget.attrs.update({'class': 'form-control'})  
        self.fields['fecha_inicio'].widget.attrs.update({'class': 'form-control'})   
        self.fields['published'].widget.attrs.update({'class': 'form-control'})   
        self.fields['cod_video'].widget.attrs.update({'class': 'form-control','rows':'3'}) 
        self.fields['detalle'].widget.attrs.update({'class': 'form-control','rows':'3'})  
       
    
    def clean(self, *args, **kwargs):
        cleaned_data = super(PonenciaForm, self).clean(*args, **kwargs)
        fecha_inicio = cleaned_data.get('fecha_inicio', None)
        bloq = cleaned_data.get('bloque', None)
        imagen = cleaned_data.get('imagen', None)
        w, h = get_image_dimensions(imagen)
        if w != 1920 or h != 1080:
            self.add_error('imagen',"Esta imagen tiene %s X %s pixel. Debe ser de 1920 X 1080 pixel" %(w,h) )
   

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
    user=forms.ModelChoiceField(queryset=PerfilUsuario.objects.all(),label='Entre Email del Usuario',required=False)
    class Meta:
        model=Ponente
        fields=['user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

        self.fields['user'].widget.attrs.update({'class': 'form-control'}) 

    def clean(self, *args, **kwargs):
        cleaned_data = super(PonenteForm, self).clean(*args, **kwargs)
        user = cleaned_data.get('user', None)
        if not user:
            self.add_error('user', 'No existe ese User')

class ModeradorForm(forms.ModelForm):
    user=forms.ModelChoiceField(queryset=PerfilUsuario.objects.all(),label='Entre Email del Usuario', required=False)
    class Meta:
        model=Moderador
        fields=['user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

        self.fields['user'].widget.attrs.update({'class': 'form-control'}) 

    def clean(self, *args, **kwargs):
        cleaned_data = super(ModeradorForm, self).clean(*args, **kwargs)
        user = cleaned_data.get('user', None)
       
        if not user:
            self.add_error('user', 'No existe ese User')
class PonentePonenciaForm(forms.ModelForm):
    ponente=forms.ModelChoiceField(queryset=Ponente.objects.all(),label='Entre Email del Ponentes',required=False)
  
    class Meta:
        model=RelPonenciaPonente
        fields=['ponente','ponencia']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

        self.fields['ponente'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['ponencia'].widget.attrs.update({'class': 'form-control','style':'display:none'}) 
      
    def clean(self, *args, **kwargs):
        cleaned_data = super(PonentePonenciaForm, self).clean(*args, **kwargs)
        user = cleaned_data.get('ponente', None)
        ponencia = cleaned_data.get('ponencia', None)
       
        if not user:
            self.add_error('ponente', 'No existe ese Ponente')

        if RelPonenciaPonente.objects.filter(ponencia=ponencia,ponente=user).exists():
            self.add_error('ponente', 'Esta Ponencia ya tiene un ponente con ese Email')

class PonenteTallerForm(forms.ModelForm):
    ponente=forms.ModelChoiceField(queryset=Ponente.objects.all(),label='Entre Email del Ponentes',required=False)
  
    class Meta:
        model=RelTallerPonente
        fields=['ponente','taller']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

        self.fields['ponente'].widget.attrs.update({'class': 'form-control'}) 
        
        self.fields['taller'].widget.attrs.update({'class': 'form-control','style':'display:none'}) 
    def clean(self, *args, **kwargs):
        cleaned_data = super(PonenteTallerForm, self).clean(*args, **kwargs)
        user = cleaned_data.get('ponente', None)
        taller = cleaned_data.get('taller', None)
       
        if not user:
            self.add_error('ponente', 'No existe ese Ponente')

        if RelTallerPonente.objects.filter(taller=taller,ponente=user).exists():
            self.add_error('ponente', 'Este taller ya tiene un ponente con ese Email')
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

    def clean(self, *args, **kwargs):
        cleaned_data = super(UserForm, self).clean(*args, **kwargs)
        email = cleaned_data.get('email', None)
        username= cleaned_data.get('username',None)
        if User.objects.filter(email=email).exclude(username=username).count():
            self.add_error('email', 'Ese Email ya existe! ')

class PerfilUserForm(forms.ModelForm):
    cel_profecional=forms.CharField(
               label = 'Cédula Profecional',
                required=False
               )
    is_ponente=forms.BooleanField(
                label = 'Desearía ser ponente en un evento   ',
                required=False
               
               )
    facebook=forms.CharField(required=False)
    twitter=forms.CharField(required=False)
    youtube=forms.CharField(required=False)
    linkedin=forms.CharField(required=False)
    num_telefono=forms.CharField(required=False,label='Número de Teléfono')
    fecha_nacimiento=forms.DateField(required=False,label='Fecha de Nacimiento')
    genero=forms.ModelChoiceField(queryset=Genero.objects.all(), label='Género')
    
    categoria=forms.ModelChoiceField(queryset=CategoriaUsuario.objects.filter(published=True),label='Categoría')
   
    class Meta:
        model=PerfilUsuario
        fields=['cel_profecional','categoria','especialidad','is_ponente','foto','detalle','datos_interes','genero','linkedin','youtube','facebook','twitter','publicaciones','puesto','num_telefono','fecha_nacimiento']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
         
        self.fields['cel_profecional'].widget.attrs.update({'class': 'form-control'})   
        self.fields['categoria'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['genero'].widget.attrs.update({'class': 'form-control'})
        self.fields['especialidad'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['detalle'].widget.attrs.update({'class': 'form-control ckeditor'}) 
        self.fields['datos_interes'].widget.attrs.update({'class': 'form-control ckeditor'}) 
        self.fields['publicaciones'].widget.attrs.update({'class': 'form-control ckeditor'})    
        self.fields['linkedin'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['youtube'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['facebook'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['twitter'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['puesto'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['fecha_nacimiento'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['num_telefono'].widget.attrs.update({'class': 'form-control'}) 
       
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
        fields=['ponentes','ponencias','paises','especialidades','eventos','afiliados','talleres','aviso_privacidad']

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


class AsignarCongresoForms(forms.ModelForm):
    user=forms.ModelChoiceField(queryset=PerfilUsuario.objects.all(),label='Email del Usuario')
    categoria_pago=forms.ModelChoiceField(queryset=CategoriaPagoCongreso.objects.all(),label='Categoría de Pago')
    is_pagado=forms.BooleanField(label='Pagó el Congreso')
    cantidad=forms.IntegerField(label='Cantidad',initial=1)
    class Meta:
        model=RelCongresoUser
        fields=['user','congreso','categoria_pago','is_pagado','cantidad']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

        self.fields['user'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['congreso'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['categoria_pago'].widget.attrs.update({'class': 'form-control','rows':'3'})   
        self.fields['is_pagado'].widget.attrs.update({'class': 'form-control'})   
        self.fields['cantidad'].widget.attrs.update({'class': 'form-control'})  
         
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
    moderador=forms.ModelChoiceField(queryset=Moderador.objects.all(),label='Moderador',required=False)
  
    class Meta:
        model=RelBloqueModerador
        fields=['moderador','bloque']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

        self.fields['moderador'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['bloque'].widget.attrs.update({'class': 'form-control','style':'display:none'}) 

    def clean(self, *args, **kwargs):
        cleaned_data = super(ModeradorBloqueForm, self).clean(*args, **kwargs)
        moderador = cleaned_data.get('moderador', None)
        bloque = cleaned_data.get('bloque', None)
       
        if not moderador:
            self.add_error('moderador', 'No existe ese Moderador')

        if RelBloqueModerador.objects.filter(bloque=bloque,moderador=moderador).exists():
            self.add_error('moderador', 'Este Bloque ya tiene un moderador con ese Email')
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

class PreguntaForm(forms.ModelForm):
    congreso=forms.ModelChoiceField(queryset=Congreso.objects.filter(published=True),label='Congreso')
    published=forms.BooleanField(label='Publicada',required=False)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

        self.fields['congreso'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['pregunta'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['published'].widget.attrs.update({'class': 'form-control'}) 
     
    class Meta:
        model=CuestionarioPregunta
        fields=['congreso','pregunta','published']

class RespuestasForm(forms.ModelForm):
    
    respuesta=forms.MultipleChoiceField(widget=forms.TextInput())

    class Meta:
        model=CuestionarioRespuestas
        fields=['respuesta','is_correcto']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

        self.fields['respuesta'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['is_correcto'].widget.attrs.update({'class': 'form-control'}) 
        

class CuestionarioForms(MultiModelForm):
    form_classes = {
        'pregunta': PreguntaForm,
        'respuesta': RespuestasForm,
        
    }

class MetaPagInicioForm(forms.ModelForm):

    

    class Meta:
        model=MetaPagInicio
        fields=['meta_og_title','meta_description','meta_og_description','meta_og_type','meta_og_url',
        'meta_twitter_card','meta_twitter_site','meta_twitter_creator','meta_keywords','meta_og_imagen','meta_title']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

        self.fields['meta_og_title'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['meta_description'].widget.attrs.update({'class': 'form-control','rows':'3'}) 
        self.fields['meta_og_description'].widget.attrs.update({'class': 'form-control','rows':'3'})   
        self.fields['meta_og_type'].widget.attrs.update({'class': 'form-control'})   
        self.fields['meta_og_url'].widget.attrs.update({'class': 'form-control'})   
        self.fields['meta_twitter_card'].widget.attrs.update({'class': 'form-control'})  
        self.fields['meta_twitter_site'].widget.attrs.update({'class': 'form-control'})   
        self.fields['meta_twitter_creator'].widget.attrs.update({'class': 'form-control '})  
        self.fields['meta_keywords'].widget.attrs.update({'class': 'form-control','rows':'3'})   
        self.fields['meta_og_imagen'].widget.attrs.update({'class': 'form-control '}) 
        self.fields['meta_title'].widget.attrs.update({'class': 'form-control'})   
          
class PregFrecuenteForm(forms.ModelForm):
    
    class Meta:
        model=PreguntasFrecuentes
        fields=['pregunta','respuesta','congreso','published']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

        self.fields['pregunta'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['respuesta'].widget.attrs.update({'class': 'form-control ckeditor'}) 
        self.fields['congreso'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['published'].widget.attrs.update({'class': 'form-control'}) 

    # def clean(self, *args, **kwargs):
    #     cleaned_data = super(ImagenCongForms, self).clean(*args, **kwargs)
    #     imagen = cleaned_data.get('imagen', None)
    #     w, h = get_image_dimensions(imagen)
    #     if w != 1920 or h != 1080:
    #         self.add_error('imagen',"Esta imagen tiene %s X %s pixel. Debe ser de 1920 X 1080 pixel" %(w,h) )


class ExportarExelForm(forms.ModelForm):
    
    congreso=forms.ModelChoiceField(queryset=Congreso.objects.all(),label='Filtrar Congreso',required=False)

    class Meta:
        model=RelCongresoUser
        fields=['congreso']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

        self.fields['congreso'].widget.attrs.update({'class': 'form-control'}) 
       
    def clean(self, *args, **kwargs):
        cleaned_data = super(ExportarExelForm, self).clean(*args, **kwargs)
        congreso = cleaned_data.get('congreso', None)
      
        if not congreso:
            print(congreso)
            self.add_error('congreso','Entre un congreso ')

