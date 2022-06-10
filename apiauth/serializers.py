from multiprocessing import Pool
from venv import create
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.urls import exceptions as url_exceptions
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions, serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.generics import CreateAPIView
from rest_framework.generics import DestroyAPIView
from rest_framework.generics import UpdateAPIView
from django.contrib.auth.models import User
from .models import Event
from allauth.account import app_settings as allauth_settings
from allauth.utils import email_address_exists
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
import re

#UPF API

class EventsSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="created_by.username", read_only=True)
    class Meta:
        model = Event
        fields = ['id','author','title', 'body', 'created_date','image', 'event_date']

class poolsSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="created_by.username", read_only=True)       
    class Meta:
        model = Pool
        fields = ['id', 'author','locality']

# AUTH API
#register serializer override
class RegisterSerializer(serializers.Serializer):
    """
    Serializer for user registration
    """
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    first_name = serializers.CharField(required=True, write_only=True)
    last_name = serializers.CharField(required=True, write_only=True)
    username = serializers.CharField(required=True, write_only=True)
    password1 = serializers.CharField(required=True, write_only=True)

    def validate_username(self, username):
        if User.objects.filter(username = username).exists():
            raise serializers.ValidationError("A user is already registered with this username")
        return username


    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        domain = email.split('@')[1]
        if not domain == 'itsv.edu.ar':
            raise serializers.ValidationError('The email must be from itsv.edu.ar domain')

        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _("A user is already registered with this e-mail address."))
        return email
    
    

    def get_cleaned_data(self):
        return {
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'username': self.validated_data.get('username','')
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        user.save()
        return user


