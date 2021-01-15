from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.core.validators import RegexValidator
from django.utils import timezone
from django.db import models


# Create your models here.

##### Tabla Categoria del usuario  ###

class CategoriaUsuario(models.Model):
    nombre=models.CharField(max_length=50)
    published=models.BooleanField(null=True)
    detalle=models.TextField(null=True,blank=True)

    class Meta:
        verbose_name='categoria del usuario'
        verbose_name_plural='categorias del usuario'

    def __str__(self):
        return self.nombre


##### Tabla Especialidades  ###

class Especialidades(models.Model):
    nombre=models.CharField(max_length=50,unique=True)
    detalle=models.TextField(null=True,blank=True)

    class Meta:
        verbose_name='especialidad del usuario'
        verbose_name_plural='especialidades del usuario'

    def __str__(self):
        return self.nombre

##### Tabla País #####

class Pais(models.Model):
    denominacion = models.CharField(unique=True, max_length=50)
    banderas=models.ImageField(storage= FileSystemStorage( location='MedCongressApp/static/'),upload_to='banderas',blank=True, null=True )

    class Meta:
        verbose_name = 'pais'
        verbose_name_plural = 'paises'

    def __str__(self):
        return self.denominacion

##### Tabla Género #####

class Genero(models.Model):
    denominacion= models.CharField(max_length=20,unique=True)

    class Meta:
        verbose_name='genero'
        verbose_name_plural='generos'
        
    def __str__(self):
        return self.denominacion

##### Tabla Ubicacion #####

class Ubicacion(models.Model):
    direccion= models.CharField(max_length=250)
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
    linkedin=models.CharField(max_length=50,null=True)
    facebook=models.CharField(max_length=50,null=True)
    twitter=models.CharField(max_length=50,null=True)
    youtube=models.CharField(max_length=50,null=True)
    publicaciones=models.TextField(null=True,blank=True)
    puesto=models.TextField(max_length=250,null=True,blank=True)
    meta_og_title=models.CharField(max_length=50,null=True,blank=True)
    meta_description=models.TextField(max_length=160,null=True,blank=True)
    meta_og_description=models.TextField(max_length=160,null=True,blank=True)
    meta_og_type=models.CharField(max_length=50,null=True,blank=True)
    meta_og_url=models.CharField(max_length=50,null=True,blank=True)
    meta_twitter_card=models.CharField(max_length=50,null=True,blank=True)
    meta_twitter_site=models.CharField(max_length=50,null=True,blank=True)
    meta_twitter_creator=models.CharField(max_length=50,null=True,blank=True)
    meta_keywords=models.TextField(max_length=250,null=True,blank=True)
    meta_og_imagen=models.ImageField(storage= FileSystemStorage( location='MedCongressApp/static/'),upload_to='metas',blank=True, null=True )
    meta_title=models.CharField(max_length=250,null=True,blank=True)
    score=models.IntegerField(null=True)
    fecha_nacimiento=models.DateField(null=True)
    num_telefono=models.CharField(max_length=20,null=True)
    class Meta:
        verbose_name='Perfil usuario'
        verbose_name_plural='Perfil de usuarios'

    def __str__(self):
        return self.usuario.email 

    def is_openpay(self):
        if self.id_openpay :
            return True
        else:
            return False
    

#### Tabla Tipo de Congresos que hay ######

class TipoCongreso(models.Model):
    nombre=models.CharField(max_length=50,unique=True)
    detalle=models.TextField(null=True,blank=True)

    class Meta:
        verbose_name='tipo de congreso'
        verbose_name_plural='tipos de congresos'

    def __str__(self):
        return self.nombre

#### Tabla Especialidad de Congresos que hay ######

class EspecialidadCongreso(models.Model):
    nombre=models.CharField(max_length=50,unique=True)
    detalle=models.TextField(null=True,blank=True)

    class Meta:
        verbose_name='especialidad del congreso'
        verbose_name_plural='especialidades de los congresos'

    def __str__(self):
        return self.nombre



#### Tabla Aval de Congresos que hay ######

