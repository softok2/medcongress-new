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
                                   CongressImagenesListView,AddPonenciaCongreso,CongressCategPagosCreateView)
from .views.imagen_views import (ImagenCreateView)
from .views.ponencia_view import (PonenciaListView, PonenciaCreateView,PonenciaPonenteListView,PonenciaPonenteCreateView)
from .views.taller_view import (TalleresListView,TallerCreateView,TallerCategPagosListView,TallerCategPagosCreateView)
from .views.ponente_view import (PonentesListView,PonentesCreateView)
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
     path('congreso', CongressListView.as_view(), name='congress_list'),
     path('congreso/adicionar', CongressCreateView.as_view(), name='congres_add'),
     path('congreso/editar/<int:pk>', CongressUpdateView.as_view(), name='congres_edit'),
     path('imagen/add', ImagenCreateView.as_view(), name='Add_imagen'),
     path('talleres/congreso/<str:path>', CongressTalleresListView.as_view(), name='Congres_talleres'),
     path('ponencias/congreso/<str:path>', CongressPonenciasListView.as_view(), name='Congres_ponencias'),
     path('ponencias/congreso/adicionar', AddPonenciaCongreso.as_view(), name='Add_ponencia'),
     path('categorias_pago/congreso/<str:path>', CongressCategPagosListView.as_view(), name='Congres_pagos'),
     path('imagenes/congreso/<str:path>', CongressImagenesListView.as_view(), name='Congres_imagenes'),
     path('ponencias', PonenciaListView.as_view(), name='ponencias_list'),
     path('ponencia/adicionar', PonenciaCreateView.as_view(), name='ponencia_add'),
     path('talleres', TalleresListView.as_view(), name='talleres_list'),
     path('taller/adicionar', TallerCreateView.as_view(), name='taller_add'),
     path('ponentes/ponencia/<str:path>', PonenciaPonenteListView.as_view(), name='Ponencia_ponentes'),
     path('ponentes', PonentesListView.as_view(), name='Ponentes_list'),
     path('ponente/adicionar', PonentesCreateView.as_view(), name='ponente_add'),
     path('ponentes/pon/adicionar/<str:path>', PonenciaPonenteCreateView.as_view(), name='ponecia_ponente_add'),
     path('categorias_pago/congres/adicinar/<str:path>', CongressCategPagosCreateView.as_view(), name='congres_cat_pago_add'),
     path('categorias_pago/tall/<str:path>', TallerCategPagosListView.as_view(), name='Taller_pagos'),
     path('categoria_pago/taller/add/<str:path>', TallerCategPagosCreateView.as_view(), name='taller_cat_pago_add'),
     
     
     
     
     
]
