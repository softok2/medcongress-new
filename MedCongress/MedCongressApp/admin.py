from django.contrib import admin
from .models import *


admin.site.register(AvalCongreso)
admin.site.register(CategoriaPagoCongreso)
admin.site.register(CategoriaUsuario)
admin.site.register(Congreso)
admin.site.register(EspecialidadCongreso)
admin.site.register(Genero)
admin.site.register(Pais)
admin.site.register(PerfilUsuario)
admin.site.register(Ponencia)
admin.site.register(Ponente)
admin.site.register(RelCongresoAval)
admin.site.register(RelCongresoCategoriaPago)
admin.site.register(RelCongresoUser)
admin.site.register(RelPonenciaPonente)
admin.site.register(RelPonenciaVotacion)
admin.site.register(RelTallerPonente)
admin.site.register(RelTallerVotacion)
admin.site.register(Taller)
admin.site.register(TipoCongreso)

