'''
 ============================================================================
 | MedCongress Application Administration Module Routing Configuration File |
 ============================================================================

'''
from django.urls import path,include

from .views.country_views import (CountryCreateView, CountryDeleteView,
                                  CountryListView, CountryUpdateView)
from .views.congress_views import (CongressListView,CongressCreateView,CongressUpdateView,
                                   CongressTalleresListView,CongressPonenciasListView,CongressCategPagosListView,
                                   CongressImagenesListView,AddPonenciaCongreso,CongressCategPagosCreateView,
                                   CongressDeletedView,CongressBloquesListView,GetBloques,AsignarCongressListView,AsignarCongressAddViews,GetPagos,
                                   AsignarCongressDeletedViews,CongressImagenCreateView,CongressCuestionarioListView,CongressPregFrecuenteListView,
                                   Ver_usuarios,Ver_Exel,Exportar_usuarios,Usuarios_pagaron)
from .views.imagen_views import (ImagenCreateView)
from .views.ponencia_view import (PonenciaListView, PonenciaCreateView,PonenciaPonenteListView,
                                   PonencicaUpdateView,PonenciaPonenteCreateView,PonenciaDeletedView,
                                   PonenciaPonenteDeletedView,PonenciaBloqueDeleted)
from .views.taller_view import (TalleresListView,TallerCreateView,TallerCategPagosListView,TallerCategPagosCreateView,
                                   TallerUpdateView,TallerPonenteListView,TallerPonenteCreateView,TallerDeletedView,AsignarTalleresListView,
                                   AsignarTallerAddViews,GetPagosT,AsignarTallerDeletedViews,TallerPonenteDeletedView,TallerBloqueDeleted)
from .views.ponente_view import (PonentesListView,PonentesCreateView,PonenteDeletedView)
from .views.user_views import (UsuariosListView,UsuarioCreateView,UsuarioUpdateView,UsuarioDeletedView)
from .views.bloque_views import (BloquesListView,BloqueCreateView,BloqueDeletedView,BloquePonenciasListView,BloqueTalleresListView,
                                   BloqueUpdateView,BloqueModeradoresListView,page_not_found,BloqueModeradoresCreateView,BloqueModeradoresDeletedView)
from .views.otros_views import (OtrosListView,OtroUpdateView)
from .views.cuestionario_views import (PreguntaCreateView,CustionarioUpdateView)
from .views.moderador_view import ModeradoresListView,ModeradorCreateView,ModeradorDeletedView
from .views.meta_views import MetaPagInicioView,MetaPagInicioUpdateView
from .views.preg_frecuente_view import PregFrecuenteCreateView,PregFrecuenteUpdateView,PregFrecuenteDeletView
from .views.dashboard import DashboardView
from django.conf.urls import handler404

handler404= page_not_found

app_name = 'MedCongressAdmin'

