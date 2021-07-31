from celery import shared_task
from MedCongressApp.models import Congreso,RelCongresoUser,Taller,RelTallerUser,User,BecasPendientes
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from django.core.mail import EmailMessage
from MedCongressApp.claves import URL_SITE
import re
@shared_task
def Constancia(titulo):
    congreso=Congreso.objects.get(pk=titulo)
    
    if congreso:
        rel_usuario_congreso=RelCongresoUser.objects.filter(congreso=congreso,is_pagado=True ).exclude(is_constancia=True).distinct('user')
        
        for usuario in rel_usuario_congreso:
            if not RelCongresoUser.objects.filter(user=usuario.user,is_constancia=True,congreso=congreso).exists():    # //////////////
                nombre='%s %s'%(usuario.user.usuario.first_name,usuario.user.usuario.last_name)
                
                cont=len(nombre)
                comienzo=1500-(cont/2*19) 
                base=Image.open('MedCongressApp/static/%s'%(congreso.foto_constancia)).convert('RGBA')
                text=Image.new('RGBA',base.size,(255,255,255,0))
                # nombre_font=ImageFont.truetype('calibri.ttf',150)
                nombre_font=ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans.ttf", 100, encoding="unic")
                # cong.set_variation_by_name('Italic')
                d=ImageDraw.Draw(text)
                d.text((comienzo,1200),nombre,font=nombre_font,fill=(89, 85, 85))
                
                
                out=Image.alpha_composite(base,text)
                tit=congreso.titulo.replace("/","").replace(" ","-").replace("?","").replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("ñ","n").replace(",","-").replace(":","-")
                tit_nombre=nombre.replace("/","").replace(" ","-").replace("?","").replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("ñ","n").replace(",","-").replace(":","-")
                nombre_img='constancia_%s_%s'%(tit_nombre,tit)
                imagen_pdf=out.convert('RGB')  
                imagen_pdf.save('MedCongressApp/static/congreso/img_constancia/%s.pdf'%(nombre_img[0:50]))
                
                usuario.is_constancia=True
                usuario.foto_constancia='%s.pdf'%(nombre_img[0:50])
                usuario.fecha_constancia=datetime.now()
                if not RelCongresoUser.objects.filter(congreso=congreso, user=usuario.user, is_constancia=True ).exists():
                    score=0
                    if congreso.score:
                        score=congreso.score
                    if usuario.user.score is None:
                        usuario.user.score=score
                    else:
                        usuario.user.score= usuario.user.score+score
                    usuario.user.save()
                usuario.save()                               
                # ////////////////
            
                email = EmailMessage('Constancia', 'En este correo se le adjunta la constancia de haber participado en el congreso %s.'%(congreso.titulo), to = [usuario.user.usuario.email])
                email.attach_file('MedCongressApp/static/congreso/img_constancia/%s.pdf'%(nombre_img[0:50]))
                email.send()



            # ////  
#         return HttpResponse(Constancia.delay())
    return congreso.titulo  

@shared_task
def Constanciataller(titulo):
    taller=Taller.objects.get(pk=titulo)
    if taller:
        rel_usuario_congreso=RelTallerUser.objects.filter(taller=taller,is_pagado=True ).exclude(is_constancia=True).distinct('user')
        
        for usuario in rel_usuario_congreso:
            if not RelTallerUser.objects.filter(user=usuario.user,is_constancia=True,taller=taller).exists():      # //////////////
                nombre='%s %s'%(usuario.user.usuario.first_name,usuario.user.usuario.last_name)
                
                cont=len(nombre)
                comienzo=1500-(cont/2*19) 
                base=Image.open('MedCongressApp/static/%s'%(taller.foto_constancia)).convert('RGBA')
                text=Image.new('RGBA',base.size,(255,255,255,0))
                #nombre_font=ImageFont.truetype('calibri.ttf',150)
                nombre_font=ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans.ttf", 100, encoding="unic")
                # cong.set_variation_by_name('Italic')
                d=ImageDraw.Draw(text)
                d.text((comienzo,1200),nombre,font=nombre_font,fill=(89, 85, 85))
                
                
                out=Image.alpha_composite(base,text)
                tit=taller.titulo.replace("/","").replace(" ","-").replace("?","").replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("ñ","n").replace(",","-").replace(":","-")
                tit_nombre=nombre.replace("/","").replace(" ","-").replace("?","").replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("ñ","n").replace(",","-").replace(":","-")
                nombre_img='constancia_%s_%s'%(tit_nombre,tit)
                imagen_pdf=out.convert('RGB')  
                imagen_pdf.save('MedCongressApp/static/congreso/img_constancia/%s.pdf'%(nombre_img[0:50]))
                
                usuario.is_constancia=True
                usuario.foto_constancia='%s.pdf'%(nombre_img[0:50])
                usuario.fecha_constancia=datetime.now()
                if not RelTallerUser.objects.filter(taller=taller, user=usuario.user, is_constancia=True ).exists():
                    score=0
                    if taller.score:
                        score=taller.score
                    if usuario.user.score is None:
                        usuario.user.score=score
                    else:
                        usuario.user.score= usuario.user.score+score
                    usuario.user.save()
                usuario.save()                               
            # ////////////////
           
