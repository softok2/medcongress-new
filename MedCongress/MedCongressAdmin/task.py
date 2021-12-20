from celery import shared_task
from MedCongressApp.models import Organizador,ConstanciaUsuario,Congreso,RelCongresoUser,RelBloqueModerador,Bloque,Taller,RelTallerUser,User,BecasPendientes,Ponencia,RelPonenciaPonente
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from django.core.mail import EmailMessage
from MedCongressApp.claves import URL_SITE
import re
from MedCongress.settings import BASE_FONT
@shared_task
def Constancia(titulo,t_user,folio_ini,folio_fin,folio_dis):
    congreso=Congreso.objects.get(pk=titulo)
    t_user=int(t_user)
    if folio_ini:
        folio_ini=int(folio_ini)
        folio_fin=int(folio_fin) 
    folio=folio_ini
    if congreso:
        if t_user==1:
            rel_usuario_congreso=RelCongresoUser.objects.filter(congreso=congreso,is_pagado=True,is_constancia=False ).distinct('user') 
            folio=folio_ini
            for usuario in rel_usuario_congreso:   
                nombre='%s %s'%(usuario.user.usuario.first_name,usuario.user.usuario.last_name)
                cont=len(nombre)
                comienzo=1500-(cont/2*19) 
                base=Image.open('MedCongressApp/static/%s'%(congreso.foto_constancia)).convert('RGBA')
                text=Image.new('RGBA',base.size,(255,255,255,0))
                # nombre_font=ImageFont.truetype('calibri.ttf',150)
                nombre_font=ImageFont.truetype(BASE_FONT, 100, encoding="unic")
                # cong.set_variation_by_name('Italic')
                if folio_ini :
                    usuario.folio_constancia=folio_dis.replace('#',str(folio))
                    # folio_font=ImageFont.truetype('calibri.ttf',100)
                    folio_font=ImageFont.truetype(BASE_FONT, 100, encoding="unic")
                    c=ImageDraw.Draw(text)
                    c.text((300,1025),str(folio_dis.replace('#',str(folio))),font=folio_font,fill=(89, 85, 85))
                    folio=folio+1
                    
                d=ImageDraw.Draw(text)
                d.text((comienzo,1200),nombre,font=nombre_font,fill=(89, 85, 85))
                out=Image.alpha_composite(base,text)
                tit=congreso.titulo.replace("/","").replace(" ","-").replace("?","").replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("ñ","n").replace(",","-").replace(":","-")
                tit_nombre=nombre.replace("/","").replace(" ","-").replace("?","").replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("ñ","n").replace(",","-").replace(":","-")
                nombre_img='constancia_%s_%s'%(tit_nombre,tit)
                imagen_pdf=out.convert('RGB')  
                imagen_pdf.save('MedCongressApp/static/congreso/img_constancia/%s_participante.pdf'%(nombre_img[0:50]))
                
                usuario.is_constancia=True
                usuario.foto_constancia='%s_participante.pdf'%(nombre_img[0:50])
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
                email.attach_file('MedCongressApp/static/congreso/img_constancia/%s_participante.pdf'%(nombre_img[0:50]))
                email.send()
            if folio_ini:
                return {'success':True,'mensaje':'Se asignaron satifactoriamente todas las <b>constancias a los Participantes del Congreso Seleccionado</b>.<br> Se asignó hasta el folio <b>%s </b>'%(folio_dis.replace('#',str(folio-1)))}
                
            else:
                return {'success':True,'mensaje':'Se asignaron satifactoriamente todas las <b>constancias a los Participantes del Congreso Seleccionado</b>'}
        
        elif t_user==2:
            ponentes=congreso.Ponentes_sin_constancias()
            folio=folio_ini
            for ponente in ponentes:
                nombre='%s %s'%(ponente.user.usuario.first_name,ponente.user.usuario.last_name)
                cont=len(nombre)
                comienzo=1500-(cont/2*19) 
                base=Image.open('MedCongressApp/static/%s'%(congreso.foto_const_ponente)).convert('RGBA')
                text=Image.new('RGBA',base.size,(255,255,255,0))
                # nombre_font=ImageFont.truetype('calibri.ttf',150)
                if folio :
                    folio_font=ImageFont.truetype(BASE_FONT, 100, encoding="unic")
                    # folio_font=ImageFont.truetype('calibri.ttf',100)
                    c=ImageDraw.Draw(text)
                    c.text((300,1025),str(folio_dis.replace('#',str(folio))),font=folio_font,fill=(89, 85, 85))
                nombre_font=ImageFont.truetype(BASE_FONT, 100, encoding="unic")
                # cong.set_variation_by_name('Italic')
                d=ImageDraw.Draw(text)
                d.text((comienzo,1200),nombre,font=nombre_font,fill=(89, 85, 85))
                out=Image.alpha_composite(base,text)
                tit=congreso.titulo.replace("/","").replace(" ","-").replace("?","").replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("ñ","n").replace(",","-").replace(":","-")
                tit_nombre=nombre.replace("/","").replace(" ","-").replace("?","").replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("ñ","n").replace(",","-").replace(":","-")
                nombre_img='constancia_%s_%s'%(tit_nombre,tit)
                imagen_pdf=out.convert('RGB')  
                imagen_pdf.save('MedCongressApp/static/congreso/img_constancia/%s_ponente.pdf'%(nombre_img[0:50]))
                folio_constancia=None
                if folio:
                    folio_constancia=folio_dis.replace('#',str(folio))
               
                constancia=ConstanciaUsuario(user=ponente.user.usuario,congreso=congreso,fecha_constancia=datetime.now(),folio_constancia=folio_constancia,tipo_constancia='Ponente',foto_constancia='%s_ponente.pdf'%(nombre_img[0:50]))
                constancia.save() 
                email = EmailMessage('Constancia', 'En este correo se le adjunta la constancia de haber participado como Ponente en el congreso %s.'%(congreso.titulo), to = [ponente.user.usuario.email])
                email.attach_file('MedCongressApp/static/congreso/img_constancia/%s_ponente.pdf'%(nombre_img[0:50]))
                email.send()
                if folio :
                    folio=folio+1
            if folio_ini:
                return {'success':True,'mensaje':'Se asignaron satifactoriamente todas las <b>constancias a los Ponentes del Congreso Seleccionado</b>.<br> Se asignó hasta el folio <b> %s </b>'%(folio_constancia)}
                
            else:
                return {'success':True,'mensaje':'Se asignaron satifactoriamente todas las <b>constancias a los Ponentes del Congreso Seleccionado</b>.'}
        
        elif t_user==3:
            moderadores=congreso.Moderadores_sin_constancias()   
            folio=folio_ini
            for moderador in moderadores:
                nombre='%s %s'%(moderador.user.usuario.first_name,moderador.user.usuario.last_name)
                cont=len(nombre)
                comienzo=1500-(cont/2*19) 
                base=Image.open('MedCongressApp/static/%s'%(congreso.foto_const_moderador)).convert('RGBA')
                text=Image.new('RGBA',base.size,(255,255,255,0))
                # nombre_font=ImageFont.truetype('calibri.ttf',150)
                if folio :
                    # folio_font=ImageFont.truetype('calibri.ttf',100)
                    folio_font=ImageFont.truetype(BASE_FONT, 100, encoding="unic")
                    c=ImageDraw.Draw(text)
                    c.text((300,1025),str(folio_dis.replace('#',str(folio))),font=folio_font,fill=(89, 85, 85))
                nombre_font=ImageFont.truetype(BASE_FONT, 100, encoding="unic")
                # cong.set_variation_by_name('Italic')
                d=ImageDraw.Draw(text)
                d.text((comienzo,1200),nombre,font=nombre_font,fill=(89, 85, 85))
                out=Image.alpha_composite(base,text)
                tit=congreso.titulo.replace("/","").replace(" ","-").replace("?","").replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("ñ","n").replace(",","-").replace(":","-")
                tit_nombre=nombre.replace("/","").replace(" ","-").replace("?","").replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("ñ","n").replace(",","-").replace(":","-")
                nombre_img='constancia_%s_%s'%(tit_nombre,tit)
                imagen_pdf=out.convert('RGB')  
                imagen_pdf.save('MedCongressApp/static/congreso/img_constancia/%s_moderador.pdf'%(nombre_img[0:50]))
                
                constancia_user=ConstanciaUsuario.objects.filter(congreso=congreso,user=moderador.user.usuario,tipo_constancia='Moderador').first()
                folio_constancia=None
                if folio:
                    folio_constancia=folio_dis.replace('#',str(folio))
                constancia=ConstanciaUsuario(user=moderador.user.usuario,congreso=congreso,fecha_constancia=datetime.now(),folio_constancia=folio_constancia,tipo_constancia='Moderador',foto_constancia='%s_moderador.pdf'%(nombre_img[0:50]))
                constancia.save() 
                email = EmailMessage('Constancia', 'En este correo se le adjunta la constancia de haber participado como Moderador en el congreso %s.'%(congreso.titulo), to = [moderador.user.usuario.email])
                email.attach_file('MedCongressApp/static/congreso/img_constancia/%s_moderador.pdf'%(nombre_img[0:50]))
                email.send()
                if folio :
                    folio=folio+1
            if folio_ini:
                return {'success':True,'mensaje':'Se asignaron satifactoriamente todas las <b>constancias a los Moderadores del Congreso Seleccionado</b>.<br> Se asignó hasta el folio <b>%s</b>'%(folio_constancia)}
                
            else:
                return {'success':True,'mensaje':'Se asignaron satifactoriamente todas las <b>constancias a los Moderadores del Congreso Seleccionado</b>'}
            
    else:
        return  {'success':False,'mensaje':'No existe ese Congreso'} 

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
           
    return taller.titulo 