urlpatterns = [
     path('', DashboardView.as_view(), name='dashboard'),
     path('pais', CountryListView.as_view(), name='country_list'),
     path('pais/adicionar', CountryCreateView.as_view(), name='country_add'),
     path('pais/adicionar/<str:param>', CountryCreateView.as_view(), name='country_add_plus'),
     path('pais/editar/<int:pk>', CountryUpdateView.as_view(), name='country_edit'),
     path('pais/eliminar/<int:pk>', CountryDeleteView.as_view(), name='country_delete'),
     path('accounts/', include('django.contrib.auth.urls')),

     # Congresos
     path('congreso', CongressListView.as_view(), name='congress_list'),
     path('congreso/adicionar', CongressCreateView.as_view(), name='congres_add'),
     path('congreso/editar/<int:pk>', CongressUpdateView.as_view(), name='congres_edit'),
     path('congreso/eliminar/<int:pk>', CongressDeletedView.as_view(), name='congress_delete'),

     # Pagar Congresos
     path('asignar/congreso', AsignarCongressListView.as_view(), name='asig_congress_list'),
     path('asignar/congreso/add', AsignarCongressAddViews.as_view(), name='asignar_congress_add'),
     path('asignar/congreso/eliminar/<int:pk>', AsignarCongressDeletedViews.as_view(), name='asig_congres_delete'),

     # Congreso-Ponencias
     path('ponencias/congreso/<str:path>', CongressPonenciasListView.as_view(), name='Congres_ponencias'),
     path('ponencia/congreso/add/<int:pk>', PonenciaCreateView.as_view(), name='ponente_ponencia_add'),

     # Congreso-Cuestionarios
     path('cuestionario/congreso/<str:path>', CongressCuestionarioListView.as_view(), name='Congres_cuestionario'),
     path('cuestionario_pregunta/congreso/add/<str:path>', PreguntaCreateView.as_view(), name='congreso_cuestionario_pregunta_add'),

      # Congreso-PregFrecuentes
     path('pregunta_frecuente/congreso/<str:path>', CongressPregFrecuenteListView.as_view(), name='Congres_freg_frecuente'),
     path('pregunta_frecuente/congreso/add/<str:path>', PregFrecuenteCreateView.as_view(), name='congreso_preg_frecuente_add'),

     # Congreso-Talleres
     path('talleres/congreso/<str:path>', CongressTalleresListView.as_view(), name='Congres_talleres'),
     path('taller/congreso/add/<int:pk>', TallerCreateView.as_view(), name='congreso_taller_add'),

     # Congreso-Bloques
     path('bloques/congreso/<str:path>', CongressBloquesListView.as_view(), name='Congres_bloques'),
     path('bloque/congreso/add/<int:pk>', BloqueCreateView.as_view(), name='congres_bloque_add'),

     # Ponencias
     path('ponencias', PonenciaListView.as_view(), name='ponencias_list'),
     path('ponencia/adicionar', PonenciaCreateView.as_view(), name='ponencia_add'),
     path('ponencia/editar/<int:pk>', PonencicaUpdateView.as_view(), name='ponencia_edit'),
     path('ponencia/eliminar/<int:pk>', PonenciaDeletedView.as_view(), name='ponencia_delete'),
     
     # Talleres
     path('talleres', TalleresListView.as_view(), name='talleres_list'),
     path('taller/adicionar', TallerCreateView.as_view(), name='taller_add'),
     path('taller/editar/<int:pk>', TallerUpdateView.as_view(), name='taller_edit'),
     path('taller/eliminar/<int:pk>', TallerDeletedView.as_view(), name='taller_delete'),

     # Pagar Talleres
     path('asignar/talleres', AsignarTalleresListView.as_view(), name='asig_talleres_list'),
     path('asignar/taller/add', AsignarTallerAddViews.as_view(), name='asignar_taller_add'), 
     path('asignar/taller/eliminar/<int:pk>', AsignarTallerDeletedViews.as_view(), name='asig_taller_delete'),

     # Usuarios
     path('usuarios', UsuariosListView.as_view(), name='usuarios_list'),
     path('usuario/adicionar', UsuarioCreateView.as_view(), name='usuario_add'),
     path('usuario/editar/<int:pk>', UsuarioUpdateView.as_view(), name='usuario_edit'),
     path('usuario/eliminar/<int:pk>', UsuarioDeletedView.as_view(), name='user_delete'),
     

     # Ponentes
     path('ponentes', PonentesListView.as_view(), name='Ponentes_list'),
     path('ponente/adicionar', PonentesCreateView.as_view(), name='ponente_add'),
     path('ponente/eliminar/<int:pk>', PonenteDeletedView.as_view(), name='ponente_delete'),
     path('ponentes/ponencia/<str:path>', PonenciaPonenteListView.as_view(), name='Ponencia_ponentes'),
     path('ponentes/taller/<str:path>', TallerPonenteListView.as_view(), name='Taller_ponentes'),
     path('ponentes-taller/adicionar/<str:path>', TallerPonenteCreateView.as_view(), name='taller_ponente_add'),
     path('ponentes-ponencia/adicionar/<str:path>', PonenciaPonenteCreateView.as_view(), name='ponecia_ponente_add'),
     path('ponentes-ponencia/eliminar/<int:pk>', PonenciaPonenteDeletedView.as_view(), name='ponecia_ponente_delete'),
     path('ponentes-taller/eliminar/<int:pk>', TallerPonenteDeletedView.as_view(), name='taller_ponente_delete'),


     # Moderadores
     path('moderadores', ModeradoresListView.as_view(), name='Moderadores_list'),
     path('moderador/adicionar', ModeradorCreateView.as_view(), name='moderador_add'),
     path('moderador/eliminar/<int:pk>', ModeradorDeletedView.as_view(), name='moderador_delete'),

     # Bloque-Moderadores
     path('moderadores/bloque/<str:path>', BloqueModeradoresListView.as_view(), name='Moderadores_bloque'),
     path('moderadores-bloque/adicionar/<str:path>', BloqueModeradoresCreateView.as_view(), name='bloque_moderador_add'),
     path('moderadores-bloque/eliminar/<int:pk>', BloqueModeradoresDeletedView.as_view(), name='moderador_block_delete'),
     

     # bloques
     path('bloques', BloquesListView.as_view(), name='bloques_list'),
     path('bloque/adicionar', BloqueCreateView.as_view(), name='bloque_add'), 
     path('bloque/editar/<int:pk>', BloqueUpdateView.as_view(), name='bloque_edit'),
     path('bloque/eliminar/<int:pk>', BloqueDeletedView.as_view(), name='bloque_delete'),
     
     # otros
     path('otros', OtrosListView.as_view(), name='otros_list'),
     path('otro/editar/<int:pk>', OtroUpdateView.as_view(), name='otro_edit'),

    

     # Bloque-Ponencias
     path('ponencias/bloque/<str:path>', BloquePonenciasListView.as_view(), name='Bloque_ponencias'),
     path('ponencia/bloque/add/<int:pk_block>', PonenciaCreateView.as_view(), name='ponencia_bloque_add'),

     # Bloque-talleres
     path('talleres/bloque/<str:path>', BloqueTalleresListView.as_view(), name='Bloque_talleres'),
     path('taller/bloque/add/<int:pk_block>', TallerCreateView.as_view(), name='taller_bloque_add'),
 
     

     # funciones Ajax
     path('get_bloques', GetBloques, name='Get_Bloque'),
     path('get_pago', GetPagos, name='Get_Pago'),
     path('get_pago_taller', GetPagosT, name='Get_Pago_taller'),
     path('taller/bloque/eliminar', TallerBloqueDeleted, name='taller_block_delete'),
     path('ponencia/bloque/eliminar', PonenciaBloqueDeleted, name='ponencia_block_delete'),
     
     
    #Categorias de Pagos
     path('categorias_pago/congreso/<str:path>', CongressCategPagosListView.as_view(), name='Congres_pagos'),
     path('categorias_pago-congres/adicinar/<str:path>', CongressCategPagosCreateView.as_view(), name='congres_cat_pago_add'),
     path('categorias_pago/taller/<str:path>', TallerCategPagosListView.as_view(), name='Taller_pagos'),
     path('categoria_pago-taller/adicionar/<str:path>', TallerCategPagosCreateView.as_view(), name='taller_cat_pago_add'),

     #Congreso-Imagenes
     path('imagenes/congreso/<str:path>', CongressImagenesListView.as_view(), name='Congres_imagenes'),
     path('imagen-congreso/adicinar/<int:pk>', CongressImagenCreateView.as_view(), name='imagen_congress_add'),
     
     #Cuestionarios
     path('cuestionario_pregunta/congreso/add/', PreguntaCreateView.as_view(), name='cuestionario_pregunta_add'),
     path('cuestionario/editar/<int:pk>', CustionarioUpdateView.as_view(), name='cuestionario_edit'),
  
     #Metadatos
     path('meta_pagina_inicio', MetaPagInicioView.as_view(), name='meta_pag_inicio'),
     path('meta_pagina_inicio/editar/<int:pk>', MetaPagInicioUpdateView.as_view(), name='meta_pag_inicio_edit'),
     
     #Pregunta Frecuentes
   
     path('pregunat_frecuente/editar/<int:pk>', PregFrecuenteUpdateView.as_view(), name='preg_frecuente_edit'),
     path('pregunat_frecuente/eliminar/<int:pk>', PregFrecuenteDeletView.as_view(), name='preg_frecuente_delete'),
     
     #Ver Usuarios
     path('ver_usuarios', Ver_usuarios.as_view(), name='Ver_usuarios'),
     path('descargar_exel', Ver_Exel.as_view(), name='Ver_exel'),
     path('exp_usuario', Exportar_usuarios.as_view(), name='Exportar_usuarios'),
     path('usurios_pagaron', Usuarios_pagaron.as_view(), name='Usuarios_pagaron'),
     
     
]
