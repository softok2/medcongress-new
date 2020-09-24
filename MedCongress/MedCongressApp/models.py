from django.db import models
from django.contrib.auth.models import User

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
    denominacion= models.CharField(max_length=20)

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
    ponente=models.BooleanField()
    cel_profecional=models.CharField(max_length=50)
    foto=models.ImageField(upload_to='img')
    activation_key = models.CharField(max_length=40,blank=True, null=True)
    key_expires = models.DateTimeField(blank=True, null=True)
    usuario=models.OneToOneField(User, on_delete=models.CASCADE)
    categoria=models.ForeignKey(CategoriaUsuario,on_delete=models.DO_NOTHING)
    pais=models.ForeignKey(Pais,on_delete=models.DO_NOTHING)
    genero=models.ForeignKey(Genero,on_delete=models.DO_NOTHING)


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
    logo=models.ImageField(upload_to='img')

    class Meta:
        verbose_name='aval del congreso'
        verbose_name_plural='avales de los congresos'

    def __str__(self):
        return self.nombre

#### Tabla Categorias de Pago para Congresos ######

class CategoriaPagoCongreso(models.Model):
    nombre=models.CharField(max_length=50)
    detalle=models.TextField(null=True,blank=True)

    class Meta:
        verbose_name='categoria de pago del congreso'
        verbose_name_plural='categorias de pago para los congresos'

    def __str__(self):
        return self.nombre

#### Tabla Congresos #######

class Congreso(models.Model):
    titulo=models.CharField(max_length=50)
    imagen=models.ImageField(upload_to='img')
    detalle=models.TextField(null=True,blank=True)
    precio=models.IntegerField()
    lugar=models.CharField(max_length=50)
    fecha_inicio=models.DateTimeField(null=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(null=True, blank=True)
    published=models.BooleanField()
    t_congreso=models.ForeignKey(TipoCongreso,on_delete=models.DO_NOTHING)
    especialidad=models.ForeignKey(EspecialidadCongreso,on_delete=models.DO_NOTHING,null=True)
    user = models.ManyToManyField(User, through='RelCongresoUser')
    aval = models.ManyToManyField(AvalCongreso, through='RelCongresoAval')
    categoria_pago = models.ManyToManyField(CategoriaPagoCongreso, through='RelCongresoCategoriaPago')

    class Meta:
        verbose_name='congreso'
        verbose_name_plural='congresos'

    def __str__(self):
        return self.titulo

##### Tabla pivote Congreso- Usuario #####

class RelCongresoUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    congreso = models.ForeignKey(Congreso, on_delete=models.CASCADE)
    categoria_pago = models.ForeignKey(CategoriaPagoCongreso, on_delete=models.CASCADE,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

##### Tabla pivote Congreso- Avales #####

class RelCongresoAval(models.Model):
    aval = models.ForeignKey(AvalCongreso, on_delete=models.CASCADE)
    congreso = models.ForeignKey(Congreso, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

##### Tabla pivote Congreso- Categorias de Pagos #####

class RelCongresoCategoriaPago(models.Model):
    categoria = models.ForeignKey(CategoriaPagoCongreso, on_delete=models.CASCADE)
    congreso = models.ForeignKey(Congreso, on_delete=models.CASCADE)
    precio=models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name='Relación Congreso - Categoría de Pago'
        verbose_name_plural='Relaciones Congreso - Categoría de Pago'

    def __str__(self):
        return 'Relación entre el Congreso '+ self.congreso.titulo +' y la Categoría de Pago '+ self.categoria.nombre

##### Tabla  Ponente  #####

class Ponente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name='ponente'
        verbose_name_plural='ponentes'

    def __str__(self):
        return self.user.first_name +' '+self.user.last_name

#### Tabla Ponencia #######

class Ponencia(models.Model):
    titulo=models.CharField(max_length=50)
    duracion=models.CharField(max_length=250)
    detalle=models.TextField(null=True,blank=True)
    imagen=models.ImageField(upload_to='img',null=True,blank=True)
    fecha_inicio=models.DateTimeField()
    lugar=models.CharField(max_length=250)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(null=True, blank=True)
    published=models.BooleanField()
    congreso=models.ForeignKey(Congreso,on_delete=models.DO_NOTHING)
    ponente = models.ManyToManyField(Ponente, through='RelPonenciaPonente')
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
    created_at = models.DateTimeField(auto_now_add=True)

##### Tabla pivote Ponencia - Votacion  #####

class RelPonenciaVotacion(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    ponencia = models.ForeignKey(Ponencia, on_delete=models.DO_NOTHING)
    votacion=models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)


#### Tabla Taller #######

class Taller(models.Model):
    titulo=models.CharField(max_length=50)
    duracion=models.CharField(max_length=250)
    precio=models.IntegerField()
    fecha_inicio=models.DateTimeField()
    lugar=models.CharField(max_length=250)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(null=True, blank=True)
    published=models.BooleanField()
    congreso=models.ForeignKey(Congreso,on_delete=models.DO_NOTHING)
    ponente = models.ManyToManyField(Ponente, through='RelTallerPonente')
    votacion = models.ManyToManyField(User, through='RelTallerVotacion')
    
    

    class Meta:
        verbose_name='taller'
        verbose_name_plural='talleres'

    def __str__(self):
        return self.titulo


##### Tabla pivote Ponencia - Ponente  #####

class RelTallerPonente(models.Model):
    ponente = models.ForeignKey(Ponente, on_delete=models.DO_NOTHING)
    taller = models.ForeignKey(Taller, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)

##### Tabla pivote Ponencia - Votacion  #####

class RelTallerVotacion(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    taller = models.ForeignKey(Taller, on_delete=models.DO_NOTHING)
    votacion=models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)



