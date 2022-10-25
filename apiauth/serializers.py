#import al libs that are needed

from django.urls import exceptions as url_exceptions
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from django.contrib.auth.models import User
from allauth.account import app_settings as allauth_settings
from allauth.utils import email_address_exists
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from string import printable
import re
from django.contrib.auth.models import User

#register serializer override to customize the fields
class RegisterSerializer(serializers.Serializer):
    """
    Serializer for user registration
    """
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    first_name = serializers.CharField(required=True, write_only=True)
    last_name = serializers.CharField(required=True, write_only=True)
    username = serializers.CharField(required=True, write_only=True)
    password1 = serializers.CharField(required=True, write_only=True)

    #validate that the username chosen is unique
    def validate_username(self, username):
        if User.objects.filter(username = username).exists():
            raise serializers.ValidationError({"Error": "A user is already registered with Username."})
        
        return username

    #validate unique email
    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError({"Error": "A user is already registered with this e-mail address."})
        return email
    
    #validate that first name does not contain special characters
    def validate_first_name(self, first_name):
        first_name.split()
        counter=0
        special_chars='[@_123456"7890!#[]-$%^&*()<>?/\|.}{~:;^`]' 
        for i in range(len(first_name)):
            
            if first_name[i] in special_chars:
                counter+=1   
          
        if counter:
            raise serializers.ValidationError({"Error": "First name contains special characters, please remove them"})
        
        return first_name

    #validate that last name does not contain special characters
    def validate_last_name(self, last_name):
        last_name.split()
        counter=0
        special_chars='[@_123456"7890!#[]-$%^&*()<>?/\|.}{~:;^`]' 
        for i in range(len(last_name)):
            
            if last_name[i] in special_chars:
                counter+=1   
          
        if counter:
            raise serializers.ValidationError({"Error": "Last name contains special characters, please remove them"})
        
        return last_name
    
    #this method get the data cleaned and validated from the serializer
    def get_cleaned_data(self):
        return {
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'username': self.validated_data.get('username','')
        }
    
    #this method create a new uset with the cleaned data, after that configure an email in Email addres table 
    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        user.save()
        return user

# This serializer manage the user information detail, in this case we are overriding it to return custom fields
#the library dj-rest-auth and allauth use this serializer inherited in many responses, for example in login response
# when you get logged on you get the token and the data set in this serializer, also  in /user url
class CustomUserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'first_name','last_name','username', 'email', 'is_staff')
        read_only_fields = ('email', 'is_staff', 'pk')
