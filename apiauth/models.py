from email.policy import default
from django.db import models
from platformdirs import user_cache_dir
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE, related_name = 'profile_image')
    image = models.ImageField(default="images/default-avatar.png", upload_to="images")
    
    def __str__(self) -> str:
        return f'Perfil de {self.user.username}'