class AvalCongreso(models.Model):
    nombre=models.CharField(max_length=50,unique=True)
    detalle=models.TextField(null=True,blank=True)
    logo=models.ImageField(storage= FileSystemStorage( location='MedCongressApp/static/'),upload_to='patrocinadores' )
    url= models.CharField(max_length=250)

    class Meta:
        verbose_name='aval del congreso'
        verbose_name_plural='avales de los congresos'

    def __str__(self):
        return self.nombre

    #### Tabla Socio de Congresos que hay ######

class SocioCongreso(models.Model):
    nombre=models.CharField(max_length=50,unique=True)
    detalle=models.TextField(null=True,blank=True)
    logo=models.ImageField(storage= FileSystemStorage( location='MedCongressApp/static/'),upload_to='socios' )
    url= models.CharField(max_length=250)

    class Meta:
        verbose_name='socio del congreso'
        verbose_name_plural='socios de los congresos'

    def __str__(self):
        return self.nombre

#### Tabla Categorias de Pago para Congresos ######

class CategoriaPagoCongreso(models.Model):
    nombre=models.CharField(max_length=50,unique=True)
    path=models.CharField(max_length=250, help_text='campo para identificarlo por la URL')
    detalle=models.TextField(null=True,blank=True)

    class Meta:
        verbose_name='categoria de pago del congreso'
        verbose_name_plural='categorias de pago para los congresos'

    def __str__(self):
        return self.nombre

#### Tabla Congresos #######

class Congreso(models.Model):
    titulo=models.CharField(max_length=250,unique=True)
    sub_titulo=models.CharField(max_length=250,null=True)
    imagen_seg=models.ImageField(storage= FileSystemStorage( location='MedCongressApp/static/'),upload_to='congreso')
    path=models.CharField(max_length=250, help_text='campo para identificarlo por la URL',unique=True)
    lugar=models.ForeignKey(Ubicacion,on_delete=models.DO_NOTHING)
    fecha_inicio=models.DateTimeField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(null=True, blank=True)
    published=models.BooleanField()
    t_congreso=models.ForeignKey(TipoCongreso,on_delete=models.DO_NOTHING)
    especialidad=models.ForeignKey(EspecialidadCongreso,on_delete=models.DO_NOTHING,null=True)
    user = models.ManyToManyField(PerfilUsuario, through='RelCongresoUser',related_name='congreso_perfilusuario')
    aval = models.ManyToManyField(AvalCongreso, through='RelCongresoAval',related_name='congreso_patrosinador')
    categoria_pago = models.ManyToManyField(CategoriaPagoCongreso, through='RelCongresoCategoriaPago',related_name='congreso_cat_pago')
    is_openpay=models.BooleanField(null=True)
    template=models.CharField(max_length=50,null=True)
    meta_og_title=models.CharField(max_length=50,null=True,blank=True)
    meta_description=models.TextField(max_length=160,null=True,blank=True)
    meta_og_description=models.TextField(max_length=160,null=True,blank=True)
    meta_og_type=models.CharField(max_length=50,null=True,blank=True)
    meta_og_url=models.CharField(max_length=50,null=True,blank=True)
    meta_twitter_card=models.CharField(max_length=50,null=True,blank=True)
    meta_twitter_site=models.CharField(max_length=50,null=True,blank=True)
    meta_twitter_creator=models.CharField(max_length=50,null=True,blank=True)
    meta_keywords=models.TextField(max_length=250,null=True,blank=True)
    meta_og_imagen=models.ImageField(storage= FileSystemStorage( location='MedCongressApp/static/'),upload_to='metas',blank=True, null=True )
    meta_title=models.CharField(max_length=250,null=True,blank=True)
    foto_constancia=models.ImageField(storage= FileSystemStorage( location='MedCongressApp/static/'),upload_to='congreso/img_constancia',null=True)
    aprobado=models.IntegerField(null=True)
    cant_preguntas=models.IntegerField(null=True)
    score=models.IntegerField(null=True)
    streaming=models.TextField(null=True,blank=True)
    programa=models.FileField(storage= FileSystemStorage( location='MedCongressApp/static/'),upload_to='programas',null=True,blank=True)
    detalles_tipo_boleto=models.TextField(null=True,blank=True)
    detalles_tipo_boleto_taller=models.TextField(null=True,blank=True)
    ver_titulo=models.BooleanField(default=True)

    class Meta:
        verbose_name='congreso'
        verbose_name_plural='congresos'

    def __str__(self):
        return self.titulo

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
    categoria_pago = models.ForeignKey(CategoriaPagoCongreso, on_delete=models.CASCADE)
    is_pagado=models.BooleanField(default=False)
    id_transaccion=models.CharField(max_length=20)
    num_autorizacion_transaccion=models.CharField(max_length=20)
    num_tarjeta_tranzaccion=models.CharField(max_length=16)
    created_at = models.DateTimeField(auto_now_add=True)
    cantidad=models.IntegerField(null=True)
    is_constancia=models.BooleanField(null=True)
    fecha_constancia=models.DateField(null=True)
    cuestionario=models.CharField(null=True,max_length=250)
    foto_constancia=models.ImageField(storage= FileSystemStorage( location='MedCongressApp/static/'),upload_to='congreso/img_constancia',null=True)
    uuid_factura=models.CharField(max_length=36,null=True)

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
        return self.user.usuario.email

