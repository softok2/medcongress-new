'''
 ============================================================================
 | MedCongress Application Administration Module Routing Configuration File |
 ============================================================================

'''
from django.urls import path,include

from .views.country_views import (CountryCreateView, CountryDeleteView,
                                  CountryListView, CountryUpdateView)
from .views.congress_views import (LogsCongreso,LogsUsuarios,CongressSalaCreateView,CongressDeletedSalaView,CongressSalaUpdateView,AsignarConstanciasUsuario,GetSalas,CongressListView,CongressCreateView,CongressUpdateView,
                                   AddPonenciaCongreso,CongressCategPagosCreateView,
                                   CongressDeletedView,GetBloques,AsignarCongressListView,AsignarCongressAddViews,GetPagos,
                                   AsignarCongressDeletedViews,CongressImagenCreateView,
                                   Ver_usuarios,Ver_Exel,Exportar_usuarios,Usuarios_pagaron,
                                   PatrocinadorSeleccionarView,PatrocinadorSeleccionarDeleted, SocioSeleccionarView,SocioSeleccionarDeleted,
                                   CongresoDetail,CongressImagenDeletedView,CongressCategPagosUpdateView,CongressCategPagosDeletedView,AsignarConstancias
                                   ,CongressProgramaUpdateView,CongressProgramaDeletedView,CongressProgramaCreateView,vTableAsJSONAsigCongreso,vTableAsJSONCongresos,ExportarBecas)
from .views.imagen_views import (ImagenCreateView,ImagenesListView)
from .views.sala_views import (SalasListView,vTableAsJSONCongresoSalas,OrdenarSalaView)
from .views.programa_views import (ProgramaListView)
from .views.boleto_views import (CategPagosListView)
from .views.beca_views import (vTableAsJSONBecaCongreso,BecasCongressListView)
from .views.ponencia_view import (PonenciaListView, PonenciaCreateView,PonenciaPonenteListView,
                                   PonencicaUpdateView,PonenciaPonenteCreateView,PonenciaDeletedView,
                                   PonenciaPonenteDeletedView,PonenciaBloqueDeleted,vTableAsJSONPonencia)
from .views.taller_view import (TalleresListView,TallerCreateView,TallerCategPagosListView,TallerCategPagosCreateView,
                                   TallerUpdateView,TallerPonenteListView,TallerPonenteCreateView,TallerDeletedView,AsignarTalleresListView,
                                   AsignarTallerAddViews,GetPagosT,AsignarTallerDeletedViews,TallerPonenteDeletedView,TallerBloqueDeleted,
                                   ReporteRelTallerUserExcel,AsignarConstanciasTaller,TallerCategPagosUpdateView,TallerCategPagosDeletedView,vTableAsJSONTaller,vTableAsJSONAsigTaller)
from .views.ponente_view import (PonentesListView,PonentesCreateView,PonenteDeletedView,UserPonenteCreateView,vTableAsJSONPonentes)
from .views.user_views import (UsuariosListView,UsuarioCreateView,UsuarioUpdateView,UsuarioDeletedView,vTableAsJSON)
from .views.bloque_views import (BloquesListView,BloqueCreateView,BloqueDeletedView,BloquePonenciasListView,BloqueTalleresListView,
                                   BloqueUpdateView,page_not_found,BloqueModeradoresDeletedView,
                                   PonenciaSeleccionarView)
