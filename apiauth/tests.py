from django.test import TestCase
import email
from urllib import request
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from allauth.account.admin import EmailAddress
from allauth.account.signals import email_confirmed

class SetUpTest(APITestCase):
    def setUp(self):
        self.register_url = 'http://localhost:8000/api/v1/register/'
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
        
        EmailAddress.objects.filter(email = 'dev@gmail.com').update(verified = True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=response.data)

    
        self.login_url = 'http://localhost:8000/api/v1/login/'
        response = self.client.post(
            self.login_url,
            {
                'email' : 'dev@gmail.com',
                'password' : 'holamundo123',
            },
            format = 'json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg = response.data)
        
        self.token = response.data['access_token']
        self.client.credentials(HTTP_AUTHORIZATION = 'Bearer' + self.token)
        return super().setUp()
    
    def test_runner(self):
        print(self.token)
