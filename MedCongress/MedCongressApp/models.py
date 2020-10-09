from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.db import models

# Create your models here.

##### Tabla Categoria del usuario  ###

class CategoriaUsuario(models.Model):
    nombre=models.CharField(max_length=50)
    detalle=models.TextField(null=True,blank=True)

    class Meta:
        verbose_name='categoria del usuario'
        verbose_name_plural='categorias del usuario'

    def __str__(self):
        return self.nombre

##### Tabla País #####

class Pais(models.Model):
    denominacion= models.CharField(max_length=50)

    class Meta:
        verbose_name='pais'
        verbose_name_plural='paises'

    def __str__(self):
        return self.denominacion

##### Tabla Género #####

class Genero(models.Model):
    denominacion= models.CharField(max_length=20)

    class Meta:
        verbose_name='genero'
        verbose_name_plural='generos'
        
    def __str__(self):
        return self.denominacion

## cargar valores por defecto en genero##


#####  Tabla Perfil Usuario (otros datos de interes del Usuario)

class PerfilUsuario(models.Model):
    ciudad=models.CharField(max_length=50)
    estado=models.CharField(max_length=50)
    id_openpay=models.CharField(max_length=20,null=True,blank=True)
    detalle=models.TextField(null=True,blank=True)
    is_ponente=models.BooleanField()
    path=models.CharField(max_length=50, help_text='campo para identificarlo por la URL')
    cel_profecional=models.CharField(max_length=50)
    foto=models.ImageField(storage= FileSystemStorage( location='MedCongressApp/static/'),upload_to='usuarios' )
    activation_key = models.CharField(max_length=40,blank=True, null=True)
    key_expires = models.DateTimeField(blank=True, null=True)
    usuario=models.OneToOneField(User, on_delete=models.CASCADE)
    categoria=models.ForeignKey(CategoriaUsuario,on_delete=models.DO_NOTHING)
    pais=models.ForeignKey(Pais,on_delete=models.DO_NOTHING)
    genero=models.ForeignKey(Genero,on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name='Perfil usuario'
        verbose_name_plural='Perfil de usuarios'

    def __str__(self):
        return self.usuario.first_name

    def is_openpay(self):
        if self.id_openpay :
            return True
        else:
            return False


#### Tabla Tipo de Congresos que hay ######

class TipoCongreso(models.Model):
    nombre=models.CharField(max_length=50)
    detalle=models.TextField(null=True,blank=True)

    class Meta:
        verbose_name='tipo de congreso'
        verbose_name_plural='tipos de congresos'

    def __str__(self):
        return self.nombre

#### Tabla Especialidad de Congresos que hay ######

class EspecialidadCongreso(models.Model):
    nombre=models.CharField(max_length=50)
    detalle=models.TextField(null=True,blank=True)

    class Meta:
        verbose_name='especialidad del congreso'
        verbose_name_plural='especialidades de los congresos'

    def __str__(self):
        return self.nombre



#### Tabla Aval de Congresos que hay ######

class AvalCongreso(models.Model):
    nombre=models.CharField(max_length=50)
    detalle=models.TextField(null=True,blank=True)
    logo=models.ImageField(storage= FileSystemStorage( location='MedCongressApp/static/'),upload_to='patrocinadores' )
    url= models.CharField(max_length=250)

    class Meta:
        verbose_name='aval del congreso'
        verbose_name_plural='avales de los congresos'

    def __str__(self):
        return self.nombre

#### Tabla Categorias de Pago para Congresos ######

class CategoriaPagoCongreso(models.Model):
    nombre=models.CharField(max_length=50)
    path=models.CharField(max_length=50, help_text='campo para identificarlo por la URL')
    detalle=models.TextField(null=True,blank=True)

    class Meta:
        verbose_name='categoria de pago del congreso'
        verbose_name_plural='categorias de pago para los congresos'

    def __str__(self):
        return self.nombre

#### Tabla Congresos #######

class Congreso(models.Model):
    titulo=models.CharField(max_length=250)
    imagen_seg=models.ImageField(storage= FileSystemStorage( location='MedCongressApp/static/'),upload_to='congreso')
    path=models.CharField(max_length=50, help_text='campo para identificarlo por la URL')
    lugar=models.CharField(max_length=50)
    fecha_inicio=models.DateTimeField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(null=True, blank=True)
    published=models.BooleanField()
    t_congreso=models.ForeignKey(TipoCongreso,on_delete=models.DO_NOTHING)
    especialidad=models.ForeignKey(EspecialidadCongreso,on_delete=models.DO_NOTHING,null=True)
    user = models.ManyToManyField(PerfilUsuario, through='RelCongresoUser',related_name='congreso_perfilusuario')
    aval = models.ManyToManyField(AvalCongreso, through='RelCongresoAval',related_name='congreso_patrosinador')
    categoria_pago = models.ManyToManyField(CategoriaPagoCongreso, through='RelCongresoCategoriaPago',related_name='congreso_cat_pago')

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
    imagen=models.ImageField(storage= FileSystemStorage( location='MedCongressApp/static/'),upload_to='congreso' ,verbose_name='imagen' )
    congreso=models.ForeignKey(Congreso,on_delete=models.DO_NOTHING)

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
    num_autorizacion_transaccion=models.CharField(max_length=6)
    num_tarjeta_tranzaccion=models.CharField(max_length=16)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return '%s->%s->%s'%(self.user.usuario.first_name, self.congreso.titulo, self.categoria_pago.nombre)

    class Meta:
        unique_together = (('user','congreso'),)

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

class CategoriaPonente(models.Model):
    nombre=models.CharField(max_length=50)
    path=models.CharField(max_length=50, help_text='campo para identificarlo por la URL')
    detalle=models.TextField(null=True,blank=True)
   
    class Meta:
        verbose_name='categoria de ponente'
        verbose_name_plural='categorias de los ponentes'

    def __str__(self):
        return 'Categoría %s'%(self.nombre)

##### Tabla  Ponente  #####

class Ponente(models.Model):
    user = models.OneToOneField(PerfilUsuario, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name='ponente'
        verbose_name_plural='ponentes'

    def __str__(self):
        return self.user.usuario.first_name +' '+self.user.usuario.last_name

#### Tabla Ponencia #######

class Ponencia(models.Model):
    titulo=models.CharField(max_length=250)
    duracion=models.CharField(max_length=250)
    detalle=models.TextField(null=True,blank=True)
    cod_video=models.CharField(max_length=10)
    imagen=models.ImageField(storage= FileSystemStorage( location='MedCongressApp/static/'),upload_to='ponencias')
    fecha_inicio=models.DateTimeField()
    path=models.CharField(max_length=50, help_text='campo para identificarlo por la URL')
    lugar=models.CharField(max_length=250)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(null=True, blank=True)
    published=models.BooleanField()
    congreso=models.ForeignKey(Congreso,on_delete=models.DO_NOTHING)
    ponente = models.ManyToManyField(Ponente, through='RelPonenciaPonente',related_name='ponencia_ponente')
    votacion = models.ManyToManyField(User, through='RelPonenciaVotacion')
    
    class Meta:
        verbose_name='ponencia'
        verbose_name_plural='ponencias'

    def __str__(self):
        return self.titulo


##### Tabla pivote Ponencia - Ponente  #####

class RelPonenciaPonente(models.Model):
    ponente = models.ForeignKey(Ponente, on_delete=models.DO_NOTHING)
    ponencia = models.ForeignKey(Ponencia, on_delete=models.DO_NOTHING)
    categoria=models.ForeignKey(CategoriaPonente,on_delete=models.DO_NOTHING,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name='Relación Ponente- Ponencia'
        verbose_name_plural='Relaciones Ponente - Ponencia'
        unique_together = (('ponencia','ponente'),)

    def __str__(self):
        return 'Relación entre la ponencia %s  y el ponente %s ' %(self.ponencia.titulo, self.ponente.user.usuario.first_name)

##### Tabla pivote Ponencia - Votacion  #####

class RelPonenciaVotacion(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    ponencia = models.ForeignKey(Ponencia, on_delete=models.DO_NOTHING)
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
    precio=models.IntegerField()
    fecha_inicio=models.DateTimeField()
    path=models.CharField(max_length=50, help_text='campo para identificarlo por la URL')
    imagen=models.ImageField(storage= FileSystemStorage( location='MedCongressApp/static/'),upload_to='talleres',blank=True, null=True )
    lugar=models.CharField(max_length=250)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(null=True, blank=True)
    published=models.BooleanField()
    congreso=models.ForeignKey(Congreso,on_delete=models.DO_NOTHING)
    ponente = models.ManyToManyField(Ponente, through='RelTallerPonente')
    votacion = models.ManyToManyField(User, through='RelTallerVotacion')
    categoria_pago = models.ManyToManyField(CategoriaPagoCongreso, through='RelTalleresCategoriaPago',related_name='talleres_cat_pago')
    

    class Meta:
        verbose_name='taller'
        verbose_name_plural='talleres'

    def __str__(self):
        return self.titulo


##### Tabla pivote Taller - Ponente  #####

class RelTallerPonente(models.Model):
    ponente = models.ForeignKey(Ponente, on_delete=models.DO_NOTHING)
    taller = models.ForeignKey(Taller, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name='Relación Ponente- Taller'
        verbose_name_plural='Relaciones Ponente - Taller'
        unique_together = (('ponente','taller'),)

    def __str__(self):
        return 'Relación entre la taller %s  y el ponente %s ' %(self.taller.titulo, self.ponente.user.first_name)

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
    num_autorizacion_transaccion=models.CharField(max_length=6)
    num_tarjeta_tranzaccion=models.CharField(max_length=16)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return '%s->%s->%s'%(self.user.usuario.first_name, self.taller.titulo, self.categoria_pago.nombre)

    class Meta:
        unique_together = (('user','taller'),)

##### Tabla Datos Iniciales#####

class DatosIniciales(models.Model):
    ponentes= models.IntegerField(null=True,default=0)
    ponencias= models.IntegerField(null=True,default=0)
    eventos= models.IntegerField(null=True,default=0)
    paises= models.IntegerField(null=True,default=0)
    especialidades= models.IntegerField(null=True,default=0)
    afiliados= models.IntegerField(null=True,default=0)
    talleres= models.IntegerField(null=True,default=0)