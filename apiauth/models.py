from django.db import models
from django.contrib.auth.models import User

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import import_string

class Event(models.Model):
    create_by = models.ForeignKey(User, on_delete= models.CASCADE)
    title = models.CharField(max_length=30)
    body = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="images")
    event_date = models.DateTimeField()


def get_token_model():
    default_model = 'rest_framework.authtoken.models.Token'
    import_path = getattr(settings, 'REST_AUTH_TOKEN_MODEL', default_model)
    session_login = getattr(settings, 'REST_SESSION_LOGIN', True)
    use_jwt = getattr(settings, 'REST_USE_JWT', False)
    
    if not any((session_login, import_path, use_jwt)):
        raise ImproperlyConfigured(
            'No authentication is configured for rest auth. You must enable one or '
            'more of `REST_AUTH_TOKEN_MODEL`, `REST_USE_JWT` or `REST_SESSION_LOGIN`'
      )
    if (
        import_path == default_model
        and 'rest_framework.authtoken' not in settings.INSTALLED_APPS
    ):
        raise ImproperlyConfigured(
            'You must include `rest_framework.authtoken` in INSTALLED_APPS '
            'or set REST_AUTH_TOKEN_MODEL to None'
        )
    return import_string(import_path) if import_path else None

TokenModel = get_token_model()
