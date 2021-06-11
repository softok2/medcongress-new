from django.contrib import admin
from django.urls import path
from .views import (Home,CongresoListView,CongresoDetail,CongresoCardForm,PerfilUserCreate,
ViewErrorOpenpay,PagarEfectivo,ViewError404,ViewPonencia,EspecialdiadesAutocomplete,
AddCart,AddCartTaller,DeletedCart,ConfCart,AvisoPrivacidad,HabilitarUser,Perfil,PagoExitoso,Email,GetPerfil,
GetCuestionario,SetConstancia,EvaluarPonencia,Resultado_Cuestionario,Get_Constancia,VerTransaccion,GetFactura,
ViewErrorFact,PerfilUpdateView,CambiarPass,UpdateEvaluarPonencia,UserAutocomplete,ViewErrorRegistrar,RegistroExitoso,
PonenteAutocomplete,ModeradorAutocomplete,CongresoAutocomplete,PatrocinadorAutocomplete,SocioAutocomplete,ViewTaller,
EvaluarTaller,UpdateEvaluarTaller,TallerAutocomplete,PonenciaAutocomplete,ViewCart,ContactoExitoso,GetFacturaPrueba,GetContactos,Enviar,
Webhook,PagoExitoso2,ViewTrabajo,ViewSala,ViewPonenciasSala,DonwloadTrabajo,PerfilCongresos,PerfilConstancias,VideoBloque)

urlpatterns = [
    # path('login',login,name='auth'),
    path('', Home.as_view(),name='Home'),
    path('congresos', CongresoListView.as_view(),name='List_congreso'),
    path('congreso/<str:path>', CongresoDetail.as_view(), name='View_congreso'),
    path('pagar', CongresoCardForm.as_view(), name='Pagar'),
    path('registrarse', PerfilUserCreate.as_view(), name='Registrarse'),
    path('ponencia/<str:path>', ViewPonencia.as_view(), name='View_ponencia'),
    path('taller/<str:path>', ViewTaller.as_view(), name='View_taller'),
    path('sala/<str:path>', ViewSala.as_view(), name='View_sala'),
    path('ponencias_sala/<str:path>', ViewPonenciasSala.as_view(), name='View_ponencias_sala'),
    
    path('error404', ViewError404.as_view(), name='Error404'),
    path('error_openpay', ViewErrorOpenpay.as_view(), name='Error_openpay'),
    path('error_registrar', ViewErrorRegistrar.as_view(), name='ErrorRegistrar'),
    
    
    path('error_facturacion', ViewErrorFact.as_view(), name='Error_facturacion'),
    path('pagar_efectivo', PagarEfectivo.as_view(), name='Pagar_efectivo'),
    path('editar_perfil/<int:pk>', PerfilUpdateView.as_view(), name='Edit_perfil'),
    


    path('especialidades_autocomp', EspecialdiadesAutocomplete , name='Especialidades_autocomp'),
    path('user_autocomp', UserAutocomplete , name='User_autocomp'),
    path('ponente_autocomp', PonenteAutocomplete , name='Ponente_autocomp'),
    path('moderador_autocomp', ModeradorAutocomplete , name='Moderador_autocomp'),
    path('congreso_autocomp', CongresoAutocomplete , name='Congreso_autocomp'),
    path('taller_autocomp', TallerAutocomplete , name='Taller_autocomp'),
    path('ponencia_autocomp', PonenciaAutocomplete , name='Ponencia_autocomp'),
    
    path('patrocinador_autocomp', PatrocinadorAutocomplete , name='Patrocinador_autocomp'),
    path('socio_autocomp', SocioAutocomplete , name='Socio_autocomp'),
    path('add_cart', AddCart.as_view() , name='Add_cart'),
    path('add_cart_taller', AddCartTaller.as_view() , name='Add_cart_taller'),
    path('deleted_cart',DeletedCart.as_view() , name='Deleted_cart'),
    path('conf_cart',ConfCart.as_view() , name='Conf_cart'),
     path('view_cart',ViewCart.as_view() , name='View_cart'),
    path('aviso_privacidad',AvisoPrivacidad.as_view() , name='aviso_privacidad'),
    path('email',Email.as_view() , name='email'),
    # path('confic_email',ConfigEmail.as_view() , name='confic_email'),
    path('habilitar_user/<str:token>',HabilitarUser.as_view() , name='habilitar_user'),
    path('perfil',Perfil.as_view() , name='perfil'),
    path('perfil/congresos',PerfilCongresos.as_view() , name='perfil_congreso'),
    path('perfil/constancias',PerfilConstancias.as_view() , name='perfil_constancias'),
    
    path('transaccion_exitosa',PagoExitoso.as_view() , name='transaccion_exitosa'),
    path('get_perfil', GetPerfil.as_view() , name='GetPerfil'),
    path('get_contactos', GetContactos.as_view() , name='GetContactos'),
    
    path('get_factura', GetFactura.as_view() , name='Factura'),
    path('get_factura_prueba/<str:invoice>', GetFacturaPrueba.as_view() , name='FacturaPrueba'),
    path('cuestionario/congreso/<str:path>',GetCuestionario.as_view() , name='Cuestionario'),
    path('bloque/preguntas_respuestas/<str:path>',VideoBloque.as_view() , name='BloqueVideo'),
    path('constancia/congreso/<str:path>',SetConstancia.as_view() , name='Constancia'),
    path('evaluar/taller',EvaluarTaller.as_view() , name='EvaluarTaller'),
    path('reevaluar/taller',UpdateEvaluarTaller.as_view() , name='UpdateEvaluarTaller'),

      path('evaluar/ponencia',EvaluarPonencia.as_view() , name='EvaluarPonencia'),
    path('reevaluar/ponencia',UpdateEvaluarPonencia.as_view() , name='UpdateEvaluarPonencia'),

    
    path('cuestionario/resultado/<str:path>',Resultado_Cuestionario.as_view() , name='Resultado_Cuestionario'),
    path('ver_constancia/congreso/<str:path>',Get_Constancia.as_view() , name='Get_Constancia'),
    path('ver_transaccion',VerTransaccion.as_view() , name='ver_transaccion'),
    path('cambiar_pass',CambiarPass.as_view() , name='Cambiar_Pass'),
    path('registro_existoso',RegistroExitoso.as_view() , name='Registro_exitoso'),
    path('pago_existoso',PagoExitoso2.as_view() , name='Pago_exitoso'),
    
    path('mensaje_exitoso',ContactoExitoso.as_view() , name='mensaje_exitoso'),
    path('enviar',Enviar.as_view() , name='enviar'),
    path('webhook',Webhook , name='webhook'),
    path('trabajo/<str:path>', ViewTrabajo.as_view(), name='View_trabajo'),
    path('descargar/trabajo/<str:path>', DonwloadTrabajo.as_view(), name='Donwload_trabajo'),
    


    
    
    
  
]