@shared_task
def AsignarBeca(exel,user_id):
    respuesta='ok'
    
    for row in exel:
        
        if  not row['Congreso'] or not row['Correo']:
            continue
        correo=str(row['Correo']).strip()
        congreso=Congreso.objects.filter(titulo=row['Congreso']).first()
        if not congreso:
            respuesta='congreso'   
            continue
        usuario=User.objects.get(pk=user_id)
        if not usuario.is_staff and not Organizador.objects.filter(congreso=congreso,user=usuario.perfilusuario).exists():
            respuesta='no_permiso'
        if not re.match('^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$',correo.lower()):
            respuesta='usuario'
            continue
        user=User.objects.filter(email=correo).first()
        if user:
            if not RelCongresoUser.objects.filter(user=user.perfilusuario,congreso=congreso,is_beca=True).exists():
                rel_congreso_user=RelCongresoUser(user=user.perfilusuario,congreso=congreso,is_beca=True,is_pagado=True,cantidad=1)
                rel_congreso_user.save()
                email = EmailMessage('Beca en MedCongress', '''Estimado(a) profesional de la salud, le informamos que se le ha asignado: %s.

        1.- Para acceder tendrá que autenticarse en el siguiente enlace %s/accounts/login/?next=/congreso/%s

        2.- Vaya a su perfil y elija la opción “Mis Congresos” donde visualizara el congreso asignado'''%(congreso.titulo,URL_SITE,congreso.path), to = [correo])
                email.send()
        else:
            if not BecasPendientes.objects.filter(email=correo,congreso=congreso).exists():
                beca_pendiente=BecasPendientes(email=correo,congreso=congreso)  
                beca_pendiente.save()
                email = EmailMessage('Beca en MedCongress', '''Estimado(a) profesional de la salud, le informamos que se le ha asignado: %s.
        1.- Para acceder tendrá que registrarse en el siguiente enlace %s/registrarse?email=%s

        2.- En su perfil elija la opción “Mis Congresos” donde podrá confirmar el evento asignado

        3.- una vez registrado, de clic en el siguiente enlace para acceder al congreso.
            %s/congreso/%s'''%(congreso.titulo,URL_SITE,correo,URL_SITE,congreso.path), to = [correo])

                email.send()
    return respuesta   