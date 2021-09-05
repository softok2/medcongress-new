from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.core.validators import RegexValidator
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db import models
from django.core.exceptions import NON_FIELD_ERRORS


# Create your models here.

##### Tabla Categoria del usuario  ###

class CategoriaUsuario(models.Model):
    nombre=models.CharField(max_length=50,error_messages={
"max_length": "El Campo <b>Nombre</b> debe tener máximo 50 caracteres"},validators=[
            RegexValidator(regex=r"^[\w.,+\- ]+$", message="El Campo <b> Nombre </b> solo admite números, letras y (.,+-)" )
        ],)
    published=models.BooleanField(null=True)
    detalle=models.TextField(null=True,blank=True)

    class Meta:
        verbose_name='categoria del usuario'
        verbose_name_plural='categorias del usuario'

    def __str__(self):
        return self.nombre


##### Tabla Especialidades  ###

class Especialidades(models.Model):
    nombre=models.CharField(max_length=50,unique=True,error_messages={
"max_length": "El Campo <b>Nombre</b> debe tener máximo 50 caracteres"},validators=[
            RegexValidator(regex=r"^[\w.,+\- ]+$", message="El Campo <b> Nombre </b> solo admite números, letras y (.,+-)" )
        ],)
    detalle=models.TextField(null=True,blank=True)

    class Meta:
        verbose_name='especialidad del usuario'
        verbose_name_plural='especialidades del usuario'

    def __str__(self):
        return self.nombre

##### Tabla País #####

class Pais(models.Model):
    denominacion = models.CharField(unique=True, max_length=50,error_messages={
"max_length": "El Campo <b>Denominación</b> debe tener máximo 50 caracteres"},validators=[
            RegexValidator(regex=r"^[\w.,+\- ]+$", message="El Campo <b> País </b> solo admite números, letras y (.,+-)" )
        ],)
    banderas=models.ImageField(storage= FileSystemStorage( location='MedCongressApp/static/'),upload_to='banderas',blank=True, null=True )

    class Meta:
        verbose_name = 'pais'
        verbose_name_plural = 'paises'

    def __str__(self):
        return self.denominacion

##### Tabla Género #####

class Genero(models.Model):
    denominacion= models.CharField(max_length=20,unique=True,error_messages={
"max_length": "El Campo <b>Denominación</b> debe tener máximo 20 caracteres"},validators=[
            RegexValidator(regex=r"^[\w.,+\- ]+$", message="El Campo <b> Género </b> solo admite números, letras y (.,+-)")
        ],)

    class Meta:
        verbose_name='genero'
        verbose_name_plural='generos'
        
    def __str__(self):
        return self.denominacion

##### Tabla Ubicacion #####

class Ubicacion(models.Model):
    direccion= models.CharField(max_length=250,error_messages={
"max_length": "El Campo <b>Dirección</b> debe tener máximo 250 caracteres"})
    latitud=models.FloatField()
    longitud=models.FloatField()

    class Meta:
        verbose_name='ubicacion'
        verbose_name_plural='ubicaciones'
        
    def __str__(self):
        return self.direccion   


## cargar valores por defecto en genero##


#####  Tabla Perfil Usuario (otros datos de interes del Usuario)

