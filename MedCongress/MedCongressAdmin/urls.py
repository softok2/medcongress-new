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
                                   AsignarCongressDeletedViews)
from .views.imagen_views import (ImagenCreateView)
from .views.ponencia_view import (PonenciaListView, PonenciaCreateView,PonenciaPonenteListView,
                                   PonencicaUpdateView,PonenciaPonenteCreateView,PonenciaDeletedView)
from .views.taller_view import (TalleresListView,TallerCreateView,TallerCategPagosListView,TallerCategPagosCreateView,
                                   TallerUpdateView,TallerPonenteListView,TallerPonenteCreateView,TallerDeletedView,AsignarTalleresListView,
                                   AsignarTallerAddViews,GetPagosT,AsignarTallerDeletedViews)
from .views.ponente_view import (PonentesListView,PonentesCreateView,PonenteDeletedView)
from .views.user_views import (UsuariosListView,UsuarioCreateView,UsuarioUpdateView,UsuarioDeletedView)
from .views.bloque_views import (BloquesListView,BloqueCreateView,BloqueDeletedView,BloquePonenciasListView,BloqueTalleresListView,
                                   BloqueUpdateView)
from .views.otros_views import (OtrosListView,OtroUpdateView)
from .views.moderador_view import ModeradoresListView
from .views.dashboard import DashboardView


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
     path('asignar/congreso', AsignarCongressListView.as_view(), name='asig_congress_list'),
     path('asignar/congreso/add', AsignarCongressAddViews.as_view(), name='asignar_congress_add'),
     path('asignar/congreso/eliminar/<int:pk>', AsignarCongressDeletedViews.as_view(), name='asig_congres_delete'),

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
     path('asignar/talleres', AsignarTalleresListView.as_view(), name='asig_talleres_list'),
     path('asignar/taller/add', AsignarTallerAddViews.as_view(), name='asignar_taller_add'), 
     path('asignar/taller/eliminar/<int:pk>', AsignarTallerDeletedViews.as_view(), name='asig_taller_delete'),

     #usuarios
     path('usuarios', UsuariosListView.as_view(), name='usuarios_list'),
     path('usuario/adicionar', UsuarioCreateView.as_view(), name='usuario_add'),
     path('usuario/editar/<int:pk>', UsuarioUpdateView.as_view(), name='usuario_edit'),
     path('usuario/eliminar/<int:pk>', UsuarioDeletedView.as_view(), name='user_delete'),
     

     #ponentes
     path('ponentes', PonentesListView.as_view(), name='Ponentes_list'),
     path('ponente/adicionar', PonentesCreateView.as_view(), name='ponente_add'),
     path('ponente/eliminar/<int:pk>', PonenteDeletedView.as_view(), name='ponente_delete'),

     #moderadores
     path('moderadores', ModeradoresListView.as_view(), name='Moderadores_list'),
     path('ponente/adicionar', PonentesCreateView.as_view(), name='ponente_add'),
     path('ponente/eliminar/<int:pk>', PonenteDeletedView.as_view(), name='ponente_delete'),

     #bloques
     path('bloques', BloquesListView.as_view(), name='bloques_list'),
     path('bloque/adicionar', BloqueCreateView.as_view(), name='bloque_add'), 
     path('bloque/editar/<int:pk>', BloqueUpdateView.as_view(), name='bloque_edit'),
     path('bloque/eliminar/<int:pk>', BloqueDeletedView.as_view(), name='bloque_delete'),
     
     #otros
     path('otros', OtrosListView.as_view(), name='otros_list'),
     path('otro/editar/<int:pk>', OtroUpdateView.as_view(), name='otro_edit'),

     # Congreso-Ponencias
     path('ponencias/congreso/<str:path>', CongressPonenciasListView.as_view(), name='Congres_ponencias'),
     #path('ponencias/congreso/adicionar', AddPonenciaCongreso.as_view(), name='Add_ponencia'),
     path('ponencia/congreso/add/<int:pk>', PonenciaCreateView.as_view(), name='ponente_ponencia_add'),

     #Congreso-Talleres
     path('talleres/congreso/<str:path>', CongressTalleresListView.as_view(), name='Congres_talleres'),
     path('taller/congreso/add/<int:pk>', TallerCreateView.as_view(), name='congreso_taller_add'),

     #Congreso-Bloques
     path('bloques/congreso/<str:path>', CongressBloquesListView.as_view(), name='Congres_bloques'),
     path('bloque/congreso/add/<int:pk>', BloqueCreateView.as_view(), name='congres_bloque_add'),

     #Bloque-Ponencias
     path('ponencias/bloque/<str:path>', BloquePonenciasListView.as_view(), name='Bloque_ponencias'),
     path('ponencia/bloque/add/<int:pk_block>', PonenciaCreateView.as_view(), name='ponencia_bloque_add'),
     #Bloque-talleres
     path('talleres/bloque/<str:path>', BloqueTalleresListView.as_view(), name='Bloque_talleres'),
     path('taller/bloque/add/<int:pk_block>', TallerCreateView.as_view(), name='taller_bloque_add'),

     path('get_bloques', GetBloques, name='Get_Bloque'),
     path('get_pago', GetPagos, name='Get_Pago'),
     path('get_pago_taller', GetPagosT, name='Get_Pago_taller'),
     
     path('ponencias/congreso/<str:path>', CongressPonenciasListView.as_view(), name='Congres_ponencias'),
    
     path('categorias_pago/congreso/<str:path>', CongressCategPagosListView.as_view(), name='Congres_pagos'),
     path('imagenes/congreso/<str:path>', CongressImagenesListView.as_view(), name='Congres_imagenes'),
     
     
     
     path('ponentes/ponencia/<str:path>', PonenciaPonenteListView.as_view(), name='Ponencia_ponentes'),
     path('ponentes/taller/<str:path>', TallerPonenteListView.as_view(), name='Taller_ponentes'),
     path('ponentes', PonentesListView.as_view(), name='Ponentes_list'),
     path('ponente/adicionar', PonentesCreateView.as_view(), name='ponente_add'),
     path('ponentes/pon/adicionar/<str:path>', PonenciaPonenteCreateView.as_view(), name='ponecia_ponente_add'),
     
     path('ponentes/tall/adicionar/<str:path>', TallerPonenteCreateView.as_view(), name='taller_ponente_add'),
     path('categorias_pago/congres/adicinar/<str:path>', CongressCategPagosCreateView.as_view(), name='congres_cat_pago_add'),
     path('categorias_pago/tall/<str:path>', TallerCategPagosListView.as_view(), name='Taller_pagos'),
     path('categoria_pago/taller/add/<str:path>', TallerCategPagosCreateView.as_view(), name='taller_cat_pago_add'),
     
     
     
     
     
]
