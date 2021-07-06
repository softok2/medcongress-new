import json
import requests
from .models import Carrito,Session,RelCongresoCategoriaPago,RelTalleresCategoriaPago
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import login as do_login
from datetime import date,datetime
from .cart import Cart
User = get_user_model()

class EmailAuthBackend(ModelBackend):
    """
    Email Authentication Backend    Permite a un usuario acceder utilizando su correo electrónico y
    contraseña. Si la autenticación falla, lo intenta con el par
    usuario/contraseña.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            captcha_token=request.POST.get("g-recaptcha-response")
            cap_url="https://www.google.com/recaptcha/api/siteverify"
            cap_secret="6Ld6FyEaAAAAAGggch470Ybh9GHS1Mu3dhz9IT3P"
            cap_data={"secret":cap_secret,"response":captcha_token}
            cap_server_response=requests.post(url=cap_url,data=cap_data)
            cap_json=json.loads(cap_server_response.text)
            if cap_json['success']==False:
                return None
               
               
            user = User.objects.get(email=username)
            if user.check_password(password):
                session=Session(usuario=user,fecha_inicio=datetime.now())
                session.save()
                cart=[{'cant':0},[]]
                carritos= Carrito.objects.filter(usuario=user)
                if carritos:
                    pagar=0
                    for carrito in carritos:
                        cart[1].append(
                        {
                            'mi_id':carrito.pk,
                            'id':carrito.id_cat_pago,
                            'tipo_evento':carrito.tipo_evento,
                            'id_congreso':carrito.id_evento,
                            'nombre_congreso':carrito.nombre_congreso,
                            'id_cat_pago':carrito.id_cat_pago,
                            'nombre_cat_pago':carrito.nombre_cat_pago,
                            'precio':carrito.precio,
                            'pagar':carrito.pagar,
                            'moneda':carrito.moneda,
                            'cantidad': carrito.cantidad
                        }
                        )
                        pagar=pagar+carrito.pagar
                    cart[0]['cant']=pagar
                    request.session["cart"]=cart
                do_login(request, user)
                if request.POST.get("tipo"):
                    car=Cart(request)
                    cantidad=request.POST.get("cantidad")
                    if request.POST.get("tipo")=='congreso':
                        
                        evento_cat_pago=RelCongresoCategoriaPago.objects.get(pk=request.POST.get("cat_pago"))
                        result=car.add_evento(relCongresoCategoriaPago=evento_cat_pago,cant=cantidad)
                    if request.POST.get("tipo")=='taller':
                        evento_cat_pago=RelTalleresCategoriaPago.objects.get(pk=request.POST.get("cat_pago"))
                        result=car.add_taller(relTallerCategoriaPago=evento_cat_pago,cant=cantidad) 
                return user
        except User.DoesNotExist:
                return None
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    
    