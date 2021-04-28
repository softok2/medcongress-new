from django import forms
from datetime import date,datetime
from django.contrib import messages
from django.db.models import Sum
from django.core.files.images import get_image_dimensions
from  MedCongressApp.models import (Congreso,Ubicacion,ImagenCongreso,TipoCongreso,Ponencia,Taller,
                                    Ponente,PerfilUsuario,RelPonenciaPonente,RelCongresoCategoriaPago,
                                    CategoriaPagoCongreso,RelTalleresCategoriaPago,Genero,CategoriaUsuario,
                                    RelTallerPonente,Bloque,DatosIniciales,RelCongresoUser,RelTallerUser,
                                    Moderador,RelBloqueModerador,ImagenCongreso,CuestionarioPregunta,CuestionarioRespuestas,
                                    MetaPagInicio,MetaPagListCongreso,PreguntasFrecuentes,RelCongresoAval, AvalCongreso,RelCongresoSocio,SocioCongreso,
                                    Idioma,DocumentoPrograma,TrabajosInvestigacion)
                    
from django.contrib.auth.models import Group, User
from betterforms.multiform import MultiModelForm
from django.core.exceptions import NON_FIELD_ERRORS
from django.forms.models import ModelMultipleChoiceField   
import re     
class CongresForm(forms.ModelForm):
    
    is_openpay=forms.BooleanField(label='Pagar por OpenPay',required=False)
    titulo=forms.CharField(label='Título')
    prueba=forms.CharField(required=False)
    prueba1=forms.CharField(required=False)
    imagen_home=forms.CharField(required=False,label='Imagen Principal')
    constancia=forms.CharField(required=False)
    template=forms.CharField(label='Template del Congreso',required=False)
    published=forms.BooleanField(label='Publicado',required=False)
    ver_titulo=forms.BooleanField(label='Ver Título',required=False)
    sub_titulo=forms.CharField(label='Título segundario',required=False) 
    t_congreso=forms.ModelChoiceField(queryset=TipoCongreso.objects.all(),label='Tipo de Congreso')
    # fecha_inicio=forms.DateTimeField()
    score=forms.IntegerField(label='Puntuación del Congreso')
    # foto_constancia=forms.ImageField(label='Buscar Imagen para la Constancia',required=False,)

    class Meta:
        model=Congreso
        fields=['titulo','sub_titulo','fecha_inicio','published','t_congreso','especialidad','is_openpay','template','constancia','aprobado','cant_preguntas','score','streaming','meta_og_title','meta_description','meta_og_description','meta_og_type','meta_og_url',
        'meta_twitter_card','meta_twitter_site','meta_twitter_creator','meta_keywords','meta_og_imagen','meta_title','detalles_tipo_boleto','detalles_tipo_boleto_taller','ver_titulo','vid_publicidad','prueba','prueba1','imagen_home']
       
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

        self.fields['titulo'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['sub_titulo'].widget.attrs.update({'class': 'form-control'}) 
        # self.fields['imagen_seg'].widget.attrs.update({ 'data-toggle':"tooltip",'data-popup':"tooltip-custom", 'data-original-title':"La Imagen debe ser de 1140 X 240 pixel "})  
        # self.fields['imagen_seg'].widget.attrs.update({'class': ' form-control '}) 
        self.fields['fecha_inicio'].widget.attrs.update({'class': 'form-control'})   
        self.fields['published'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['ver_titulo'].widget.attrs.update({'class': 'form-control'})    
        self.fields['t_congreso'].widget.attrs.update({'class': 'form-control'})  
        self.fields['especialidad'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['is_openpay'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['template'].widget.attrs.update({'class': 'form-control',})
        # self.fields['foto_constancia'].widget.attrs.update({'class': 'form-control',}) 
        self.fields['aprobado'].widget.attrs.update({'class': 'form-control',})  
        self.fields['cant_preguntas'].widget.attrs.update({'class': 'form-control',})                        
        self.fields['score'].widget.attrs.update({'class': 'form-control',})   
        self.fields['streaming'].widget.attrs.update({'class': 'form-control','rows':'3'}) 
        self.fields['vid_publicidad'].widget.attrs.update({'class': 'form-control','rows':'3'})
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
        self.fields['detalles_tipo_boleto'].widget.attrs.update({'class': 'form-control ckeditor'})
        self.fields['detalles_tipo_boleto_taller'].widget.attrs.update({'class': 'form-control ckeditor'})     
   
    
    def clean(self, *args, **kwargs):
        try:
            cleaned_data = super(CongresForm, self).clean(*args, **kwargs)
            imagenes = cleaned_data.get('prueba', None)
            
            imagen_seg = cleaned_data.get('prueba1', None)
            constancia = cleaned_data.get('constancia', None)
            imagen_home = cleaned_data.get('imagen_home', None)
            
            if not imagenes :
                self.add_error('prueba', 'Debe al menos entrar una <b>Imagen Principal</b>')
            if not imagen_seg :
                self.add_error('prueba1', 'Debe  entrar una <b>Imagen Segundaria</b>')
            if not imagen_home :
                self.add_error('imagen_home', 'Debe  entrar una <b>Imagen Principal</b>')
        except Exception as e:
            print('dfvdfbhfghjghg')
            print(e)
            messages.warning(self.request, e)
            
class ImagenCongresoForms(forms.ModelForm):
    imagen=forms.ImageField()
    
    class Meta:
        model=ImagenCongreso
        fields=['imagen']       
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['imagen'].widget.attrs.update({ 'data-toggle':"tooltip",'data-popup':"tooltip-custom", 'data-original-title':"La Imagen debe ser de 1920 X 1080 pixel "})  

    def clean(self, *args, **kwargs):
        
        cleaned_data = super(ImagenCongresoForms, self).clean(*args, **kwargs)
        imagen = cleaned_data.get('imagen', None)
       
        if imagen:
            w, h = get_image_dimensions(imagen)
            if w != 1920 or h != 1080:
                self.add_error('imagen',"La <b> Imagen Principal</b> tiene %s X %s pixel. Debe ser de<b> 1920 X 1080 pixel</b>" %(w,h) )
        
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
        # 'imagen_congreso':ImagenCongresoForms
    }

class MyMultipleModelChoiceField(ModelMultipleChoiceField):

    def label_from_instance(self, obj):
        return "%s" % (obj.user.usuario.email)

class PonenciaForm(forms.ModelForm):
    prueba=forms.CharField(required=False)
    titulo=forms.CharField(label='Título')
    fecha_inicio=forms.DateTimeField()
    published=forms.BooleanField(label='Publicado',required=False)
    # ponente=forms.ModelMultipleChoiceField(queryset=Ponente.objects.all(),label='Ponente',required=False)
    # ponente=forms.ModelChoiceField(queryset=Ponente.objects.all(),label='Ponente',required=False)
    error=forms.CharField(required=False)
    class Meta:
        model=Ponencia
        fields=['titulo','duracion','detalle','fecha_inicio','published','cod_video','congreso','bloque','is_info',
        'meta_og_title','meta_description','meta_og_description','meta_og_type','meta_og_url',
        'meta_twitter_card','meta_twitter_site','meta_twitter_creator','meta_keywords','meta_og_imagen','meta_title','error','prueba']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

        
        self.fields['titulo'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['duracion'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['congreso'].widget.attrs.update({'class': 'form-control'})
        self.fields['bloque'].widget.attrs.update({'class': 'form-control'})  
        self.fields['fecha_inicio'].widget.attrs.update({'class': 'form-control'})   
        self.fields['published'].widget.attrs.update({'class': 'form-control'})  
        # self.fields['ponente'].widget.attrs.update({'class': 'form-control'})   
        self.fields['cod_video'].widget.attrs.update({'class': 'form-control','rows':'6'}) 
        self.fields['detalle'].widget.attrs.update({'class': 'form-control','rows':'3'})  
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
       
        # self.fields['ponente'].widget.attrs.update({'class': 'form-control multiple-select-box selectivity-input'})  
    
    def clean(self, *args, **kwargs):
        try:
            cleaned_data = super(PonenciaForm, self).clean(*args, **kwargs)
            fecha_inicio = cleaned_data.get('fecha_inicio', None)
            bloq = cleaned_data.get('bloque', None)
            congreso=cleaned_data.get('congreso', None)
            imagenes = cleaned_data.get('prueba', None)
        
        
            if not imagenes :
                self.add_error('prueba', 'Debe entrar una <b>Imagen </b> a la ponencia')


            if bloq and fecha_inicio.date() != bloq.fecha_inicio.date():
                self.add_error('fecha_inicio', 'La fecha de inicio no coincide  con las del bloque que pertenece %s '%(bloq.fecha_inicio.date()))
                return
            try:
                if fecha_inicio < congreso.fecha_inicio:
                    self.add_error('fecha_inicio', 'Esta Fecha no puede ser menor  que la Fecha de inicio del Congreso %s'%(congreso.fecha_inicio))
                    return
            except Exception as e:
                self.add_error('fecha_inicio','Entre bien la Fecha')
        except Exception as e:
            self.add_error('error', e)


class PonenciaPonenteForm(forms.ModelForm):
   
    ponente=forms.ModelMultipleChoiceField(queryset=Ponente.objects.all(),label='Ponente',required=True)
  
    class Meta:
        model=Ponente
        fields=['ponente',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        self.fields['ponente'].widget.attrs.update({'class': 'select2 form-control','multiple':"multiple"}) 
        # self.fields['ponente'] = MyMultipleModelChoiceField(
        #     queryset=Ponente.objects.all(), 
        #     required=True, 
        #     widget=forms.SelectMultiple())
    # def clean(self, *args, **kwargs):
    #     try:
    #         cleaned_data = super(PonenciaPonenteForm, self).clean(*args, **kwargs)
    #         ponente = cleaned_data.items
           
    #         if not ponente:
    #             self.add_error('ponente', 'Este Campo es obligatorio mio')
    #             return

    #     except Exception as e:
    #         self.add_error('error', e)    

class TallerForm(forms.ModelForm):
    prueba=forms.CharField(required=False)
    
    titulo=forms.CharField(label='Título')
    fecha_inicio=forms.DateTimeField()
    published=forms.BooleanField(label='Publicado',required=False)
    score=forms.IntegerField(label='Puntuación del Taller')
    foto_constancia=forms.ImageField(label='Buscar Imagen para la Constancia',required=False,)
    class Meta:
        model=Taller
        fields=['titulo','duracion','fecha_inicio','prueba','published','congreso','detalle','bloque',
        'meta_og_title','meta_description','meta_og_description','meta_og_type','meta_og_url',
        'meta_twitter_card','meta_twitter_site','meta_twitter_creator','meta_keywords','meta_og_imagen','meta_title','cod_video','score']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

        self.fields['titulo'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['duracion'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['congreso'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['bloque'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['fecha_inicio'].widget.attrs.update({'class': 'form-control'})   
        self.fields['published'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['score'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['detalle'].widget.attrs.update({'class': 'form-control','rows':'3'}) 
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
        self.fields['cod_video'].widget.attrs.update({'class': 'form-control','rows':'3'}) 
        

    def clean(self, *args, **kwargs):
        cleaned_data = super(TallerForm, self).clean(*args, **kwargs)
        fecha_inicio = cleaned_data.get('fecha_inicio', None)
        bloq = cleaned_data.get('bloque', None)
        # bloque=Bloque.objects.get(pk=int(bloq))
        imagen = cleaned_data.get('prueba', None)
        if not imagen :
                self.add_error('prueba', 'Debe entrar una <b>Imagen </b> al Taller')
        try:
            if bloq and fecha_inicio.date() != bloq.fecha_inicio.date():
                self.add_error('fecha_inicio', 'La <b> Fecha de Inicio</b> no coincide con la del bloque que pertenece <b> %s</b> '%(bloq.fecha_inicio.date()))
        except Exception as e:
            self.add_error('fecha_inicio','Entre bien la <b>Fecha de Inicio</b>')
class PonenciaForms(MultiModelForm):
    form_classes = {
        'ponencia': PonenciaForm,
        'ubicacion':UbicacionForm,
        'ponencia_ponente':PonenciaPonenteForm,
        
    }

class TallerForms(MultiModelForm):
    form_classes = {
        'taller': TallerForm,
        'ubicacion':UbicacionForm,
        'taller_ponente':PonenciaPonenteForm,
    }

class PonenteForm(forms.ModelForm):
    user=forms.ModelChoiceField(queryset=PerfilUsuario.objects.all(),label='Seleccione usuario',required=True)
    class Meta:
        model=Ponente
        fields=['user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

        self.fields['user'].widget.attrs.update({'class': 'select2 form-control '}) 

    def clean(self, *args, **kwargs):
        cleaned_data = super(PonenteForm, self).clean(*args, **kwargs)
        user = cleaned_data.get('user', None)
        if not user:
            self.add_error('user', 'Debe entrar un <b>Usuario</b>')
        else:
            if Ponente.objects.filter(user=user).exists():
                self.add_error('user', 'Este <b>Ponente</b> ya existe')

class ModeradorForm(forms.ModelForm):
    user=forms.ModelChoiceField(queryset=PerfilUsuario.objects.all(),label='Seleccione usuario',required=True)
    class Meta:
        model=Moderador
        fields=['user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

        self.fields['user'].widget.attrs.update({'class': 'select2 form-control'}) 

    def clean(self, *args, **kwargs):
        cleaned_data = super(ModeradorForm, self).clean(*args, **kwargs)
        user = cleaned_data.get('user', None)
       
        if not user:
            self.add_error('user', 'Debe entrar un Usuario')
            
class PonentePonenciaForm(forms.ModelForm):
    ponente=forms.ModelChoiceField(queryset=Ponente.objects.all(),label='Seleccione Usuario',required=True)
  
    class Meta:
        model=RelPonenciaPonente
        fields=['ponente','ponencia']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

        self.fields['ponente'].widget.attrs.update({'class': 'select2 form-control'}) 
        self.fields['ponencia'].widget.attrs.update({'class': 'form-control','style':'display:none'}) 
      
    def clean(self, *args, **kwargs):
        cleaned_data = super(PonentePonenciaForm, self).clean(*args, **kwargs)
        user = cleaned_data.get('ponente', None)
        ponencia = cleaned_data.get('ponencia', None)
       
        if not user:
            self.add_error('ponente', 'Entre un Ponente')

        if RelPonenciaPonente.objects.filter(ponencia=ponencia,ponente=user).exists():
            self.add_error('ponente', 'Esta Ponencia ya tiene este Ponente')

class PonenteTallerForm(forms.ModelForm):
    ponente=forms.ModelChoiceField(queryset=Ponente.objects.all(),label='Seleccione Usuario',required=True)
  
    class Meta:
        model=RelTallerPonente
        fields=['ponente','taller']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

        self.fields['ponente'].widget.attrs.update({'class': 'select2 form-control'}) 
        
        self.fields['taller'].widget.attrs.update({'class': 'form-control','style':'display:none'}) 
    def clean(self, *args, **kwargs):
        cleaned_data = super(PonenteTallerForm, self).clean(*args, **kwargs)
        user = cleaned_data.get('ponente', None)
        taller = cleaned_data.get('taller', None)
       
        if not user:
            self.add_error('ponente', 'Entre un Ponente')

        if RelTallerPonente.objects.filter(taller=taller,ponente=user).exists():
            self.add_error('ponente', 'Este taller ya tiene ese Ponente')
class CongresoCategPagoForm(forms.ModelForm):
    categoria=forms.ModelChoiceField(queryset=CategoriaPagoCongreso.objects.all(),label='Categoría de Pago')
    
    class Meta:
        model=RelCongresoCategoriaPago
        fields=['categoria','congreso','precio','moneda']
       

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

        self.fields['categoria'].widget.attrs.update({'class': 'form-control select2'}) 
        self.fields['congreso'].widget.attrs.update({'class': 'form-control','style':'display:none'}) 
        self.fields['precio'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['moneda'].widget.attrs.update({'class': 'form-control'}) 
        
    def clean(self, *args, **kwargs):
      
        cleaned_data = super(CongresoCategPagoForm, self).clean(*args, **kwargs)
        precio=cleaned_data.get('precio', None)

        if precio<0:
            self.add_error('precio', ' El PRECIO debe ser valor positivo')
        
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
        
    def clean(self, *args, **kwargs):
      
        cleaned_data = super(TallerCategPagoForm, self).clean(*args, **kwargs)
        precio=cleaned_data.get('precio', None)

        if precio<0:
            self.add_error('precio', ' El PRECIO debe ser valor positivo')
        
class UserForm(forms.ModelForm):
    first_name=forms.CharField(
               label = 'Nombre',
               )
    last_name=forms.CharField(
                label = 'Apellidos',
                )
    username= forms.CharField(
               label = 'Usuario',required=False
               )
    email= forms.CharField(
               label = 'Correo'
               )          
    
    class Meta:
        model=User
        fields=['first_name','last_name','email','username']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

 
      
          
        self.fields['first_name'].widget.attrs.update({'class': 'form-control','placeholder':'Nombre'})   
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})   
        self.fields['email'].widget.attrs.update({'class': 'form-control'})  
        self.fields['username'].widget.attrs.update({'type': 'hidden'})    

    def clean(self, *args, **kwargs):
        cleaned_data = super(UserForm, self).clean(*args, **kwargs)
        email = cleaned_data.get('email', None)
        username= cleaned_data.get('username',None)
        if User.objects.filter(email=email).exclude(username=username).count():
            self.add_error('email', '¡Ese Correo ya existe! ')
        nombre = cleaned_data.get('first_name', None)
        apellido = cleaned_data.get('last_name', None)                                                      
        if not re.match(r"^[A-Za-zñÑáéíóúÁÉÍÓÚ. ]+$",nombre):
            self.add_error('first_name', 'El Campo <b> Nombre</b> solo admite letras ')
        if not re.match(r"^[A-Za-zñÑáéíóúÁÉÍÓÚ. ]+$",apellido):
            self.add_error('first_name', 'El Campo <b> Apellidos</b> solo admite letras ') 
class PerfilUserForm(forms.ModelForm):
    cel_profecional=forms.CharField(
               label = 'Cédula Profesional',
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
    
    categoria=forms.ModelChoiceField(queryset=CategoriaUsuario.objects.all(),label='Categoría')
   
    class Meta:
        model=PerfilUsuario
        fields=['cel_profecional','categoria','especialidad','is_ponente','foto','detalle','datos_interes','genero','linkedin','youtube','facebook','twitter','publicaciones','puesto','num_telefono','fecha_nacimiento',
        'meta_og_title','meta_description','meta_og_description','meta_og_type','meta_og_url',
        'meta_twitter_card','meta_twitter_site','meta_twitter_creator','meta_keywords','meta_og_imagen','meta_title']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
         
        self.fields['cel_profecional'].widget.attrs.update({'class': 'form-control'})   
        self.fields['categoria'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['genero'].widget.attrs.update({'class': 'form-control'})
        self.fields['especialidad'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['detalle'].widget.attrs.update({'class': 'form-control ckeditor'}) 
        self.fields['datos_interes'].widget.attrs.update({'class': 'form-control ckeditor '}) 
        self.fields['publicaciones'].widget.attrs.update({'class': 'form-control ckeditor'})    
        self.fields['linkedin'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['youtube'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['is_ponente'].widget.attrs.update({'class': ' form-check-input me-2','id':'flexCheckDefault'}) 
        self.fields['facebook'].widget.attrs.update({'class': 'form-control '}) 
        self.fields['twitter'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['puesto'].widget.attrs.update({'class': 'form-control','rows':'2','style':'height: 10%;'}) 
        self.fields['fecha_nacimiento'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['num_telefono'].widget.attrs.update({'class': 'form-control'}),
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
       
class UsuarioForms(MultiModelForm):
    form_classes = {
        'user': UserForm,
        'perfiluser': PerfilUserForm,
        'ubicacion':UbicacionForm,
    }

class BloqueForms(forms.ModelForm):
    
    titulo=forms.CharField(label='Título')
    duracion=forms.CharField(label='Duración')
    published=forms.BooleanField(label='Publicado',required=False)
    congreso=forms.ModelChoiceField(queryset=Congreso.objects.all(),label='Congreso',required=True)
    # fecha_inicio=forms.DateTimeField(required=True)
    
    class Meta:
        model=Bloque
        fields=['titulo','duracion','detalle','fecha_inicio','published','congreso']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        # self.fields['fecha_inicio'].input_formats = ['%d/%m/%Y %H:%M:%S']
        self.fields['titulo'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['duracion'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['detalle'].widget.attrs.update({'class': 'form-control','rows':'3'})   
        self.fields['fecha_inicio'].widget.attrs.update({'class': 'form-control'})   
        self.fields['published'].widget.attrs.update({'class': 'form-control'})   
        self.fields['congreso'].widget.attrs.update({'class': 'form-control select2'})  

    def clean(self, *args, **kwargs):
        cleaned_data = super(BloqueForms, self).clean(*args, **kwargs)
        congreso = cleaned_data.get('congreso', None)
        titulo = cleaned_data.get('titulo', None)
        fecha = cleaned_data.get('fecha_inicio')
        if not congreso:
            self.add_error('congreso', 'Debe entrar un  <b>Congreso</b>')
            return
        if fecha:
            if fecha < congreso.fecha_inicio:
                self.add_error('fecha_inicio', 'Esta <b>Fecha</b> no puede ser menor  que la <b>Fecha de inicio del Congreso ( %s )  </b>'%(congreso.fecha_inicio))
   
       
        
        
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
    user=forms.ModelChoiceField(queryset=PerfilUsuario.objects.all(),label='Correo del Usuario',required=True)
    categoria_pago=forms.ModelChoiceField(queryset=CategoriaPagoCongreso.objects.all(),label='Categoría de Pago')
    congreso=forms.ModelChoiceField(queryset=Congreso.objects.all(),label='Congreso',required=True)
    is_pagado=forms.BooleanField(label='Pagó el Congreso')
    cantidad=forms.IntegerField(label='Cantidad',initial=1)
    class Meta:
        model=RelCongresoUser
        fields=['user','congreso','categoria_pago','is_pagado','cantidad']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

        self.fields['user'].widget.attrs.update({'class': 'select2 form-control'}) 
        self.fields['congreso'].widget.attrs.update({'class': 'select2 form-control'}) 
        self.fields['categoria_pago'].widget.attrs.update({'class': 'form-control','rows':'3'})   
        self.fields['is_pagado'].widget.attrs.update({'class': 'form-control'})   
        self.fields['cantidad'].widget.attrs.update({'class': 'form-control'})  
    def clean(self, *args, **kwargs):
        cleaned_data = super(AsignarCongresoForms, self).clean(*args, **kwargs)
        congreso = cleaned_data.get('congreso', None)
        cantidad = cleaned_data.get('cantidad', None)
        user = cleaned_data.get('user', None)
       
       
        if not congreso:
            self.add_error('congreso', 'No existe ese Congreso')

        if not user:
            self.add_error('user', 'No existe ese Usuario')
        if cantidad<0:
            self.add_error('cantidad', 'El Campo CANTIDAD debe tener un valor positivo')

class AsignarConstanciaUserForms(forms.ModelForm):
    
    foto_constancia=forms.FileField(required=False)
    class Meta:
        model=RelCongresoUser
        fields=['foto_constancia']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

    def clean(self, *args, **kwargs):
        cleaned_data = super(AsignarConstanciaUserForms, self).clean(*args, **kwargs)
        constancia = cleaned_data.get('foto_constancia', None)
        if constancia:
            filename = constancia.name
            if not filename.endswith(".pdf")  :
                self.add_error('foto_constancia',"No está <b> permitido </b> subir ese <b>tipo de archivo</b>. Es solo PDF"  )
        else:
            self.add_error('foto_constancia',"Debe subir un <b> PDF </b>"  )
class AsignarTallerForms(forms.ModelForm):
    user=forms.ModelChoiceField(queryset=PerfilUsuario.objects.all(),label='Email del Usuario',required=True)
    categoria_pago=forms.ModelChoiceField(queryset=CategoriaPagoCongreso.objects.all(),label='Categoría de Pago')
    is_pagado=forms.BooleanField(label='Pagó el Taller')
    taller=forms.ModelChoiceField(queryset=Taller.objects.all(),label='Taller',required=True)
    class Meta:
        model=RelTallerUser
        fields=['user','taller','categoria_pago','is_pagado','cantidad']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

        self.fields['user'].widget.attrs.update({'class': 'select2 form-control'}) 
        self.fields['taller'].widget.attrs.update({'class': 'select2 form-control'}) 
        self.fields['categoria_pago'].widget.attrs.update({'class': 'form-control','rows':'3'})   
        self.fields['is_pagado'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['cantidad'].widget.attrs.update({'class': 'form-control'})  
    def clean(self, *args, **kwargs):
        cleaned_data = super(AsignarTallerForms, self).clean(*args, **kwargs)
        taller = cleaned_data.get('taller', None)
        user = cleaned_data.get('user', None)
        cantidad = cleaned_data.get('cantidad', None)

        if not taller:
            self.add_error('taller', 'No existe ese Taller')

        if not user:
            self.add_error('user', 'No existe ese Usuario')  
        if cantidad<0:
            self.add_error('cantidad', 'El Campo CANTIDAD debe tener un valor positivo')
          
class ModeradorBloqueForm(forms.ModelForm):
    moderador=forms.ModelChoiceField(queryset=Moderador.objects.all(),label='Moderador')
  
    class Meta:
        model=RelBloqueModerador
        fields=['moderador','bloque']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

        self.fields['moderador'].widget.attrs.update({'class': 'form-control select2'}) 
        self.fields['bloque'].widget.attrs.update({'class': 'form-control','style':'display:none'}) 

    def clean(self, *args, **kwargs):
        cleaned_data = super(ModeradorBloqueForm, self).clean(*args, **kwargs)
        moderador = cleaned_data.get('moderador', None)
        bloque = cleaned_data.get('bloque', None)
       
        if not moderador:
            self.add_error('moderador', 'Debe entrar un <b>Moderador</b>')

        if RelBloqueModerador.objects.filter(bloque=bloque,moderador=moderador).exists():
            self.add_error('moderador', 'Este <b>Bloque</b> ya tiene este <b>Moderador</b>')
class ImagenCongForms(forms.ModelForm):
    imagen=forms.ImageField(label='Buscar Imagen',required=False)
    update=forms.BooleanField(required=False)
    class Meta:
        model=ImagenCongreso
        fields=['imagen','congreso','update']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

        self.fields['imagen'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['congreso'].widget.attrs.update({'class': 'form-control'}) 

    def clean(self, *args, **kwargs):
        cleaned_data = super(ImagenCongForms, self).clean(*args, **kwargs)
        imagen = cleaned_data.get('imagen', None)
        update = cleaned_data.get('updates', None)
        if imagen:
            w, h = get_image_dimensions(imagen)
            if w != 1920 or h != 1080:
                self.add_error('imagen',"Esta imagen tiene %s X %s pixel. Debe ser de 1920 X 1080 pixel" %(w,h) )
        else:
            if not update:
                self.add_error('imagen',"Este campo es obligatorio mio" )
class PreguntaForm(forms.ModelForm):
    congreso=forms.ModelChoiceField(queryset=Congreso.objects.all(),label='Congreso')
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

class MetaPagListarForm(forms.ModelForm):

    class Meta:
        model=MetaPagListCongreso
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
    published=forms.BooleanField(label='Publicado',required=False)
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
    
    congreso=forms.ModelChoiceField(queryset=Congreso.objects.all(),label='Filtrar Congreso',required=True)

    class Meta:
        model=RelCongresoUser
        fields=['congreso']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

        self.fields['congreso'].widget.attrs.update({'class': 'form-control select2'}) 
       
    # def clean(self, *args, **kwargs):
    #     cleaned_data = super(ExportarExelForm, self).clean(*args, **kwargs)
    #     congreso = cleaned_data.get('congreso', None)
      
    #     if not congreso:
    #         self.add_error('congreso','Entre un congreso ')
    #     if not RelCongresoUser.objects.filter(congreso=congreso).values('user__usuario__first_name','user__usuario__last_name','user__usuario__email','congreso__titulo','categoria_pago__nombre').annotate(Sum('cantidad')).exists():
    #         self.add_error('congreso','Entre un congreso ')

class ExportarTallerExelForm(forms.ModelForm):
    
    taller=forms.ModelChoiceField(queryset=Taller.objects.all(),label='Filtrar Congreso',required=True)

    class Meta:
        model=RelTallerUser
        fields=['taller']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

        self.fields['taller'].widget.attrs.update({'class': 'form-control select2'}) 
       
    # def clean(self, *args, **kwargs):
    #     cleaned_data = super(ExportarTallerExelForm, self).clean(*args, **kwargs)
    #     taller = cleaned_data.get('taller', None)
    #     if not taller:
        
    #         self.add_error('taller','Entre un taller ')

class CongresoPatrocinadorForm(forms.ModelForm):
    
    aval=forms.ModelChoiceField(queryset=AvalCongreso.objects.all(),required=False)
    class Meta:
        model=RelCongresoAval
        fields=['congreso','aval']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

        self.fields['congreso'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['aval'].widget.attrs.update({'class': 'select2 form-control'}) 
      
    def clean(self, *args, **kwargs):
        cleaned_data = super(CongresoPatrocinadorForm, self).clean(*args, **kwargs)
        aval = cleaned_data.get('aval', None)
        congreso = cleaned_data.get('congreso', None)
       
        if not aval:
            self.add_error('aval', 'Debe entrar un Patrocinador')

        if RelCongresoAval.objects.filter(congreso=congreso,aval=aval).exists():
            self.add_error('aval', 'Este Patrocinador ya esta asociado a este Congreso')


class CongresoSocioForm(forms.ModelForm):
    
    socio=forms.ModelChoiceField(queryset=SocioCongreso.objects.all(),required=True)
    class Meta:
        model=RelCongresoSocio
        fields=['congreso','socio']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

        self.fields['congreso'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['socio'].widget.attrs.update({'class': 'select2 form-control'}) 
      
    def clean(self, *args, **kwargs):
        cleaned_data = super(CongresoSocioForm, self).clean(*args, **kwargs)
        socio = cleaned_data.get('socio', None)
        congreso = cleaned_data.get('congreso', None)
       
        if not socio:
            self.add_error('socio', 'Debe entrar un Socio')

        if RelCongresoSocio.objects.filter(congreso=congreso,socio=socio).exists():
            self.add_error('socio', 'Este Socio ya esta asociado a este congreso')


class SelectPonencia(forms.Form):
    ponencia=forms.ModelChoiceField(queryset=Ponencia.objects.all(),required=False)
    def __init__(self, *args, **kwargs):
        self.path = kwargs.pop('path', None)
        super().__init__(*args, **kwargs) 
        bloque=Bloque.objects.filter(path=self.path).first()
        ponencia=forms.ModelChoiceField(queryset=Ponencia.objects.filter(congreso=bloque.congreso))
        self.fields['ponencia'].widget.attrs.update({'class': 'form-control'}) 
    
    def clean(self, *args, **kwargs):
        cleaned_data = super(SelectPonencia, self).clean(*args, **kwargs)
        ponencia_titulo = cleaned_data.get('ponencia', None)
        if not ponencia_titulo:
            self.add_error('ponencia', 'Deb entrar una <b>Ponencia</b>')
        else:
            bloque=Bloque.objects.filter(path=self.path).first()
            ponencia=Ponencia.objects.filter(titulo=ponencia_titulo).first()
            if ponencia.bloque==bloque:
                self.add_error('ponencia', 'Esta <b>Ponencia</b> ya está en este <b> bloque</b>')
                return
            if ponencia.fecha_inicio.date() != bloque.fecha_inicio.date():
                self.add_error('ponencia', 'Esta <b>Ponencia</b> no tiene la misma <b>fecha de inicio que este Bloque</b>')

        # if RelCongresoSocio.objects.filter(congreso=congreso,socio=socio).exists():
        #     self.add_error('socio', 'Este Socio ya esta asociado a este congreso')

class CongresoProgramaForm(forms.ModelForm):
    idioma=forms.ModelChoiceField(queryset=Idioma.objects.all(),label='Idioma')
    
    class Meta:
        model=DocumentoPrograma
        fields=['idioma','congreso','documento','texto']
       

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

        self.fields['idioma'].widget.attrs.update({'class': 'form-control select2'}) 
        self.fields['congreso'].widget.attrs.update({'class': 'form-control','style':'display:none'}) 
        self.fields['texto'].widget.attrs.update({'class': 'form-control'}) 
        
        
    def clean(self, *args, **kwargs):
        cleaned_data = super(CongresoProgramaForm, self).clean(*args, **kwargs)
        documento = cleaned_data.get('documento', None)
        if documento:
            filename = documento.name
            
            if(not filename.endswith(".doc") and not filename.endswith(".docx") and
                not filename.endswith(".pdf") and not filename.endswith(".zip") and
                not filename.endswith(".rar") ) :
                self.add_error('documento',"No está <b> permitido </b> subir ese <b>tipo de archivo</b>. Los permitidos son <b>  .doc, .docx, .pdf, .rar, .zip </b>."  )

class CongresoTrabajoForm(forms.ModelForm):
    titulo=forms.CharField(label='Título',required=True)
    
    class Meta:
        model=TrabajosInvestigacion
        fields=['titulo','congreso','documento','descripcion','autor','cod_video','foto']
       

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

        self.fields['descripcion'].widget.attrs.update({'class': 'form-control ckeditor'}) 
        self.fields['congreso'].widget.attrs.update({'class': 'form-control','style':'display:none'}) 
        self.fields['titulo'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['autor'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['cod_video'].widget.attrs.update({'class': 'form-control','rows':'7'}) 
        
    def clean(self, *args, **kwargs):
        cleaned_data = super(CongresoTrabajoForm, self).clean(*args, **kwargs)
        documento = cleaned_data.get('documento', None)
        if documento:
            filename = documento.name
            
            if(not filename.endswith(".doc") and not filename.endswith(".docx") and
                not filename.endswith(".pdf") and not filename.endswith(".zip") and
                not filename.endswith(".rar") ) :
                self.add_error('documento',"En el Campo <b> Documento </b> no está <b> permitido </b> subir ese <b>tipo de archivo</b>. Los permitidos son <b>  .doc, .docx, .pdf, .rar, .zip </b>."  )
