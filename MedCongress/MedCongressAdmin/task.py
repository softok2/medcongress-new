from celery import shared_task
from MedCongressApp.models import Congreso,RelCongresoUser
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from django.core.mail import EmailMessage

@shared_task
def Constancia(x,y):
    congreso=Congreso.objects.all().first()
    if congreso:
        rel_usuario_congreso=RelCongresoUser.objects.filter(congreso=congreso ).distinct('user')
        
        for usuario in rel_usuario_congreso:
                # //////////////
            nombre='%s %s'%(usuario.user.usuario.first_name,usuario.user.usuario.last_name)
            
            cont=len(nombre)
            comienzo=450-(cont/2*19) 
            base=Image.open('MedCongressApp/static/%s'%(congreso.foto_constancia)).convert('RGBA')
            text=Image.new('RGBA',base.size,(255,255,255,0))
            # nombre_font=ImageFont.truetype('calibri.ttf',40)
            nombre_font=ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans.ttf", 28, encoding="unic")
            # cong.set_variation_by_name('Italic')
            d=ImageDraw.Draw(text)
            d.text((comienzo,290),nombre,font=nombre_font,fill=(89, 85, 85))
            
            
            out=Image.alpha_composite(base,text)
            tit=congreso.titulo.replace("/","").replace(" ","-").replace("?","").replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("ñ","n")
            tit_nombre=nombre.replace("/","").replace(" ","-").replace("?","").replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("ñ","n")
            nombre_img='constancia_%s_%s'%(tit_nombre,tit)  
            out.save('MedCongressApp/static/congreso/img_constancia/%s.png'%(nombre_img))
            usuario.is_constancia=True
            usuario.foto_constancia='%s.png'%(nombre_img)
            usuario.fecha_constancia=datetime.now()
            usuario.save()
            # ////////////////
            if usuario.user.usuario.email == 'frankhef91@gmail.com':
                email = EmailMessage('Constancia', 'En este correo se le adjunta la constancia de haber participado en el congreso %s.'%(congreso.titulo), to = [usuario.user.usuario.email])
                email.attach_file('MedCongressApp/static/congreso/img_constancia/%s.png'%(nombre_img))
                email.send()



            # ////
#         return HttpResponse(Constancia.delay())
    return congreso.titulo   