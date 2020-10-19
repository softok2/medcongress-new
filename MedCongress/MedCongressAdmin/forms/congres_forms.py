from django import forms
from  MedCongressApp.models import (Congreso,Ubicacion,ImagenCongreso,TipoCongreso,Ponencia,Taller,
                                    Ponente,PerfilUsuario,RelPonenciaPonente,RelCongresoCategoriaPago,
                                    CategoriaPagoCongreso,RelTalleresCategoriaPago)
from django.contrib.auth.models import Group, User
from betterforms.multiform import MultiModelForm

        
class CongresForm(forms.ModelForm):
    imagen_seg=forms.ImageField(label='Buscar Imagen',required=False)
    titulo=forms.CharField(label='Título')
    sub_titulo=forms.CharField(label='Título segundario',required=False) 
    t_congreso=forms.ModelChoiceField(queryset=TipoCongreso.objects.all(),label='Tipo de Congreso')
    fecha_inicio=forms.DateTimeField(widget=forms.TextInput())
    class Meta:
        model=Congreso
        fields=['titulo','sub_titulo','imagen_seg','fecha_inicio','published','t_congreso','especialidad']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

        self.fields['titulo'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['sub_titulo'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['imagen_seg'].widget.attrs.update({'class': ' form-control '}) 
        self.fields['fecha_inicio'].widget.attrs.update({'class': 'form-control'})   
        self.fields['published'].widget.attrs.update({'class': 'form-control'})   
        self.fields['t_congreso'].widget.attrs.update({'class': 'form-control'})  
        self.fields['especialidad'].widget.attrs.update({'class': 'form-control'})     

    # def clean(self, *args, **kwargs):
    #     cleaned_data = super(UserForm, self).clean(*args, **kwargs)
    #     password = cleaned_data.get('password', None)
    #     password1 = cleaned_data.get('password1', None)
    #     if password!=password1 :
    #         self.add_error('password1', 'No coinciden los password ')

# class PerfilUserForm(forms.ModelForm):
#     cel_profecional=forms.CharField(
#                label = 'Célula Profecional',
#                 required=False
#                )
#     is_ponente=forms.BooleanField(
#                 label = 'Desearía ser ponente en un evento   ',
#                 required=False
               
#                )
#     categoria=forms.ModelChoiceField(queryset=CategoriaUsuario.objects.filter(published=True))
   
#     class Meta:
#         model=PerfilUsuario
#         fields=['cel_profecional','categoria','genero','especialidad','is_ponente']
        
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
         
#         self.fields['cel_profecional'].widget.attrs.update({'class': 'form-control'})   
#         self.fields['categoria'].widget.attrs.update({'class': 'form-control'}) 
#         self.fields['genero'].widget.attrs.update({'class': 'form-control'}) 
       
class ImagenCongresoForms(forms.ModelForm):
    imagen=forms.ImageField(required=False)
    class Meta:
        model=ImagenCongreso
        fields=['imagen']       
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['imagen'].widget.attrs.update({'class': 'form-control'}) 

class Ubicacion(forms.ModelForm):
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
        cleaned_data = super(Ubicacion, self).clean(*args, **kwargs)
        longitud = cleaned_data.get('longitud', None)
        latitud = cleaned_data.get('latitud', None)
        if longitud is None :
            self.add_error('direccion', 'Debe seleccionar una dirección')
    

# class Categoria(forms.ModelForm):

#     nombre= forms.CharField(
#         label='Nueva Categoría',
#         required=False
#     )

#     class Meta:
#         model=CategoriaUsuario
#         fields=['nombre']
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
        
#         self.fields['nombre'].widget.attrs.update({'class': 'form-control'}) 
       



class CongresoForms(MultiModelForm):
    form_classes = {
        'congreso': CongresForm,
        'ubicacion':Ubicacion,
        'imagen_congreso':ImagenCongresoForms
    }

    


class PonenciaForm(forms.ModelForm):
    imagen=forms.ImageField(label='Buscar Imagen',required=False)
    titulo=forms.CharField(label='Título')
    cod_video=forms.CharField(label='Código del video en Vimeo',required=False)
    fecha_inicio=forms.DateTimeField()
   
    class Meta:
        model=Ponencia
        fields=['titulo','duracion','detalle','fecha_inicio','imagen','published','cod_video','congreso']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

        self.fields['titulo'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['duracion'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['congreso'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['fecha_inicio'].widget.attrs.update({'class': 'form-control'})   
        self.fields['published'].widget.attrs.update({'class': 'form-control'})   
        self.fields['cod_video'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['detalle'].widget.attrs.update({'class': 'form-control','rows':'3'})  

class TallerForm(forms.ModelForm):
    imagen=forms.ImageField(label='Buscar Imagen',required=False)
    titulo=forms.CharField(label='Título')
    fecha_inicio=forms.DateTimeField()
    class Meta:
        model=Taller
        fields=['titulo','duracion','fecha_inicio','imagen','published','congreso']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

        self.fields['titulo'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['duracion'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['congreso'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['fecha_inicio'].widget.attrs.update({'class': 'form-control'})   
        self.fields['published'].widget.attrs.update({'class': 'form-control'})   
        

class PonenciaForms(MultiModelForm):
    form_classes = {
        'ponencia': PonenciaForm,
        'ubicacion':Ubicacion,
        
    }
class TallerForms(MultiModelForm):
    form_classes = {
        'taller': TallerForm,
        'ubicacion':Ubicacion,
        
    }

class PonenteForm(forms.ModelForm):
    user=forms.ModelChoiceField(queryset=PerfilUsuario.objects.all(),label='Usuario')
    class Meta:
        model=Ponente
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

#    categoria = models.ForeignKey(CategoriaPagoCongreso, on_delete=models.CASCADE)
#     congreso = models.ForeignKey(Congreso, on_delete=models.CASCADE)
#     precio=models.FloatField()
#     moneda=models.CharField(max_length=3)

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