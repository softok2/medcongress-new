from django.contrib import admin
from django.urls import path
from .views import (Home,CongresoListView,CongresoDetail,CongresoCardForm,PerfilUserCreate,ViewError404)

urlpatterns = [
    
    path('', Home.as_view(),name='Home'),
    path('congresos', CongresoListView.as_view(),name='List_congreso'),
    path('congreso/<str:path>', CongresoDetail.as_view(), name='View_congreso'),
    path('pagar_congreso/<str:path_congreso>/<str:path_categoria>', CongresoCardForm.as_view(), name='Pagar_congreso'),
    path('registrarse', PerfilUserCreate.as_view(), name='Registrarse'),

    path('error404', ViewError404.as_view(), name='Error404'),
  
]
