import json
import requests
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
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
            cap_url="http://www.google.com/recaptcha/api/siteverify"
            cap_secret="6Ld6FyEaAAAAAGggch470Ybh9GHS1Mu3dhz9IT3P"
            cap_data={"secret":cap_secret,"response":captcha_token}
            cap_server_response=requests.post(url=cap_url,data=cap_data)
            cap_json=json.loads(cap_server_response.text)
            if cap_json['success']==False:
                return None
               
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
                return None
    def get_user(self, user_id):
       
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None