#             email = EmailMessage('Constancia', '''Estimado asistente al Simposio AMCIC 2020,

 

# Por medio del presente, se envía la constancia de asistencia al  taller  del Simposio el cual esperamos haya sido de tu interés y agrado. Recuerda que tienes acceso a las presentaciones del simposio a través de la plataforma de MedCongress, solo tienes que ingresar a la página https://medcongress.com.mx/ y en login ingresar tu correo electrónico y tu contraseña, dentro del programa podrás elegir las ponencias de tu interés que deseas ver.

 

# Si tienes problemas para ingresar a la plataforma, por favor comunícate con nosotros para ayudarte a solucionar tu ingreso.

 

# Recibirás una encuesta de satisfacción en las próximas semanas, te agradeceremos tus comentarios.

 

# Nos vemos en el 2° Simposio en Ciencias de la Salud AMCIC 2021, el cual se llevará a cabo en el último trimestre del año, modalidad virtual!''', to = [usuario.user.usuario.email])
#             email.attach_file('MedCongressApp/static/congreso/img_constancia/%s.pdf'%(nombre_img[0:50]))
#             email.send()



            # ////  
#         return HttpResponse(Constancia.delay())
    return taller.titulo 
@shared_task
def AsignarBeca(exel):
    respuesta='ok'
    for row in exel:
        
        if  not row['Congreso'] or not row['Correo']:
            continue
        correo=str(row['Correo']).strip()
        congreso=Congreso.objects.filter(titulo=row['Congreso']).first()
        if not congreso:
            respuesta='congreso'   
            continue
        if not re.match('^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$',correo.lower()):
            respuesta='usuario'
            continue
        user=User.objects.filter(email=correo).first()
        if user:
            if not RelCongresoUser.objects.filter(user=user.perfilusuario,congreso=congreso,is_beca=True).exists():
                rel_congreso_user=RelCongresoUser(user=user.perfilusuario,congreso=congreso,is_beca=True,is_pagado=True,cantidad=1)
                rel_congreso_user.save()
                email = EmailMessage('Beca en MedCongress', '''Estimado(a) profesional de la salud, le informamos que se le ha asignado una beca para el %s1 .

        1.- Para acceder tendrá que autenticarse en el siguiente enlace %s/accounts/login/?next=/congreso/%s

        2.- Vaya a su perfil y elija la opción “Mis Congresos” donde visualizara el congreso asignado'''%(congreso.titulo,URL_SITE,congreso.path), to = [correo])
                email.send()
        else:
            if not BecasPendientes.objects.filter(email=correo,congreso=congreso).exists():
                beca_pendiente=BecasPendientes(email=correo,congreso=congreso)  
                beca_pendiente.save()
                email = EmailMessage('Beca en MedCongress', '''Estimado(a) profesional de la salud, le informamos que se le ha asignado una beca para el %s.
        1.- Para acceder tendrá que registrarse en el siguiente enlace %s/registrarse?email=%s

        2.- En su perfil elija la opción “Mis Congresos” donde podrá confirmar el evento asignado

        3.- una vez registrado, de clic en el siguiente enlace para acceder al congreso.
            %s/congreso/%s'''%(congreso.titulo,URL_SITE,correo,URL_SITE,congreso.path), to = [correo])

            email.send()
    return respuesta   