class PerfilUsuario(models.Model):
    
    id_openpay=models.CharField(max_length=20,null=True,blank=True)
    detalle=models.TextField(null=True,blank=True)
    is_ponente=models.BooleanField(blank=True, null=True)
    path=models.CharField(max_length=250, help_text='campo para identificarlo por la URL')
    cel_profecional=models.CharField(max_length=50,null=True)
    foto=models.ImageField(storage= FileSystemStorage( location='MedCongressApp/static/'),upload_to='usuarios',blank=True, null=True )
    activation_key = models.CharField(max_length=60,blank=True, null=True)
    key_expires = models.DateTimeField(blank=True, null=True)
    usuario=models.OneToOneField(User, on_delete=models.CASCADE)
    categoria=models.ForeignKey(CategoriaUsuario,on_delete=models.DO_NOTHING,null=True)
    especialidad=models.ForeignKey(Especialidades,on_delete=models.DO_NOTHING,null=True,blank=True)
    ubicacion=models.ForeignKey(Ubicacion,on_delete=models.DO_NOTHING,null=True)
    genero=models.ForeignKey(Genero,on_delete=models.DO_NOTHING,null=True)
    datos_interes=models.TextField(null=True,blank=True)
    linkedin=models.CharField(max_length=50,null=True,error_messages={
"max_length": "El Campo <b>Linkedin</b> debe tener máximo 50 caracteres"})
    facebook=models.CharField(max_length=50,null=True,error_messages={
"max_length": "El Campo <b> Facebook</b> debe tener máximo 50 caracteres"})
    twitter=models.CharField(max_length=50,null=True,error_messages={
"max_length": "El Campo <b>Twitter</b> debe tener máximo 50 caracteres"})
    youtube=models.CharField(max_length=50,null=True,error_messages={
"max_length": "El Campo <b>Youtube</b> debe tener máximo 50 caracteres"})
    publicaciones=models.TextField(null=True,blank=True)
    puesto=models.TextField(max_length=250,null=True,blank=True)
    meta_og_title=models.CharField(max_length=50,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas para FaceBook Título</b> debe tener máximo 50 caracteres"})
    meta_description=models.TextField(max_length=160,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas Principales Descripción</b> debe tener máximo 160 caracteres"})
    meta_og_description=models.TextField(max_length=160,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas para FaceBook Descripción</b> debe tener máximo 160 caracteres"})
    meta_og_type=models.CharField(max_length=50,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas para FaceBook Tipo</b> debe tener máximo 50 caracteres"})
    meta_og_url=models.CharField(max_length=250,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas para FaceBook URL</b> debe tener máximo 250 caracteres"})
    meta_twitter_card=models.CharField(max_length=50,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas para Redes Sociales Card</b> debe tener máximo 50 caracteres"})
    meta_twitter_site=models.CharField(max_length=250,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas para Redes Sociales Sitio</b> debe tener máximo 250 caracteres"})
    meta_twitter_creator=models.CharField(max_length=50,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas para Redes Sociales Creador</b> debe tener máximo 50 caracteres"})
    meta_keywords=models.TextField(max_length=250,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas Principales Palabras Claves </b> debe tener máximo 250 caracteres"})
    meta_og_imagen=models.ImageField(storage= FileSystemStorage( location='MedCongressApp/static/'),upload_to='metas',blank=True, null=True )
    meta_title=models.CharField(max_length=50,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas Principales Título </b> debe tener máximo 50 caracteres"})
    score=models.IntegerField(null=True)
    fecha_nacimiento=models.DateField(null=True)
    num_telefono=models.CharField(max_length=20,null=True,validators=[
            RegexValidator(regex=r"^[0-9()+-]+$", message="Entre un No. de <b>Teléfono</b> correcto. Ej. <b>(+99)999-999-999</b>")
        ],)
    class Meta:
        verbose_name='Perfil usuario'
        verbose_name_plural='Perfil de usuarios'

    def __str__(self):
        return '%s %s <%s>'%( self.usuario.first_name,self.usuario.last_name,self.usuario.email)

    def is_openpay(self):
        if self.id_openpay :
            return True
        else:
            return False
    

#### Tabla Tipo de Congresos que hay ######

class TipoCongreso(models.Model):
    nombre=models.CharField(max_length=50,unique=True,error_messages={
"max_length": "El Campo <b>Nombre</b> debe tener máximo 50 caracteres"})
    detalle=models.TextField(null=True,blank=True)

    class Meta:
        verbose_name='tipo de congreso'
        verbose_name_plural='tipos de congresos'

    def __str__(self):
        return self.nombre

#### Tabla Especialidad de Congresos que hay ######

class EspecialidadCongreso(models.Model):
    nombre=models.CharField(max_length=50,unique=True,error_messages={
"max_length": "El Campo <b>Nombre</b> debe tener máximo 50 caracteres"},validators=[
            RegexValidator(regex=r"^[\w.,+\- ]+$", message="El Campo <b> Nombre </b> solo admite números, letras y (.,+-)")
        ],)
    detalle=models.TextField(null=True,blank=True)

    class Meta:
        verbose_name='especialidad del congreso'
        verbose_name_plural='especialidades de los congresos'

    def __str__(self):
        return self.nombre



#### Tabla Aval de Congresos que hay ######

class AvalCongreso(models.Model):
    nombre=models.CharField(max_length=50,unique=True,error_messages={
"max_length": "El Campo <b>Nombre</b> debe tener máximo 50 caracteres","unique":"Ya existe un <b> Patrocinador</b> con este <b>Nombre</b>"})
    detalle=models.TextField(null=True,blank=True)
    logo=models.ImageField(storage= FileSystemStorage( location='MedCongressApp/static/'),upload_to='patrocinadores' )
    url= models.URLField(max_length=250,error_messages={
"max_length": "El Campo <b>URL</b> debe tener máximo 250 caracteres"})

    class Meta:
        verbose_name='aval del congreso'
        verbose_name_plural='avales de los congresos'

    def __str__(self):
        return self.nombre

    #### Tabla Socio de Congresos que hay ######

class SocioCongreso(models.Model):
    nombre=models.CharField(max_length=50,unique=True,error_messages={
"max_length": "El Campo <b>Nombre</b> debe tener máximo 50 caracteres","unique":"Ya existe un <b> Patrocinador</b> con este <b>Nombre</b>"})
    detalle=models.TextField(null=True,blank=True)
    logo=models.ImageField(storage= FileSystemStorage( location='MedCongressApp/static/'),upload_to='socios' )
    url= models.URLField(max_length=250,error_messages={
"max_length": "El Campo <b>URL</b> debe tener máximo 250 caracteres"})

    class Meta:
        verbose_name='socio del congreso'
        verbose_name_plural='socios de los congresos'

    def __str__(self):
        return self.nombre

#### Tabla Categorias de Pago para Congresos ######

class CategoriaPagoCongreso(models.Model):
    nombre=models.CharField(max_length=50,unique=True,error_messages={
"max_length": "El Campo <b>Nombre</b> debe tener máximo 50 caracteres"},validators=[
            RegexValidator(regex=r"^[\w.,+\- ]+$", message="El Campo <b> Nombre </b> solo admite números, letras y (.,+-)" )
        ],)
    path=models.CharField(max_length=250, help_text='campo para identificarlo por la URL')
    detalle=models.TextField(null=True,blank=True)

    class Meta:
        verbose_name='categoria de pago del congreso'
        verbose_name_plural='categorias de pago para los congresos'

    def __str__(self):
        return self.nombre

#### Tabla Congresos #######

class Congreso(models.Model):
    titulo=models.CharField(max_length=250,unique=True,error_messages={
"max_length": "El Campo <b>Título</b> debe tener máximo 250 caracteres"})
    sub_titulo=models.CharField(max_length=250,null=True, error_messages={
"max_length": "El Campo <b>SubTítulo</b> debe tener máximo 250 caracteres"})
    imagen_seg=models.ImageField(storage= FileSystemStorage( location='MedCongressApp/static/'),upload_to='congreso',error_messages={
"blank": 'Debe  entrar una <b> Imagen Segundaria </b>'})
    imagen_home=models.ImageField(storage= FileSystemStorage( location='MedCongressApp/static/'),upload_to='congreso',error_messages={
"blank": 'Debe  entrar una <b> Imagen Segundaria </b>'},null=True, blank=True)
    path=models.CharField(max_length=250, help_text='campo para identificarlo por la URL',unique=True)
    lugar=models.ForeignKey(Ubicacion,on_delete=models.DO_NOTHING)
    fecha_inicio=models.DateTimeField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(null=True, blank=True)
    published=models.BooleanField(null=True, blank=True)
    is_home=models.BooleanField()
    t_congreso=models.ForeignKey(TipoCongreso,on_delete=models.DO_NOTHING)
    especialidad=models.ForeignKey(EspecialidadCongreso,on_delete=models.DO_NOTHING,null=True)
    user = models.ManyToManyField(PerfilUsuario, through='RelCongresoUser',related_name='congreso_perfilusuario')
    aval = models.ManyToManyField(AvalCongreso, through='RelCongresoAval',related_name='congreso_patrosinador')
    categoria_pago = models.ManyToManyField(CategoriaPagoCongreso, through='RelCongresoCategoriaPago',related_name='congreso_cat_pago')
    is_openpay=models.BooleanField(null=True)
    template=models.CharField(max_length=50,null=True)
    meta_og_title=models.CharField(max_length=50,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas para FaceBook Título</b> debe tener máximo 50 caracteres"})
    meta_description=models.TextField(max_length=160,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas Principales Descripción</b> debe tener máximo 160 caracteres"})
    meta_og_description=models.TextField(max_length=160,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas para FaceBook Descripción</b> debe tener máximo 160 caracteres"})
    meta_og_type=models.CharField(max_length=50,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas para FaceBook Tipo</b> debe tener máximo 50 caracteres"})
    meta_og_url=models.CharField(max_length=250,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas para FaceBook URL</b> debe tener máximo 250 caracteres"})
    meta_twitter_card=models.CharField(max_length=50,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas para Redes Sociales Card</b> debe tener máximo 50 caracteres"})
    meta_twitter_site=models.CharField(max_length=250,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas para Redes Sociales Sitio</b> debe tener máximo 250 caracteres"})
    meta_twitter_creator=models.CharField(max_length=50,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas para Redes Sociales Creador</b> debe tener máximo 50 caracteres"})
    meta_keywords=models.TextField(max_length=250,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas Principales Palabras Claves </b> debe tener máximo 250 caracteres"})
    meta_og_imagen=models.ImageField(storage= FileSystemStorage( location='MedCongressApp/static/'),upload_to='metas',blank=True, null=True )
    meta_title=models.CharField(max_length=50,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas Principales Título </b> debe tener máximo 50 caracteres"})
    foto_constancia=models.FileField(storage= FileSystemStorage( location='MedCongressApp/static/congreso/img_constancia'),null=True)
    foto_const_ponente=models.FileField(storage= FileSystemStorage( location='MedCongressApp/static/congreso/img_constancia'),null=True)
    foto_const_moderador=models.FileField(storage= FileSystemStorage( location='MedCongressApp/static/congreso/img_constancia'),null=True)
    aprobado=models.IntegerField(null=True)
    cant_preguntas=models.IntegerField(null=True)
    score=models.IntegerField(null=True)
    streaming=models.TextField(null=True,blank=True)
    vid_publicidad=models.TextField(null=True,blank=True)
    detalles_tipo_boleto=models.TextField(null=True,blank=True)
    detalles_tipo_boleto_taller=models.TextField(null=True,blank=True)
    ver_titulo=models.BooleanField(default=True)

    class Meta:
        verbose_name='congreso'
        verbose_name_plural='congresos'

    def __str__(self):
        return self.titulo
    
    def Ponentes(self):

        ponencias=Ponencia.objects.filter(congreso=self)
        ponentes_env=[]
        for ponencia in ponencias:
            ponencia_ponentes=RelPonenciaPonente.objects.filter(ponencia=ponencia)
            for ponencia_ponente in ponencia_ponentes:
                if not ponencia_ponente.ponente in ponentes_env:
                    ponentes_env.append(ponencia_ponente.ponente)
        return ponentes_env
    
    def Moderadores(self):

        bloques=Bloque.objects.filter(congreso=self)
        moderadores_env=[]
        for bloque in bloques:
            bloque_moderadores=RelBloqueModerador.objects.filter(bloque=bloque)
            for bloque_moderadore in bloque_moderadores:
                if not bloque_moderadore.moderador in moderadores_env:
                    moderadores_env.append(bloque_moderadore.moderador)
        return moderadores_env

    # def get_imagen_by_order(self):   
    #     if self.imagen_set.count():
    #         return self.downloaditemsample_set.order_by('order')[0]

##### Tabla Imagenes congreso #####

class ImagenCongreso(models.Model):
    imagen=models.ImageField(storage= FileSystemStorage( location='MedCongressApp/static/'),upload_to='congreso')
    congreso=models.ForeignKey(Congreso,on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name='imagen de congreso'
        verbose_name_plural='Imagenes de congreso'

    def __str__(self):
        return 'Imagen del congreso %s'%(self.congreso.titulo)

##### Tabla pivote Congreso- Usuario #####

class RelCongresoUser(models.Model):
    user = models.ForeignKey(PerfilUsuario, on_delete=models.CASCADE)
    congreso = models.ForeignKey(Congreso, on_delete=models.CASCADE)
    categoria_pago = models.ForeignKey(CategoriaPagoCongreso, on_delete=models.CASCADE,null=True)
    is_pagado=models.BooleanField(default=False)
    id_transaccion=models.CharField(max_length=20)
    num_autorizacion_transaccion=models.CharField(max_length=20)
    num_tarjeta_tranzaccion=models.CharField(max_length=16)
    created_at = models.DateTimeField(auto_now_add=True)
    cantidad=models.IntegerField(null=True)
    is_constancia=models.BooleanField(null=True)
    folio_constancia=models.CharField(null=True,max_length=250)
    fecha_constancia=models.DateField(null=True)
    cuestionario=models.CharField(null=True,max_length=250)
    foto_constancia=models.ImageField(storage= FileSystemStorage( location='MedCongressApp/static/'),upload_to='congreso/img_constancia',null=True)
    uuid_factura=models.CharField(max_length=36,null=True)
    is_beca=models.BooleanField(default=False)

    def __str__(self):
        return '%s->%s->%s'%(self.user.usuario.first_name, self.congreso.titulo, self.categoria_pago.nombre)

    class Meta:
        verbose_name='relacion congreso - usuario'
        verbose_name_plural='relaciones congreso - usuarios'
        

##### Tabla pivote Congreso- Avales #####

class RelCongresoAval(models.Model):
    aval = models.ForeignKey(AvalCongreso, on_delete=models.CASCADE)
    congreso = models.ForeignKey(Congreso, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name='relacion congreso - aval'
        verbose_name_plural='relaciones congreso - aval'
        unique_together = (('aval','congreso'),)

    def __str__(self):
        return 'Relación del congreso %s con el patrocinador %s'%(self.congreso.titulo,self.aval.nombre)

##### Tabla pivote Congreso- Socios #####

class RelCongresoSocio(models.Model):
    socio = models.ForeignKey(SocioCongreso, on_delete=models.CASCADE)
    congreso = models.ForeignKey(Congreso, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name='relacion congreso - socio'
        verbose_name_plural='relaciones congreso - socios'
        unique_together = (('socio','congreso'),)

    def __str__(self):
        return 'Relación del congreso %s con el Socio %s'%(self.congreso.titulo,self.aval.nombre)


##### Tabla pivote Congreso- Categorias de Pagos #####

class RelCongresoCategoriaPago(models.Model):
    categoria = models.ForeignKey(CategoriaPagoCongreso, on_delete=models.CASCADE)
    congreso = models.ForeignKey(Congreso, on_delete=models.CASCADE)
    precio=models.FloatField()
    moneda=models.CharField(max_length=3)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name='Relación Congreso - Categoría de Pago'
        verbose_name_plural='Relaciones Congreso - Categoría de Pago'
        unique_together = (('categoria','congreso','moneda'),)

    def unique_error_message(self, model_class, unique_check):
        if model_class == type(self) and unique_check == ('categoria', 'congreso','moneda'):
            return 'Ya existe una Categoría de pago en este congreso con ese nombre y esa moneda'
        else:
            return super(RelCongresoCategoriaPago, self).unique_error_message(model_class, unique_check)   

    def __str__(self):
        return 'Relación entre el Congreso %s y la Categoría de Pago %s'%(self.congreso.titulo , self.categoria.nombre)

##### Tabla Categoria Ponente  #####

# class CategoriaPonente(models.Model):
#     nombre=models.CharField(max_length=50)
#     path=models.CharField(max_length=250, help_text='campo para identificarlo por la URL')
#     detalle=models.TextField(null=True,blank=True)
   
#     class Meta:
#         verbose_name='categoria de ponente'
#         verbose_name_plural='categorias de los ponentes'

#     def __str__(self):
#         return 'Categoría %s'%(self.nombre)

##### Tabla  Ponente  #####

class Ponente(models.Model):
    user = models.OneToOneField(PerfilUsuario, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name='ponente'
        verbose_name_plural='ponentes'

    def __str__(self):
        return '%s %s <%s>'%(self.user.usuario.first_name,self.user.usuario.last_name,self.user.usuario.email)

##### Tabla  moderador  #####

class Moderador(models.Model):
    user = models.OneToOneField(PerfilUsuario, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name='moderador'
        verbose_name_plural='moderadores'

    def __str__(self):
        return '%s %s <%s>'%(self.user.usuario.first_name,self.user.usuario.last_name, self.user.usuario.email )

#### Tabla Bloque #######

class Bloque(models.Model):
    titulo=models.CharField(max_length=250,error_messages={
"max_length": "El Campo <b>Título </b> debe tener máximo 250 caracteres"})
    duracion=models.CharField(max_length=250,error_messages={
"max_length": "El Campo <b>Duración </b> debe tener máximo 250 caracteres"})
    detalle=models.TextField(null=True,blank=True)
    fecha_inicio=models.DateTimeField()
    path=models.CharField(max_length=250, help_text='campo para identificarlo por la URL')
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(null=True, blank=True)
    published=models.BooleanField()
    moderador = models.ManyToManyField(Moderador, through='RelBloqueModerador',related_name='bloque_moderador')
    congreso=models.ForeignKey(Congreso,on_delete=models.CASCADE)
    cod_video=models.TextField(null=True,blank=True)
    imagen=models.ImageField(storage= FileSystemStorage( location='MedCongressApp/static/'),upload_to='bloque',null=True,blank=True)
    class Meta:
        verbose_name='bloque'
        verbose_name_plural='bloques'

    def __str__(self):
        return self.titulo
    
##### Tabla pivote Bloque - moderador  #####

class RelBloqueModerador(models.Model):
    moderador = models.ForeignKey(Moderador, on_delete=models.CASCADE)
    bloque = models.ForeignKey(Bloque, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name='Relación Maderador - Bloque'
        verbose_name_plural='Relaciones moderador - bloque'
        unique_together = (('moderador','bloque'),)

    def __str__(self):
        return 'Relación entre el bloque %s  y el moderador %s ' %(self.bloque.titulo, self.moderador.user.usuario.first_name)
#### Tabla Sala #######

class Sala(models.Model):
    titulo=models.CharField(max_length=250,error_messages={
"max_length": "El Campo <b>Título </b> debe tener máximo 250 caracteres"})
    detalle=models.TextField(null=True,blank=True)
    cod_video=models.TextField(null=True,blank=True)
    color=models.CharField(max_length=10,default='#4A5966')
    congreso=models.ForeignKey(Congreso,on_delete=models.CASCADE)
    imagen=models.ImageField(storage= FileSystemStorage( location='MedCongressApp/static/'),upload_to='salas',blank=True, null=True  )
  
    path=models.CharField(max_length=250, help_text='campo para identificarlo por la URL')
    published=models.BooleanField(null=True,blank=True)
    ponencia_streamming=models.IntegerField(null=True,blank=True)
    orden=models.IntegerField(default=1)
    meta_og_title=models.CharField(max_length=50,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas para FaceBook Título</b> debe tener máximo 50 caracteres"})
    meta_description=models.TextField(max_length=160,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas Principales Descripción</b> debe tener máximo 160 caracteres"})
    meta_og_description=models.TextField(max_length=160,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas para FaceBook Descripción</b> debe tener máximo 160 caracteres"})
    meta_og_type=models.CharField(max_length=50,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas para FaceBook Tipo</b> debe tener máximo 50 caracteres"})
    meta_og_url=models.CharField(max_length=250,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas para FaceBook URL</b> debe tener máximo 250 caracteres"})
    meta_twitter_card=models.CharField(max_length=50,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas para Redes Sociales Card</b> debe tener máximo 50 caracteres"})
    meta_twitter_site=models.CharField(max_length=250,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas para Redes Sociales Sitio</b> debe tener máximo 250 caracteres"})
    meta_twitter_creator=models.CharField(max_length=50,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas para Redes Sociales Creador</b> debe tener máximo 50 caracteres"})
    meta_keywords=models.TextField(max_length=250,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas Principales Palabras Claves </b> debe tener máximo 250 caracteres"})
    meta_og_imagen=models.ImageField(storage= FileSystemStorage( location='MedCongressApp/static/'),upload_to='metas',blank=True, null=True )
    meta_title=models.CharField(max_length=50,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas Principales Título </b> debe tener máximo 50 caracteres"})
    class Meta:
        verbose_name='Sala'
        verbose_name_plural='Salas'

    def __str__(self):
        return self.titulo
#### Tabla Ponencia #######

class Ponencia(models.Model):
    titulo=models.CharField(max_length=250,error_messages={
"max_length": "El Campo <b>Título </b> debe tener máximo 250 caracteres"})
    duracion=models.CharField(max_length=250,error_messages={
"max_length": "El Campo <b>Duración </b> debe tener máximo 250 caracteres"})
    detalle=models.TextField(null=True,blank=True)
    cod_video=models.TextField(null=True,blank=True)
    id_video=models.TextField(null=True,blank=True)
    imagen=models.ImageField(storage= FileSystemStorage( location='MedCongressApp/static/'),upload_to='ponencias',blank=True, null=True  )
    fecha_inicio=models.DateTimeField()
    path=models.CharField(max_length=250, help_text='campo para identificarlo por la URL')
    lugar=models.ForeignKey(Ubicacion,on_delete=models.DO_NOTHING)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(null=True, blank=True)
    published=models.BooleanField()
    congreso=models.ForeignKey(Congreso,on_delete=models.CASCADE)
    bloque=models.ForeignKey(Bloque,on_delete=models.CASCADE,null=True,blank=True)
    sala=models.ForeignKey(Sala,on_delete=models.CASCADE,null=True,blank=True)
    ponente = models.ManyToManyField(Ponente, through='RelPonenciaPonente',related_name='ponencia_ponente')
    votacion = models.ManyToManyField(User, through='RelPonenciaVotacion')
    meta_og_title=models.CharField(max_length=50,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas para FaceBook Título</b> debe tener máximo 50 caracteres"})
    meta_description=models.TextField(max_length=160,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas Principales Descripción</b> debe tener máximo 160 caracteres"})
    meta_og_description=models.TextField(max_length=160,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas para FaceBook Descripción</b> debe tener máximo 160 caracteres"})
    meta_og_type=models.CharField(max_length=50,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas para FaceBook Tipo</b> debe tener máximo 50 caracteres"})
    meta_og_url=models.CharField(max_length=250,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas para FaceBook URL</b> debe tener máximo 250 caracteres"})
    meta_twitter_card=models.CharField(max_length=50,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas para Redes Sociales Card</b> debe tener máximo 50 caracteres"})
    meta_twitter_site=models.CharField(max_length=250,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas para Redes Sociales Sitio</b> debe tener máximo 250 caracteres"})
    meta_twitter_creator=models.CharField(max_length=50,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas para Redes Sociales Creador</b> debe tener máximo 50 caracteres"})
    meta_keywords=models.TextField(max_length=250,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas Principales Palabras Claves </b> debe tener máximo 250 caracteres"})
    meta_og_imagen=models.ImageField(storage= FileSystemStorage( location='MedCongressApp/static/'),upload_to='metas',blank=True, null=True )
    meta_title=models.CharField(max_length=50,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas Principales Título </b> debe tener máximo 50 caracteres"})
    is_info=models.BooleanField(null=True)
    
    class Meta:
        verbose_name='ponencia'
        verbose_name_plural='ponencias'

    def __str__(self):
        return self.titulo

    def iniciada(self):
        now=timezone.now()
        if self.fecha_inicio > now:
            return True
        else:
            return False

##### Tabla pivote Ponencia - Ponente  #####

class RelPonenciaPonente(models.Model):
    ponente = models.ForeignKey(Ponente, on_delete=models.CASCADE)
    ponencia = models.ForeignKey(Ponencia, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name='Relación Ponente- Ponencia'
        verbose_name_plural='Relaciones Ponente - Ponencia'
        unique_together = (('ponencia','ponente'),)

    def __str__(self):
        return 'Relación entre la ponencia %s  y el ponente %s ' %(self.ponencia.titulo, self.ponente.user.usuario.first_name)

##### Tabla pivote Ponencia - Votacion  #####

class RelPonenciaVotacion(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    ponencia = models.ForeignKey(Ponencia, on_delete=models.CASCADE)
    votacion=models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name='votación ponencia - usuario'
        verbose_name_plural='votaciones ponencia - usuario'
        unique_together = (('user','ponencia'),)

    def __str__(self):
        return ' Votación de la ponencia %s por el usuario %s' %(self.ponencia.titulo, self.user.first_name)


#### Tabla Taller #######

class Taller(models.Model):
    titulo=models.CharField(max_length=250,error_messages={
"max_length": "El Campo <b>Título </b> debe tener máximo 250 caracteres"})
    duracion=models.CharField(max_length=250,error_messages={
"max_length": "El Campo <b>Duración </b> debe tener máximo 250 caracteres"}) 
    fecha_inicio=models.DateTimeField()
    cod_video=models.TextField(null=True,blank=True)
    id_video=models.TextField(null=True,blank=True)
    detalle=models.TextField(null=True,blank=True)
    path=models.CharField(max_length=250, help_text='campo para identificarlo por la URL')
    imagen=models.ImageField(storage= FileSystemStorage( location='MedCongressApp/static/'),upload_to='talleres',blank=True, null=True )
    lugar=models.ForeignKey(Ubicacion,on_delete=models.DO_NOTHING)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(null=True, blank=True)
    published=models.BooleanField()
    congreso=models.ForeignKey(Congreso,on_delete=models.CASCADE)
    bloque=models.ForeignKey(Bloque,on_delete=models.CASCADE,null=True,blank=True)
    ponente = models.ManyToManyField(Ponente, through='RelTallerPonente',related_name='taller_ponente')
    votacion = models.ManyToManyField(User, through='RelTallerVotacion')
    categoria_pago = models.ManyToManyField(CategoriaPagoCongreso, through='RelTalleresCategoriaPago',related_name='talleres_cat_pago')
    meta_og_title=models.CharField(max_length=50,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas para FaceBook Título</b> debe tener máximo 50 caracteres"})
    meta_description=models.TextField(max_length=160,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas Principales Descripción</b> debe tener máximo 160 caracteres"})
    meta_og_description=models.TextField(max_length=160,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas para FaceBook Descripción</b> debe tener máximo 160 caracteres"})
    meta_og_type=models.CharField(max_length=50,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas para FaceBook Tipo</b> debe tener máximo 50 caracteres"})
    meta_og_url=models.CharField(max_length=250,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas para FaceBook URL</b> debe tener máximo 250 caracteres"})
    meta_twitter_card=models.CharField(max_length=50,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas para Redes Sociales Card</b> debe tener máximo 50 caracteres"})
    meta_twitter_site=models.CharField(max_length=250,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas para Redes Sociales Sitio</b> debe tener máximo 250 caracteres"})
    meta_twitter_creator=models.CharField(max_length=50,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas para Redes Sociales Creador</b> debe tener máximo 50 caracteres"})
    meta_keywords=models.TextField(max_length=250,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas Principales Palabras Claves </b> debe tener máximo 250 caracteres"})
    meta_og_imagen=models.ImageField(storage= FileSystemStorage( location='MedCongressApp/static/'),upload_to='metas',blank=True, null=True )
    meta_title=models.CharField(max_length=50,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas Principales Título </b> debe tener máximo 50 caracteres"})
    foto_constancia=models.ImageField(storage= FileSystemStorage( location='MedCongressApp/static/'),upload_to='congreso/img_constancia',null=True)
    score=models.IntegerField(null=True)
    class Meta:
        verbose_name='taller'
        verbose_name_plural='talleres'

    def __str__(self):
        return self.titulo
        
    def iniciada(self):
        now=timezone.now()
        if self.fecha_inicio > now:
            return True
        else:
            return False

##### Tabla pivote Taller - Ponente  #####

class RelTallerPonente(models.Model):
    ponente = models.ForeignKey(Ponente, on_delete=models.CASCADE)
    taller = models.ForeignKey(Taller, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name='Relación Ponente- Taller'
        verbose_name_plural='Relaciones Ponente - Taller'
        unique_together = (('ponente','taller'),)

    def __str__(self):
        return 'Relación entre la taller %s  y el ponente %s ' %(self.taller.titulo, self.ponente.user.usuario.first_name)

##### Tabla pivote Taller - Votacion  #####

class RelTallerVotacion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    taller = models.ForeignKey(Taller, on_delete=models.CASCADE)
    votacion=models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name='votación taller - usuario'
        verbose_name_plural='votaciones taller - usuario'
        unique_together = (('user','taller'),)


    def __str__(self):
        return ' Votación del taller %s por el usuario %s' %(self.taller.titulo, self.user.first_name)

##### Tabla pivote Talleres - Categorias de Pagos #####

class RelTalleresCategoriaPago(models.Model):
    categoria = models.ForeignKey(CategoriaPagoCongreso, on_delete=models.CASCADE)
    taller = models.ForeignKey(Taller, on_delete=models.CASCADE)
    precio=models.FloatField()
    moneda=models.CharField(max_length=3)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name='Relación Taller - Categoría de Pago'
        verbose_name_plural='Relaciones Talleres - Categoría de Pago'
        unique_together = (('categoria','taller','moneda'),)

    def __str__(self):
        return 'Relación entre el Taller %s y la Categoría de Pago %s'%(self.taller.titulo , self.categoria.nombre)

    def unique_error_message(self, model_class, unique_check):
        if model_class == type(self) and unique_check == ('categoria', 'taller','moneda'):
            return 'Ya existe una Categoría de pago en este taller con ese nombre y esa moneda'
        else:
            return super(RelTalleresCategoriaPagos, self).unique_error_message(model_class, unique_check)   

##### Tabla pivote Taller - Usuario #####

class RelTallerUser(models.Model):
    user = models.ForeignKey(PerfilUsuario, on_delete=models.CASCADE)
    taller = models.ForeignKey(Taller, on_delete=models.CASCADE)
    categoria_pago = models.ForeignKey(CategoriaPagoCongreso, on_delete=models.CASCADE)
    is_pagado=models.BooleanField(default=False)
    id_transaccion=models.CharField(max_length=20)
    num_autorizacion_transaccion=models.CharField(max_length=20)
    num_tarjeta_tranzaccion=models.CharField(max_length=16)
    created_at = models.DateTimeField(auto_now_add=True)
    cantidad=models.IntegerField(null=True)
    uuid_factura=models.CharField(max_length=36,null=True)
    is_constancia=models.BooleanField(null=True)
    fecha_constancia=models.DateField(null=True)
    foto_constancia=models.ImageField(storage= FileSystemStorage( location='MedCongressApp/static/'),upload_to='congreso/img_constancia',null=True)


    def __str__(self):
        return '%s->%s->%s'%(self.user.usuario.first_name, self.taller.titulo, self.categoria_pago.nombre)

    class Meta:
        verbose_name='Relación Taller - usuario'
        verbose_name_plural='Relaciones Talleres - usuarios'
        

##### Tabla Datos Iniciales#####

class DatosIniciales(models.Model):
    ponentes= models.IntegerField(null=True,default=0)
    ponencias= models.IntegerField(null=True,default=0)
    eventos= models.IntegerField(null=True,default=0)
    paises= models.IntegerField(null=True,default=0)
    especialidades= models.IntegerField(null=True,default=0)
    afiliados= models.IntegerField(null=True,default=0)
    talleres= models.IntegerField(null=True,default=0)
    aviso_privacidad=models.TextField(null=True)

##### Tabla Cuestionarios-Preguntas#####

class CuestionarioPregunta(models.Model):
    congreso=models.ForeignKey(Congreso,on_delete=models.CASCADE)
    pregunta= models.CharField(max_length=250,error_messages={
"max_length": "El Campo <b>Pregunta </b> debe tener máximo 250 caracteres"})
    published=models.BooleanField(null=True)
    def __str__(self):
        return pregunta

    class Meta:
        verbose_name='Pregunta del Cuestionario'
        verbose_name_plural='Preguntas del Cuestionario'
##### Tabla Cuestionarios-Respuestas#####

class CuestionarioRespuestas(models.Model):
    pregunta=models.ForeignKey(CuestionarioPregunta,on_delete=models.CASCADE)
    respuesta= models.CharField(max_length=250,error_messages={
"max_length": "El Campo <b>Respuesta </b> debe tener máximo 250 caracteres"})
    is_correcto=models.BooleanField()
    published=models.BooleanField(null=True)

#####  Tabla metadatos de la pagina Inicio 

class MetaPagInicio(models.Model): 
    meta_og_title=models.CharField(max_length=50,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas para FaceBook Título</b> debe tener máximo 50 caracteres"})
    meta_description=models.TextField(max_length=160,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas Principales Descripción</b> debe tener máximo 160 caracteres"})
    meta_og_description=models.TextField(max_length=160,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas para FaceBook Descripción</b> debe tener máximo 160 caracteres"})
    meta_og_type=models.CharField(max_length=50,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas para FaceBook Tipo</b> debe tener máximo 50 caracteres"})
    meta_og_url=models.CharField(max_length=250,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas para FaceBook URL</b> debe tener máximo 250 caracteres"})
    meta_twitter_card=models.CharField(max_length=50,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas para Redes Sociales Card</b> debe tener máximo 50 caracteres"})
    meta_twitter_site=models.CharField(max_length=250,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas para Redes Sociales Sitio</b> debe tener máximo 250 caracteres"})
    meta_twitter_creator=models.CharField(max_length=50,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas para Redes Sociales Creador</b> debe tener máximo 50 caracteres"})
    meta_keywords=models.TextField(max_length=250,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas Principales Palabras Claves </b> debe tener máximo 250 caracteres"})
    meta_og_imagen=models.ImageField(storage= FileSystemStorage( location='MedCongressApp/static/'),upload_to='metas',blank=True, null=True )
    meta_title=models.CharField(max_length=50,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas Principales Título </b> debe tener máximo 50 caracteres"})
    class Meta:
        verbose_name='El Meta de la Página Inicio'
        verbose_name_plural='Los Metas de la Página de Inicio'

    def __str__(self):
        return self.meta_title 
   

#####  Tabla metadatos de la pagina Listar Congreso 

class MetaPagListCongreso(models.Model): 
    meta_og_title=models.CharField(max_length=50,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas para FaceBook Título</b> debe tener máximo 50 caracteres"})
    meta_description=models.TextField(max_length=160,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas Principales Descripción</b> debe tener máximo 160 caracteres"})
    meta_og_description=models.TextField(max_length=160,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas para FaceBook Descripción</b> debe tener máximo 160 caracteres"})
    meta_og_type=models.CharField(max_length=50,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas para FaceBook Tipo</b> debe tener máximo 50 caracteres"})
    meta_og_url=models.CharField(max_length=250,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas para FaceBook URL</b> debe tener máximo 250 caracteres"})
    meta_twitter_card=models.CharField(max_length=50,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas para Redes Sociales Card</b> debe tener máximo 50 caracteres"})
    meta_twitter_site=models.CharField(max_length=250,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas para Redes Sociales Sitio</b> debe tener máximo 250 caracteres"})
    meta_twitter_creator=models.CharField(max_length=50,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas para Redes Sociales Creador</b> debe tener máximo 50 caracteres"})
    meta_keywords=models.TextField(max_length=250,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas Principales Palabras Claves </b> debe tener máximo 250 caracteres"})
    meta_og_imagen=models.ImageField(storage= FileSystemStorage( location='MedCongressApp/static/'),upload_to='metas',blank=True, null=True )
    meta_title=models.CharField(max_length=50,null=True,blank=True,error_messages={
"max_length": "El Campo <b>Metas Principales Título </b> debe tener máximo 50 caracteres"})
    class Meta:
        verbose_name='El Meta de la Página Listar Congresos'
        verbose_name_plural='Los Metas de la Página Listar Congresos'

    def __str__(self):
        return self.meta_title 


class PreguntasFrecuentes(models.Model):
    pregunta=models.CharField(max_length=250,error_messages={
"max_length": "El Campo <b>Pregunta </b> debe tener máximo 250 caracteres"})
    respuesta=models.TextField()
    congreso=models.ForeignKey(Congreso,on_delete=models.CASCADE)
    published=models.BooleanField(null=True)
    class Meta:
        verbose_name='Pregunta frecuente de un Congreso'
        verbose_name_plural='Preguntas fercuentes de los Congresos'

    def __str__(self):
        return self.pregunta 


##### Tabla de Información de quienes somos en la Pagina de Inicio #####
class QuienesSomos(models.Model):
    titulo=models.CharField(max_length=250,error_messages={
"max_length": "El Campo <b>Título </b> debe tener máximo 250 caracteres"} )
    sub_titulo=models.CharField(max_length=250,error_messages={
"max_length": "El Campo <b>SubTítulo </b> debe tener máximo 250 caracteres"})
    texto=models.TextField()
    
    class Meta:
        verbose_name='quienes somos'
        verbose_name_plural='quienes somos'

    def __str__(self):
        return self.titulo 


##### Tabla Imagenes Quienes Somos #####

class ImagenQuienesSomos(models.Model):
    imagen=models.ImageField(storage= FileSystemStorage( location='MedCongressApp/static/'),upload_to='congreso' ,verbose_name='imagen', null=False)
    q_somos=models.ForeignKey(QuienesSomos,on_delete=models.CASCADE)

    class Meta:
        verbose_name='imagen de quienes somos'
        verbose_name_plural='Imagenes de quienes somos'

    def __str__(self):
        return 'Imagen del quienes somos  %s'%(self.q_somos.titulo)


##### Tabla de Información de Ofrecemos en la Pagina de Inicio #####
class Ofrecemos(models.Model):
    titulo=models.CharField(max_length=250,error_messages={
"max_length": "El Campo <b>Título </b> debe tener máximo 250 caracteres"} )
    icono=models.ImageField(storage= FileSystemStorage( location='MedCongressApp/static/'),upload_to='assets/img/iconos' ,verbose_name='icono', null=False)
    texto=models.TextField()
    
    class Meta:
        verbose_name='ofrecemos'
        verbose_name_plural='ofrecemos'

    def __str__(self):
        return self.titulo 

class Footer(models.Model):
    direccion=models.CharField(max_length=250,error_messages={
"max_length": "El Campo <b>Dirección </b> debe tener máximo 250 caracteres"})
    email=models.EmailField()
    telefono=models.CharField(max_length=20,validators=[
            RegexValidator(regex=r"^[0-9()+-]+$", message="Entre un No. de <b>Teléfono</b> correcto. Ej. <b>(+99)999-999-999</b>")
        ],error_messages={
"max_length": "El Campo <b>Teléfono </b> debe tener máximo 20 caracteres"})
    whatsapp=models.CharField(max_length=20,validators=[
            RegexValidator(regex=r"^[0-9()+-]+$", message="Entre un No. de <b>Whatsapp</b> correcto. Ej. <b>(+99)999-999-999</b>" )
        ],error_messages={
"max_length": "El Campo <b>Whatsapp </b> debe tener máximo 20 caracteres"})
    
    class Meta:
        verbose_name='Contacto footer'
        verbose_name_plural='Contacto footer'

    def __str__(self):
        return 'Contactos del Footer'

class ImagenHome(models.Model):
    imagen=models.ImageField(storage= FileSystemStorage( location='MedCongressApp/static/'),upload_to='congreso' ,verbose_name='imagen', null=False)

    class Meta:
        verbose_name='Imagen Home'
        

    def __str__(self):
        return 'Imagen Home'

class Documento(models.Model):
    documento=models.FileField(storage= FileSystemStorage( location='MedCongressApp/static/'),upload_to='documentos')
    titulo=models.CharField(max_length=25,error_messages={
"max_length": "El Campo <b>Título </b> debe tener máximo 25 caracteres"})
    class Meta:
        verbose_name='Documento'

    def __str__(self):
        return 'Documento'
##### Tabla Idiomas #####

class Idioma(models.Model):
    nombre= models.CharField(max_length=20,unique=True,error_messages={
"max_length": "El Campo <b>Nombre </b> debe tener máximo 20 caracteres"})
    abreviatura= models.CharField(max_length=4,unique=True,error_messages={
"max_length": "El Campo <b>Abreviatura </b> debe tener máximo 4 caracteres"})
    class Meta:
        verbose_name='idioma'
        verbose_name_plural='idiomas'
        
    def __str__(self):
        return self.nombre

class DocumentoPrograma(models.Model):
    documento=models.FileField(storage= FileSystemStorage( location='MedCongressApp/static/'),upload_to='programas')
    texto=models.CharField(max_length=25,error_messages={
"max_length": "El Campo <b>Texto </b> debe tener máximo 25 caracteres"})
    idioma=models.ForeignKey(Idioma,on_delete=models.CASCADE)
    congreso=models.ForeignKey(Congreso,on_delete=models.CASCADE)
    class Meta:
        verbose_name='DocumentoPrograma'

    def __str__(self):
        return 'Documento'

class Carrito(models.Model):
    id_congreso_cat_pago=models.IntegerField()
    tipo_evento=models.CharField(max_length=20)                        
    id_evento=models.IntegerField()                        
    nombre_congreso=models.CharField(max_length=250) 
    id_cat_pago=models.IntegerField()
    nombre_cat_pago=models.CharField(max_length=250) 
    precio=models.FloatField() 
    pagar=models.FloatField() 
    moneda=models.CharField(max_length=3)                       
    cantidad=models.IntegerField()
    usuario=models.ForeignKey(User,on_delete=models.CASCADE)                       
    class Meta:
        verbose_name='Cart'

    def __str__(self):
        return 'Carrito de Compra'

class Session(models.Model):
    usuario=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True,unique=True) 
    fecha_inicio=models.DateTimeField() 
    class Meta:
        verbose_name='Session'

    def __str__(self):
        return 'Session usuario <%s>' %(self.usuario.email)  

class TrabajosInvestigacion(models.Model):
    documento=models.FileField(storage= FileSystemStorage( location='MedCongressApp/static/'),upload_to='trabajos')
    titulo=models.CharField(max_length=250, null=False,unique=True,error_messages={
                            "max_length": "El Campo <b>Título</b> debe tener máximo 250 caracteres","unique":"Ya existe un <b> Trabajo de Investigación</b> con ese título"})
    descripcion=models.TextField(null=True,blank=True)
    congreso=models.ForeignKey(Congreso,on_delete=models.CASCADE)
    autor= models.CharField( max_length=50,error_messages={
                            "max_length": "El Campo <b>Autor</b> debe tener máximo 50 caracteres"},validators=[
                            RegexValidator(regex=r"^[\w.,+\- ]+$", message="El Campo <b> Autor </b> solo admite números, letras y (.,+-)")
                            ],)
    cod_video=models.TextField(null=True,blank=True)
    foto=models.ImageField(storage= FileSystemStorage( location='MedCongressApp/static/'),upload_to='usuarios',blank=True, null=True )
    path=models.CharField(max_length=250, unique=True,null=True, help_text='campo para identificarlo por la URL')
    class Meta:
        verbose_name='TrabajosInvestigacion'

    def __str__(self):
        return 'TrabajosInvestigacion'


class UserActivityLog(models.Model):
    user = models.ForeignKey(PerfilUsuario, on_delete = models.CASCADE)
    fecha = models.DateTimeField( editable = False)
    congreso= models.ForeignKey(Congreso, on_delete = models.CASCADE)
    mensaje= models.CharField(max_length=250)
    tipo= models.CharField(max_length=100)
    tiempo= models.CharField(max_length=100)
    class Meta:
        ordering = ['fecha']
    
    def __str__(self):
        return self.user

class BecasPendientes(models.Model):
    congreso= models.ForeignKey(Congreso, on_delete = models.CASCADE)
    email=models.EmailField()

    class Meta:
        verbose_name='BecasPendientes'

    def __str__(self):
        return 'Beca Pendiente del correo %s en el congreso %s'%s(self.email,self.congreso)

##### Tabla Constancia por usuarios  #####

class ConstanciaUsuario(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    congreso = models.ForeignKey(Congreso, on_delete=models.CASCADE)
    folio_constancia=models.CharField(null=True,max_length=250)
    fecha_constancia=models.DateField(null=True)
    tipo_constancia=models.CharField(null=True,max_length=50)
    foto_constancia=models.ImageField(storage= FileSystemStorage( location='MedCongressApp/static/'),upload_to='congreso/img_constancia',null=True)
    
    class Meta:
        verbose_name='constancia - usuario'
        unique_together = (('user','congreso','tipo_constancia'),)


    def __str__(self):
        return ' Constancia del usuario %s %s por haber participado como %s en el congreso " %s " ' %( self.user.first_name,self.user.last_name,self.tipo_constancia,self.congreso.titulo)

##### Tabla  Organizador  #####

class Organizador(models.Model):
    user = models.ForeignKey(PerfilUsuario, on_delete=models.CASCADE)
    congreso=models.ForeignKey(Congreso,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name='organizador'
        verbose_name_plural='organizadores'

    def __str__(self):
        return '%s %s <%s> Organizador del Congreso " %s "'%(self.user.usuario.first_name,self.user.usuario.last_name,self.user.usuario.email,self.congreso.titulo)
