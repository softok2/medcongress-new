from celery import shared_task
from MedCongressApp.models import Congreso,RelCongresoUser,Taller,RelTallerUser,User
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from django.core.mail import EmailMessage

@shared_task
def Constancia(titulo):
    congreso=Congreso.objects.get(pk=titulo)
    
    if congreso:
        rel_usuario_congreso=RelCongresoUser.objects.filter(congreso=congreso,is_pagado=True ).exclude(is_constancia=True).distinct('user')
        
        for usuario in rel_usuario_congreso:
            if not RelCongresoUser.objects.filter(user= .user,is_constancia=True,congreso=congreso).exists():    # //////////////
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
    for row in exel:
        user=Use
    return exel