##### Tabla  moderador  #####

class Moderador(models.Model):
    user = models.OneToOneField(PerfilUsuario, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name='moderador'
        verbose_name_plural='moderadores'

    def __str__(self):
        return self.user.usuario.email 

#### Tabla Bloque #######

class Bloque(models.Model):
    titulo=models.CharField(max_length=250)
    duracion=models.CharField(max_length=250)
    detalle=models.TextField(null=True,blank=True)
    fecha_inicio=models.DateTimeField()
    path=models.CharField(max_length=250, help_text='campo para identificarlo por la URL')
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(null=True, blank=True)
    published=models.BooleanField()
    moderador = models.ManyToManyField(Moderador, through='RelBloqueModerador',related_name='bloque_moderador')
    congreso=models.ForeignKey(Congreso,on_delete=models.CASCADE)
    
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


#### Tabla Ponencia #######

class Ponencia(models.Model):
    titulo=models.CharField(max_length=250)
    duracion=models.CharField(max_length=250)
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
    ponente = models.ManyToManyField(Ponente, through='RelPonenciaPonente',related_name='ponencia_ponente')
    votacion = models.ManyToManyField(User, through='RelPonenciaVotacion')
    meta_og_title=models.CharField(max_length=50,null=True,blank=True)
    meta_description=models.TextField(max_length=160,null=True,blank=True)
    meta_og_description=models.TextField(max_length=160,null=True,blank=True)
    meta_og_type=models.CharField(max_length=50,null=True,blank=True)
    meta_og_url=models.CharField(max_length=50,null=True,blank=True)
    meta_twitter_card=models.CharField(max_length=50,null=True,blank=True)
    meta_twitter_site=models.CharField(max_length=50,null=True,blank=True)
    meta_twitter_creator=models.CharField(max_length=50,null=True,blank=True)
    meta_keywords=models.TextField(max_length=250,null=True,blank=True)
    meta_og_imagen=models.ImageField(storage= FileSystemStorage( location='MedCongressApp/static/'),upload_to='metas',blank=True, null=True )
    meta_title=models.CharField(max_length=250,null=True,blank=True)
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
    titulo=models.CharField(max_length=250)
    duracion=models.CharField(max_length=250) 
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
    meta_og_title=models.CharField(max_length=50,null=True,blank=True)
    meta_description=models.TextField(max_length=160,null=True,blank=True)
    meta_og_description=models.TextField(max_length=160,null=True,blank=True)
    meta_og_type=models.CharField(max_length=50,null=True,blank=True)
    meta_og_url=models.CharField(max_length=50,null=True,blank=True)
    meta_twitter_card=models.CharField(max_length=50,null=True,blank=True)
    meta_twitter_site=models.CharField(max_length=50,null=True,blank=True)
    meta_twitter_creator=models.CharField(max_length=50,null=True,blank=True)
    meta_keywords=models.TextField(max_length=250,null=True,blank=True)
    meta_og_imagen=models.ImageField(storage= FileSystemStorage( location='MedCongressApp/static/'),upload_to='metas',blank=True, null=True )
    meta_title=models.CharField(max_length=250,null=True,blank=True)
    

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
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    taller = models.ForeignKey(Taller, on_delete=models.DO_NOTHING)
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
    pregunta= models.CharField(max_length=250)
    published=models.BooleanField(null=True)
    def __str__(self):
        return pregunta

    class Meta:
        verbose_name='Pregunta del Cuestionario'
        verbose_name_plural='Preguntas del Cuestionario'
##### Tabla Cuestionarios-Respuestas#####

class CuestionarioRespuestas(models.Model):
    pregunta=models.ForeignKey(CuestionarioPregunta,on_delete=models.CASCADE)
    respuesta= models.CharField(max_length=250)
    is_correcto=models.BooleanField()
    published=models.BooleanField(null=True)

#####  Tabla metadatos de la pagina Inicio 

class MetaPagInicio(models.Model): 
    meta_og_title=models.CharField(max_length=50,null=True,blank=True)
    meta_description=models.TextField(max_length=160,null=True,blank=True)
    meta_og_description=models.TextField(max_length=160,null=True,blank=True)
    meta_og_type=models.CharField(max_length=50,null=True,blank=True)
    meta_og_url=models.CharField(max_length=50,null=True,blank=True)
    meta_twitter_card=models.CharField(max_length=50,null=True,blank=True)
    meta_twitter_site=models.CharField(max_length=50,null=True,blank=True)
    meta_twitter_creator=models.CharField(max_length=50,null=True,blank=True)
    meta_keywords=models.TextField(max_length=250,null=True,blank=True)
    meta_og_imagen=models.ImageField(storage= FileSystemStorage( location='MedCongressApp/static/'),upload_to='metas',blank=True, null=True )
    meta_title=models.CharField(max_length=250,null=True,blank=True)
    class Meta:
        verbose_name='El Meta de la Página Inicio'
        verbose_name_plural='Los Metas de la Página de Inicio'

    def __str__(self):
        return self.meta_title 
   

#####  Tabla metadatos de la pagina Listar Congreso 

class MetaPagListCongreso(models.Model): 
    meta_og_title=models.CharField(max_length=50,null=True,blank=True)
    meta_description=models.TextField(max_length=160,null=True,blank=True)
    meta_og_description=models.TextField(max_length=160,null=True,blank=True)
    meta_og_type=models.CharField(max_length=50,null=True,blank=True)
    meta_og_url=models.CharField(max_length=50,null=True,blank=True)
    meta_twitter_card=models.CharField(max_length=50,null=True,blank=True)
    meta_twitter_site=models.CharField(max_length=50,null=True,blank=True)
    meta_twitter_creator=models.CharField(max_length=50,null=True,blank=True)
    meta_keywords=models.TextField(max_length=250,null=True,blank=True)
    meta_og_imagen=models.ImageField(storage= FileSystemStorage( location='MedCongressApp/static/'),upload_to='metas',blank=True, null=True )
    meta_title=models.CharField(max_length=250,null=True,blank=True)
    class Meta:
        verbose_name='El Meta de la Página Listar Congresos'
        verbose_name_plural='Los Metas de la Página Listar Congresos'

    def __str__(self):
        return self.meta_title 


class PreguntasFrecuentes(models.Model):
    pregunta=models.CharField(max_length=250)
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
    titulo=models.CharField(max_length=250, )
    sub_titulo=models.CharField(max_length=250)
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
    titulo=models.CharField(max_length=250, )
    icono=models.CharField(max_length=250)
    texto=models.TextField()
    
    class Meta:
        verbose_name='ofrecemos'
        verbose_name_plural='ofrecemos'

    def __str__(self):
        return self.titulo 

class Footer(models.Model):
    direccion=models.CharField(max_length=250)
    email=models.EmailField()
    telefono=models.CharField(max_length=20)
    whatsapp=models.CharField(max_length=20)
    
    class Meta:
        verbose_name='Contacto footer'
        verbose_name_plural='Contacto footer'

    def __str__(self):
        return 'Contactos del Footer'
