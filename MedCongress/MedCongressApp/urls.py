from django.contrib import admin
from django.urls import path
from .views import (Home,CongresoListView,CongresoDetail,CongresoCardForm,PerfilUserCreate)

urlpatterns = [
    
    path('', Home.as_view(),name='Home'),
    path('congresos', CongresoListView.as_view(),name='List_congreso'),
    path('congreso/<int:pk>/', CongresoDetail.as_view(), name='View_congreso'),
    path('pagar_congreso/<int:pk>/<int:pk_cat>', CongresoCardForm.as_view(), name='Pagar_congreso'),
    path('registrarse', PerfilUserCreate.as_view(), name='Registrarse'),
  
]
