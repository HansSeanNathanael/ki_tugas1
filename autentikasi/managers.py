import uuid

from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

class EncryptionUserManager(BaseUserManager):
    
    def create_user(self, username : str, password : str, **extra_fields):
        if username is None:
            raise ValueError(_('Username tidak boleh kosong'))
        
        user = self.model(id=uuid.uuid4(), username=username, **extra_fields)
        user.set_password(password)
        user.save()
        
        return user