from .views.repositorio_view import vTableAsJSONRepositorio,DocumentosListView,DocumentoCreateView,DocumentoDeletedView
from .views_nomencladores.genero_views import (GeneroListView,GeneroCreateView,GeneroDeletedView,GeneroUpdateView,vTableAsJSONGenero)
from .views_nomencladores.cat_pago_views import (vTableAsJSONCatPago,CatPagoListView,CatPagoCreateView,CatPagoDeletedView,CatPagoUpdateView)
from .views_nomencladores.patrocinador_views import (vTableAsJSONPatrocinador,PatrocinadorListView,PatrocinadorCreateView,PatrocinadorDeletedView,PatrocinadorUpdateView)
from .views_nomencladores.socio_views import (vTableAsJSONSocio,SocioListView,SocioCreateView,SocioDeletedView,SocioUpdateView)
from .views_nomencladores.cat_usuario_views import (vTableAsJSONCatUsuario,CatUsuarioListView,CatUsuarioCreateView,CatUsuarioDeletedView,CatUsuarioUpdateView)
from .views_nomencladores.esp_evento_views import (vTableAsJSONEspEventos,EspEventoListView,EspEventoCreateView,EspEventoDeletedView,EspEventoUpdateView)
from .views_nomencladores.tipo_evento_views import (vTableAsJSONTipoEvento,TipoEventoListView,TipoEventoCreateView,TipoEventoDeletedView,TipoEventoUpdateView)
from .views_nomencladores.idioma_views import (vTableAsJSONIdioma,IdiomaListView,IdiomaCreateView,IdiomaDeletedView,IdiomaUpdateView)
from .views_nomencladores.esp_usuario_views import (vTableAsJSONEspUsuario,EspUsuarioListView,EspUsuarioCreateView,EspUsuarioDeletedView,EspUsuarioUpdateView)
from .views_inicio.quienes_somos_views import (QuienesSomosListView,QuienesSomosUpdateView,QuienesSomosCreateView,QuienesSomosImagenCreateView,QuienesSomosImagenDeletedView)
from .views_inicio.imagen_home_view import ImagenListView,ImagenCreateView,ImagenUpdateView,ImagenDeletedView

from .views_inicio.footer_views import (FooterListView,FooterUpdateView,FooterCreateView)
from .views_inicio.meta_datos_views import (MetaInicioListView,MetaInicioUpdateView,MetaInicioCreateView,MetaListarListView,MetaListarUpdateView,MetaListarCreateView)

from .views_inicio.ofrecemos_views import (OfrecemosListView,OfrecemosCreateView,OfrecemosDeletedView,OfrecemosUpdateView)
from .views.otros_views import (OtrosListView,OtroUpdateView)
from .views.cuestionario_views import (PreguntaCreateView,CustionarioUpdateView,CustionarioDeletedView,CuestionarioListView)
from .views.trabajos_views import (TrabajosListView,CongressTrabajoCreateView,CongressTrabajoUpdateView,CongressTrabajoDeletedView)
from .views.moderador_view import ModeradoresListView,BloqueModeradoresCreateView,ModeradorCreateView,ModeradorDeletedView,vTableAsJSONModeradores,UserModeradorCreateView
from .views.organizador_view import OrganizadorListView,vTableAsJSONOrganizadores,OrganizadorCreateView,OrganizadorDeletedView
from .views.meta_views import MetaPagInicioView,MetaPagInicioUpdateView
from .views.preg_frecuente_view import PregFrecuenteListView,PregFrecuenteCreateView,PregFrecuenteUpdateView,PregFrecuenteDeletView
from .views.dashboard import DashboardView
from django.conf.urls import handler404

handler404= page_not_found

app_name = 'MedCongressAdmin'

