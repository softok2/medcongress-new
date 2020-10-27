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
                                   CongressDeletedView)
from .views.imagen_views import (ImagenCreateView)
from .views.ponencia_view import (PonenciaListView, PonenciaCreateView,PonenciaPonenteListView,
                                   PonencicaUpdateView,PonenciaPonenteCreateView,PonenciaDeletedView)
from .views.taller_view import (TalleresListView,TallerCreateView,TallerCategPagosListView,TallerCategPagosCreateView,
                                   TallerUpdateView,TallerPonenteListView,TallerPonenteCreateView,TallerDeletedView)
from .views.ponente_view import (PonentesListView,PonentesCreateView,PonenteDeletedView)
from .views.user_views import (UsuariosListView,UsuarioCreateView,UsuarioUpdateView)
from .views.bloque_views import (BloquesListView,BloqueCreateView)
from .views.otros_views import (OtrosListView,OtroUpdateView)

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
     
    
     # Ponencias
     path('ponencias', PonenciaListView.as_view(), name='ponencias_list'),
     path('ponencia/adicionar', PonenciaCreateView.as_view(), name='ponencia_add'),
     path('ponencia/editar/<int:pk>', PonencicaUpdateView.as_view(), name='ponencia_edit'),
     path('ponencia/eliminar/<int:pk>', PonenciaDeletedView.as_view(), name='ponencia_delete'),
     path('ponencia/congreso/add/<int:pk>', PonenciaCreateView.as_view(), name='ponente_ponencia_add'),
     # Talleres
     path('talleres', TalleresListView.as_view(), name='talleres_list'),
     path('taller/adicionar', TallerCreateView.as_view(), name='taller_add'),
     path('taller/editar/<int:pk>', TallerUpdateView.as_view(), name='taller_edit'),
     path('taller/congreso/add/<int:pk>', TallerCreateView.as_view(), name='congreso_taller_add'),
     path('taller/eliminar/<int:pk>', TallerDeletedView.as_view(), name='taller_delete'),
     #usuarios
     path('usuarios', UsuariosListView.as_view(), name='usuarios_list'),
     path('usuario/adicionar', UsuarioCreateView.as_view(), name='usuario_add'),
     path('usuario/editar/<int:pk>', UsuarioUpdateView.as_view(), name='usuario_edit'),
     #ponentes
     path('ponentes', PonentesListView.as_view(), name='Ponentes_list'),
     path('ponente/adicionar', PonentesCreateView.as_view(), name='ponente_add'),
     path('ponente/eliminar/<int:pk>', PonenteDeletedView.as_view(), name='ponente_delete'),
     #bloques
     path('bloques', BloquesListView.as_view(), name='bloques_list'),
     path('bloque/adicionar', BloqueCreateView.as_view(), name='bloque_add'), 

     #otros
     path('otros', OtrosListView.as_view(), name='otros_list'),
     path('otro/editar/<int:pk>', OtroUpdateView.as_view(), name='otro_edit'),
     path('imagen/add', ImagenCreateView.as_view(), name='Add_imagen'),
     path('talleres/congreso/<str:path>', CongressTalleresListView.as_view(), name='Congres_talleres'),
     path('ponencias/congreso/<str:path>', CongressPonenciasListView.as_view(), name='Congres_ponencias'),
     path('categorias_pago/congreso/<str:path>', CongressCategPagosListView.as_view(), name='Congres_pagos'),
     path('imagenes/congreso/<str:path>', CongressImagenesListView.as_view(), name='Congres_imagenes'),
     path('ponencias/congreso/adicionar', AddPonenciaCongreso.as_view(), name='Add_ponencia'),
     path('ponencia/adicionar', PonenciaCreateView.as_view(), name='ponencia_add'),
     
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
