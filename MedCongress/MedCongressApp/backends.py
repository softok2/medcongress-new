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