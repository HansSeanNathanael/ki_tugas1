from django.http.request import HttpRequest
from django.contrib.auth.backends import BaseBackend

from .models import User

class AuthBackend(BaseBackend):
    def authenticate(self, request : HttpRequest, username : str, password : str):
        
        user = User.objects.filter(username=username).first()
        if user is None:
            return None
        
        if user.check_password(password):
            return user
        return None
    
    def get_user(self, id : str):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            return None