urlpatterns = [
      path('', CongressListView.as_view(), name='dashboard'),
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
      path('congreso/previsualizar/<str:path>', CongresoDetail.as_view(), name='congress_previsualizar'),

      # Pagar Congresos
      path('asignar/congreso', AsignarCongressListView.as_view(), name='asig_congress_list'),
      path('asignar/congreso/add', AsignarCongressAddViews.as_view(), name='asignar_congress_add'),
      path('asignar/congreso/eliminar/<int:pk>', AsignarCongressDeletedViews.as_view(), name='asig_congres_delete'),

      #Becas Congreso
      
      path('becas/congreso', BecasCongressListView.as_view(), name='asig_becas_list'),
      path('exportar/becas', ExportarBecas.as_view(), name='exportar_becas'),
      # path('asignar/congreso/eliminar/<int:pk>', AsignarCongressDeletedViews.as_view(), name='asig_congres_delete'),
      
      # Congreso-Ponencias
      path('ponencia/congreso/add/<str:path>', PonenciaCreateView.as_view(), name='ponente_ponencia_add'),
      path('ponencia/editar/<str:path>/<int:pk>', PonencicaUpdateView.as_view(), name='Edit_Congreso_ponencia'),

      # Congreso-Cuestionarios
      path('cuestionario/congreso/<str:path>', CuestionarioListView.as_view(), name='Congres_cuestionario'),
      path('cuestionario_pregunta/congreso/add/<str:path>', PreguntaCreateView.as_view(), name='congreso_cuestionario_pregunta_add'),

        # Congreso-PregFrecuentes
      path('pregunta_frecuente/congreso/<str:path>',PregFrecuenteListView.as_view(), name='Congres_freg_frecuente'),
      path('pregunta_frecuente/congreso/add/<str:path>', PregFrecuenteCreateView.as_view(), name='congreso_preg_frecuente_add'),

      # Congreso-Talleres
      path('taller/congreso/add/<int:pk>', TallerCreateView.as_view(), name='congreso_taller_add'),

      # Congreso-Bloques
      # path('bloques/congreso/<str:path>', CongressBloquesListView.as_view(), name='Congres_bloques'),
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
      path('usuario/asig_congreso/<int:pk>', AsignarCongressAddViews.as_view(), name='asig_congreso'),
      

      # Ponentes
      path('ponentes', PonentesListView.as_view(), name='Ponentes_list'),
      path('ponente/adicionar', PonentesCreateView.as_view(), name='ponente_add'),
      path('ponente/eliminar/<int:pk>', PonenteDeletedView.as_view(), name='ponente_delete'),
      path('user-ponente/adicionar', UserPonenteCreateView.as_view(), name='user_ponente_add'),
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
      path('user-moderador/adicionar', UserModeradorCreateView.as_view(), name='user_moderador_add'),

      # Organizadores
      path('organizadores', OrganizadorListView.as_view(), name='Organizadores_list'),
      path('organizadores/adicionar', OrganizadorCreateView.as_view(), name='organizador_add'),
      path('organizador/eliminar/<int:pk>', OrganizadorDeletedView.as_view(), name='organizador_delete'),
      # path('user-moderador/adicionar', UserModeradorCreateView.as_view(), name='user_moderador_add'),
      
      # Bloque-Moderadores-
      # path('moderadores/bloque/<str:path>', BloqueModeradoresListView.as_view(), name='Moderadores_bloque'),
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
      path('ponencias/bloque/<str:path>/<str:tipo>', BloquePonenciasListView.as_view(), name='Bloque_ponencias'),
      path('ponencia/bloque/add/<int:pk_block>', PonenciaCreateView.as_view(), name='ponencia_bloque_add'),
      path('ponencia/bloque/edit/<str:pk_block>/<int:pk>', PonencicaUpdateView.as_view(), name='ponencia_bloque_edit'),
      path('bloque_ponencia/seleccionar/<str:path>', PonenciaSeleccionarView.as_view(), name='bloque_ponencia_select'),
      
      # Bloque-talleres
      path('talleres/bloque/<str:path>/<str:tipo>', BloqueTalleresListView.as_view(), name='Bloque_talleres'),
      path('taller/bloque/add/<int:pk_block>', TallerCreateView.as_view(), name='taller_bloque_add'),
  
      

      # funciones Ajax
      path('get_bloques', GetBloques, name='Get_Bloque'),
      path('get_sala', GetSalas, name='Get_Sala'),
      path('get_pago', GetPagos, name='Get_Pago'),
      path('get_pago_taller', GetPagosT, name='Get_Pago_taller'),
      path('taller/bloque/eliminar', TallerBloqueDeleted, name='taller_block_delete'),
      path('ponencia/bloque/eliminar', PonenciaBloqueDeleted, name='ponencia_block_delete'),
      
      
      #Categorias de Pagos-Congreso
      path('categorias_pago/congreso/<str:path>', CategPagosListView.as_view(), name='Congres_pagos'),
      path('categorias_pago-congres/adicinar/<str:path>', CongressCategPagosCreateView.as_view(), name='congres_cat_pago_add'),
      path('categorias_pago-congres/editar/<str:path>/<int:pk>', CongressCategPagosUpdateView.as_view(), name='congres_cat_pago_editar'),
      path('categorias_pago-congres/eliminar/<int:pk>', CongressCategPagosDeletedView.as_view(), name='congres_cat_pago_eliminar'),

      #Programa-Congreso
      path('programas/congreso/<str:path>',ProgramaListView.as_view(), name='Congres_programas'),
      path('programa-congres/adicinar/<str:path>', CongressProgramaCreateView.as_view(), name='congres_programa_add'),
      path('programa-congres/editar/<str:path>/<int:pk>', CongressProgramaUpdateView.as_view(), name='congres_programa_editar'),
      path('programa-congres/eliminar/<int:pk>', CongressProgramaDeletedView.as_view(), name='congres_programa_eliminar'),
      
  

      #Sala-Congreso
      path('salas/congreso/<str:path>', SalasListView.as_view(), name='Congres_salas'),
      path('sala-congres/adicinar/<str:path>', CongressSalaCreateView.as_view(), name='congres_sala_add'),
      path('sala-congres/editar/<str:path>/<int:pk>', CongressSalaUpdateView.as_view(), name='congres_sala_editar'),
      path('sala-congres/eliminar/<int:pk>', CongressDeletedSalaView.as_view(), name='congres_sala_eliminar'),
      path('sala-congres/ordenar', OrdenarSalaView.as_view(), name='congres_sala_ordenar'),

      


      #Categorias de Pagos-Taller
      path('categorias_pago/taller/<str:path>', TallerCategPagosListView.as_view(), name='Taller_pagos'),
      path('categoria_pago-taller/adicionar/<str:path>', TallerCategPagosCreateView.as_view(), name='taller_cat_pago_add'),
      path('categorias_pago-taller/editar/<int:pk>', TallerCategPagosUpdateView.as_view(), name='taller_cat_pago_editar'),
      path('categorias_pago-taller/eliminar/<int:pk>', TallerCategPagosDeletedView.as_view(), name='taller_cat_pago_eliminar'),


      #Congreso-Imagenes
      path('imagenes/congreso/<str:path>', ImagenesListView.as_view(), name='Congres_imagenes'),
      path('imagen-congreso/adicinar/<int:pk>', CongressImagenCreateView.as_view(), name='imagen_congress_add'),
        path('imagen-congreso/eliminar/<int:pk>', CongressImagenDeletedView.as_view(), name='imagen_congress_deleted'),
      

      #Congreso-Patrocinadores
      # path('patrocinadores/congreso/<str:path>', PatrocinadorListView.as_view(), name='Congres_patrocinadores'),
      path('patrocinador-congreso/adicinar/<int:pk>', PatrocinadorCreateView.as_view(), name='patrocinadores_congress_add'),
      path('patrocinador-congreso/seleccionar/<str:path>', PatrocinadorSeleccionarView.as_view(), name='patrocinadores_congress_select'),
      path('patrocinador-congreso/deleted', PatrocinadorSeleccionarDeleted, name='congreso_patrocinador_delete'),

      #Congreso-Socios
        path('socios/congreso/<str:path>', SocioListView.as_view(), name='Congres_socios'),
      path('socio-congreso/adicinar/<int:pk>', SocioCreateView.as_view(), name='socios_congress_add'),
      path('socio-congreso/seleccionar/<str:path>',SocioSeleccionarView.as_view(), name='socios_congress_select'),
      path('socio-congreso/deleted', SocioSeleccionarDeleted, name='congreso_socio_delete'),

      
      #Cuestionarios
      path('cuestionario_pregunta/congreso/add/', PreguntaCreateView.as_view(), name='cuestionario_pregunta_add'),
      path('cuestionario/editar/<int:pk>', CustionarioUpdateView.as_view(), name='cuestionario_edit'),
      path('cuestionario/eliminar/<int:pk>', CustionarioDeletedView.as_view(), name='cuestionario_delete'),
    
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
      path('usuarios_pagaron', Usuarios_pagaron.as_view(), name='Usuarios_pagaron'),
      

      #Reportes
      path('reporte_congreso_user', ReporteRelTallerUserExcel.as_view(), name='Rep_RelCongresoUser'),
        path('reporte_taller_user', ReporteRelTallerUserExcel.as_view(), name='Rep_RelTallerUser'),
      
        # Genero
      path('generos', GeneroListView.as_view(), name='generos_list'),
      path('genero/adicionar',GeneroCreateView.as_view(), name='genero_add'), 
      path('genero/editar/<int:pk>', GeneroUpdateView.as_view(), name='genero_edit'),
      path('genero/eliminar/<int:pk>', GeneroDeletedView.as_view(), name='genero_delete'),

        # Cat de Pago
      path('cat_pago', CatPagoListView.as_view(), name='cat_pagos_list'),
      path('cat_pago/adicionar',CatPagoCreateView.as_view(), name='cat_pago_add'), 
      path('cat_pago/editar/<int:pk>', CatPagoUpdateView.as_view(), name='cat_pago_edit'),
      path('cat_pago/eliminar/<int:pk>', CatPagoDeletedView.as_view(), name='cat_pago_delete'),

        # Patrocinadores
      path('patrocinador', PatrocinadorListView.as_view(), name='patrocinadores_list'),
      path('patrocinador/adicionar',PatrocinadorCreateView.as_view(), name='patrocinador_add'), 
      path('patrocinador/editar/<int:pk>', PatrocinadorUpdateView.as_view(), name='patrocinador_edit'),
      path('patrocinador/eliminar/<int:pk>', PatrocinadorDeletedView.as_view(), name='patrocinador_delete'),

        # Socios
      path('socio', SocioListView.as_view(), name='socios_list'),
      path('socio/adicionar',SocioCreateView.as_view(), name='socio_add'), 
      path('socio/editar/<int:pk>', SocioUpdateView.as_view(), name='socio_edit'),
      path('socio/eliminar/<int:pk>', SocioDeletedView.as_view(), name='socio_delete'),

        # Categoria de Usuarios
      path('cat_usuario', CatUsuarioListView.as_view(), name='cat_usuarios_list'),
      path('cat_usuario/adicionar',CatUsuarioCreateView.as_view(), name='cat_usuario_add'), 
      path('cat_usuario/editar/<int:pk>', CatUsuarioUpdateView.as_view(), name='cat_usuario_edit'),
      path('cat_usuario/eliminar/<int:pk>', CatUsuarioDeletedView.as_view(), name='cat_usuario_delete'),

        # Especialidades de Eventos
      path('esp_evento', EspEventoListView.as_view(), name='esp_eventos_list'),
      path('esp_evento/adicionar',EspEventoCreateView.as_view(), name='esp_evento_add'), 
      path('esp_evento/editar/<int:pk>', EspEventoUpdateView.as_view(), name='esp_evento_edit'),
      path('esp_evento/eliminar/<int:pk>', EspEventoDeletedView.as_view(), name='esp_evento_delete'),

        # Especialidades de usuarios
      path('esp_usuario', EspUsuarioListView.as_view(), name='esp_usuarios_list'),
      path('esp_usuario/adicionar',EspUsuarioCreateView.as_view(), name='esp_usuario_add'), 
      path('esp_usuario/editar/<int:pk>', EspUsuarioUpdateView.as_view(), name='esp_usuario_edit'),
      path('esp_usuario/eliminar/<int:pk>', EspUsuarioDeletedView.as_view(), name='esp_usuario_delete'),

        # Idiomas
      path('idiomas', IdiomaListView.as_view(), name='idiomas_list'),
      path('idioma/adicionar',IdiomaCreateView.as_view(), name='idioma_add'), 
      path('idioma/editar/<int:pk>', IdiomaUpdateView.as_view(), name='idioma_edit'),
      path('idioma/eliminar/<int:pk>', IdiomaDeletedView.as_view(), name='idioma_delete'),
      # Tipos de Eventos
      path('tipo_evento', TipoEventoListView.as_view(), name='tipo_eventos_list'),
      path('tipo_evento/adicionar',TipoEventoCreateView.as_view(), name='tipo_evento_add'), 
      path('tipo_evento/editar/<int:pk>', TipoEventoUpdateView.as_view(), name='tipo_evento_edit'),
      path('tipo_evento/eliminar/<int:pk>', TipoEventoDeletedView.as_view(), name='tipo_evento_delete'),

        #Quienes Somos
      path('quienes_somos', QuienesSomosListView.as_view(), name='quienes_somos_list'),
      path('quienes_somos/editar/<int:pk>', QuienesSomosUpdateView.as_view(), name='quienes_somos_edit'),
      path('quienes_somos/adicionar',QuienesSomosCreateView.as_view(), name='quienes_somos_add'), 


        #Footer
      path('footer', FooterListView.as_view(), name='footer_list'),
      path('footer/editar/<int:pk>', FooterUpdateView.as_view(), name='footer_edit'),
      path('footer/adicionar',FooterCreateView.as_view(), name='footer_add'), 

      #ImagenInicio
      path('imagen_inicio', ImagenListView.as_view(), name='imagen_list'),
      path('imagen_inicio/editar/<int:pk>', ImagenUpdateView.as_view(), name='imagen_edit'),
      path('imagen_inicio/adicionar',ImagenCreateView.as_view(), name='imagen_home_add'), 
      path('imagen_inicio/deleted/<int:pk>',ImagenDeletedView.as_view(), name='imagen_deleted'), 
      


      #Meta Pag Inicio
      path('meta_pag_inicio', MetaInicioListView.as_view(), name='meta_pag_inicio_list'),
      path('meta_pag_inicio/editar/<int:pk>', MetaInicioUpdateView.as_view(), name='meta_pag_inicio_edit'),
      path('meta_pag_inicio/adicionar',MetaInicioCreateView.as_view(), name='meta_pag_inicio_add'), 

      #Meta Pag Listar Congresos
      path('meta_pag_listar_congreso', MetaListarListView.as_view(), name='meta_pag_listar_list'),
      path('meta_pag_listar_congreso/editar/<int:pk>', MetaListarUpdateView.as_view(), name='meta_pag_listar_edit'),
      path('meta_pag_listar_congreso/adicionar',MetaListarCreateView.as_view(), name='meta_pag_listar_add'), 

        #Ofrecemos
      path('ofrecemos', OfrecemosListView.as_view(), name='ofrecemos_list'),
      path('ofrecemos/adicionar',OfrecemosCreateView.as_view(), name='ofrecemos_add'), 
      path('ofrecemos/editar/<int:pk>', OfrecemosUpdateView.as_view(), name='ofrecemos_edit'),
      path('ofrecemos/eliminar/<int:pk>', OfrecemosDeletedView.as_view(), name='ofrecemos_deleted'),

      #Congreso-Quienes Somos
      
      path('imagen-quienes_somos/adicinar', QuienesSomosImagenCreateView.as_view(), name='imagen-quienes_somos_add'),
      path('imagen-quienes_somos/eliminar/<int:pk>', QuienesSomosImagenDeletedView.as_view(), name='imagen_quienes_somos_deleted'),

      #Constancias-Congreso
      path('asignar_constancias', AsignarConstancias.as_view(), name='asig_constancia_list'),
      
          #Constancias-Taller
      path('asig_constancia_taller', AsignarConstanciasTaller.as_view(), name='asig_constancia_taller'),
      
      # Repositorio
      path('documentos', DocumentosListView.as_view(), name='documentos_list'),
      path('documento/adicionar',DocumentoCreateView.as_view(), name='documento_add'), 
      #  path('genero/editar/<int:pk>', GeneroUpdateView.as_view(), name='genero_edit'),
      path('documento/eliminar/<int:pk>', DocumentoDeletedView.as_view(), name='documento_delete'),

      # Trabajos de Investigacion
      # path('trabajos', TrabajosListView.as_view(), name='trabajos_list'),
        # Trabajos de Investigacion
      path('trabajos/congreso/<str:path>', TrabajosListView.as_view(), name='Congres_trabajos'),
      path('trabajos-congres/adicinar/<str:path>', CongressTrabajoCreateView.as_view(), name='congres_trabajo_add'),
      path('trabajos-congres/editar/<str:path>/<int:pk>', CongressTrabajoUpdateView.as_view(), name='congres_trabajo_editar'),
      path('trabajos-congres/eliminar/<int:pk>', CongressTrabajoDeletedView.as_view(), name='congres_trabajo_eliminar'),

      #Logs
      path('logs/congreso', LogsCongreso.as_view(), name='LogsCongreso'),
      path('logs/usuario', LogsUsuarios.as_view(), name='LogsUsuario'),
      
      

## Tablas en JSON


      path('pruebaTablaJson', vTableAsJSON.as_view(), name='table_json'),
      path('pruebaTablaJsonPonencia', vTableAsJSONPonencia.as_view(), name='table_json_ponencia'),
      path('pruebaTablaJsonTaller', vTableAsJSONTaller.as_view(), name='table_json_taller'),
       path('pruebaTablaJsonAsigCongreso', vTableAsJSONAsigCongreso.as_view(), name='table_json_asig_congreso'),
       path('pruebaTablaJsonBecaCongreso', vTableAsJSONBecaCongreso.as_view(), name='table_json_beca_congreso'),
       path('pruebaTablaJsonAsigTaller', vTableAsJSONAsigTaller.as_view(), name='table_json_asig_taller'),
      path('pruebaTablaJsonPonentes', vTableAsJSONPonentes.as_view(), name='table_json_ponentes'),
       path('pruebaTablaJsonModeradores', vTableAsJSONModeradores.as_view(), name='table_json_moderadores'),
      path('pruebaTablaJsonCongresos', vTableAsJSONCongresos.as_view(), name='table_json_congresos'),
      path('pruebaTablaJsonGenero', vTableAsJSONGenero.as_view(), name='table_json_generos'),
      path('pruebaTablaJsonCatPago', vTableAsJSONCatPago.as_view(), name='table_json_catpagos'),
    path('pruebaTablaJsonCatUsuario', vTableAsJSONCatUsuario.as_view(), name='table_json_catusuarios'),
    path('pruebaTablaJsonEspEvento', vTableAsJSONEspEventos.as_view(), name='table_json_esp_eventos'),
    path('pruebaTablaJsonEspUsuario', vTableAsJSONEspUsuario.as_view(), name='table_json_esp_usuarios'),
    path('pruebaTablaJsonIndioma', vTableAsJSONIdioma.as_view(), name='table_json_idiomas'),
    path('pruebaTablaJsonPatrocinador', vTableAsJSONPatrocinador.as_view(), name='table_json_patrocinadores'),
    path('pruebaTablaJsonSocio', vTableAsJSONSocio.as_view(), name='table_json_socios'),
     path('pruebaTablaJsonTipoEvento', vTableAsJSONTipoEvento.as_view(), name='table_json_tipo_eventos'),
     path('pruebaTablaJsonRepositorio', vTableAsJSONRepositorio.as_view(), name='table_json_documentos'),
    path('pruebaTablaJsonCongresosSalas', vTableAsJSONCongresoSalas.as_view(), name='table_json_salas'),
     path('TablaJsonOrganizadores', vTableAsJSONOrganizadores.as_view(), name='table_json_organizadores'), 

#Constancia Usuario
path('constancia-usuario/add/<int:pk>', AsignarConstanciasUsuario.as_view(), name='constancia_usuario_add'),
  ]
