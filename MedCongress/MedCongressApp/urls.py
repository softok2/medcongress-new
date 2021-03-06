from django.contrib import admin
from django.urls import path
from .views import (Home,CongresoListView,CongresoDetail,CongresoCardForm,PerfilUserCreate,
ViewErrorOpenpay,PagarEfectivo,ViewError404,ViewPonencia,EspecialdiadesAutocomplete,
AddCart,AddCartTaller,DeletedCart,ConfCart,AvisoPrivacidad,HabilitarUser,Perfil,PagoExitoso,TermCondiciones,VerTransaccion)

urlpatterns = [
    
    path('', Home.as_view(),name='Home'),
    path('congresos', CongresoListView.as_view(),name='List_congreso'),
    path('congreso/<str:path>', CongresoDetail.as_view(), name='View_congreso'),
    path('pagar', CongresoCardForm.as_view(), name='Pagar'),
    path('registrarse', PerfilUserCreate.as_view(), name='Registrarse'),
    path('view_ponencia', ViewPonencia.as_view(), name='View_ponencia'),
    path('error404', ViewError404.as_view(), name='Error404'),
    path('error_openpay', ViewErrorOpenpay.as_view(), name='Error_openpay'),
    path('pagar_efectivo', PagarEfectivo.as_view(), name='Pagar_efectivo'),
    path('especialidades_autocomp', EspecialdiadesAutocomplete , name='Especialidades_autocomp'),
    path('add_cart', AddCart.as_view() , name='Add_cart'),
    path('add_cart_taller', AddCartTaller.as_view() , name='Add_cart_taller'),
    path('deleted_cart',DeletedCart.as_view() , name='Deleted_cart'),
    path('conf_cart',ConfCart.as_view() , name='Conf_cart'),
    path('aviso_privacidad',AvisoPrivacidad.as_view() , name='aviso_privacidad'),
    path('terminos_condiciones',TermCondiciones.as_view() , name='terminos_condiciones'),
    # path('email',Email.as_view() , name='email'),
    # path('confic_email',ConfigEmail.as_view() , name='confic_email'),
    path('habilitar_user/<str:token>',HabilitarUser.as_view() , name='habilitar_user'),
    path('perfil',Perfil.as_view() , name='perfil'),
    path('transaccion_exitosa',PagoExitoso.as_view() , name='transaccion_exitosa'),
    path('ver_transaccion',VerTransaccion.as_view() , name='ver_transaccion'),

    
    
  
]
