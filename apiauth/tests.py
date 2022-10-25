#import needed libs
from http import client
from django.test import TestCase
from urllib import request
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from allauth.account.admin import EmailAddress
from allauth.account.signals import email_confirmed
from rest_framework.test import APIClient

#set up test is executed before any other test, it create an user, authenticate it and return a token.
#with this token we can make all the others unitests
class SetUpTest(APITestCase):
    def setUp(self):
        self.register_url = 'http://localhost:8000/api/v1/register/'
        self.client = APIClient()
        response = self.client.post(
            self.register_url,
            {
                'email' : 'dev@gmail.com',
                'first_name' : 'Developer',
                'last_name' : 'Developer',
                'username' : 'Developer',
                'password1' : 'holamundo123',
            },
            format = 'json',
        )
        #verify the account
        EmailAddress.objects.filter(email = 'dev@gmail.com').update(verified = True)
        #check that the register response is correct
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=response.data)

        self.client = APIClient()

        self.login_url = 'http://localhost:8000/api/v1/login/'
        response = self.client.post(
            self.login_url,
            {
                'email' : 'dev@gmail.com',
                'password' : 'holamundo123',
            },
            format = 'json',
        )
        #check login response with user previously registered
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg = response.data)
        self.token = response.data['access_token']
        
    def test_runner(self):
        print(self.token)