from django.contrib import admin
from django.urls import path
from .views import (Home,CongresoListView,CongresoDetail,CongresoCardForm,PerfilUserCreate,
ViewErrorOpenpay,PagarEfectivo,ViewError404,ViewPonencia,EspecialdiadesAutocomplete,
AddCart,AddCartTaller,DeletedCart,ConfCart,AvisoPrivacidad,HabilitarUser,Perfil,PagoExitoso,Email,GetPerfil,
GetCuestionario,SetConstancia,EvaluarPonencia,Resultado_Cuestionario,Get_Constancia,VerTransaccion,GetFactura,
ViewErrorFact,PerfilUpdateView,CambiarPass,UpdateEvaluarPonencia,UserAutocomplete,ViewErrorRegistrar,RegistroExitoso)

urlpatterns = [
    
    path('', Home.as_view(),name='Home'),
    path('congresos', CongresoListView.as_view(),name='List_congreso'),
    path('congreso/<str:path>', CongresoDetail.as_view(), name='View_congreso'),
    path('pagar', CongresoCardForm.as_view(), name='Pagar'),
    path('registrarse', PerfilUserCreate.as_view(), name='Registrarse'),
    path('view_ponencia/<str:path>', ViewPonencia.as_view(), name='View_ponencia'),
    path('error404', ViewError404.as_view(), name='Error404'),
    path('error_openpay', ViewErrorOpenpay.as_view(), name='Error_openpay'),
    path('error_registrar', ViewErrorRegistrar.as_view(), name='ErrorRegistrar'),
    
    
    path('error_facturacion', ViewErrorFact.as_view(), name='Error_facturacion'),
    path('pagar_efectivo', PagarEfectivo.as_view(), name='Pagar_efectivo'),
    path('editar_perfil/<int:pk>', PerfilUpdateView.as_view(), name='Edit_perfil'),
    


    path('especialidades_autocomp', EspecialdiadesAutocomplete , name='Especialidades_autocomp'),
    path('user_autocomp', UserAutocomplete , name='User_autocomp'),
    path('add_cart', AddCart.as_view() , name='Add_cart'),
    path('add_cart_taller', AddCartTaller.as_view() , name='Add_cart_taller'),
    path('deleted_cart',DeletedCart.as_view() , name='Deleted_cart'),
    path('conf_cart',ConfCart.as_view() , name='Conf_cart'),
    path('aviso_privacidad',AvisoPrivacidad.as_view() , name='aviso_privacidad'),
    path('email',Email.as_view() , name='email'),
    # path('confic_email',ConfigEmail.as_view() , name='confic_email'),
    path('habilitar_user/<str:token>',HabilitarUser.as_view() , name='habilitar_user'),
    path('perfil',Perfil.as_view() , name='perfil'),
    path('transaccion_exitosa',PagoExitoso.as_view() , name='transaccion_exitosa'),
    path('get_perfil', GetPerfil.as_view() , name='GetPerfil'),
    path('get_factura/<str:invoice>', GetFactura.as_view() , name='Factura'),
    path('cuestionario/congreso/<str:path>',GetCuestionario.as_view() , name='Cuestionario'),
    path('constancia/congreso/<str:path>',SetConstancia.as_view() , name='Constancia'),
    path('evaluar/ponencia',EvaluarPonencia.as_view() , name='EvaluarPonencia'),
    path('reevaluar/ponencia',UpdateEvaluarPonencia.as_view() , name='UpdateEvaluarPonencia'),

    
    path('cuestionario/resultado/<str:path>',Resultado_Cuestionario.as_view() , name='Resultado_Cuestionario'),
    path('ver_constancia/congreso/<str:path>',Get_Constancia.as_view() , name='Get_Constancia'),
    path('ver_transaccion',VerTransaccion.as_view() , name='ver_transaccion'),
    path('cambiar_pass',CambiarPass.as_view() , name='Cambiar_Pass'),
    path('registro_existoso',RegistroExitoso.as_view() , name='Registro_exitoso'),
    
    
    # path('asignar_pass',AsignarPass.as_view() , name='pass'),
    
    
    
  
]
