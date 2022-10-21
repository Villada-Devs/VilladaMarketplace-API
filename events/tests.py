from apiauth.tests import *
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

# Create your tests here.
class TestEvent(SetUpTest):
    #Este test case toma un usuario que no esta verificado, es decir is_staff = False
    def test_event_post_by_generic_user(self):
        self.events_url = 'http://localhost:8000/api/v1/events/'
        client = APIClient()
        client.credentials(AUTHORIZATION=f'JWT {self.token}')       
        response = self.client.post(
            self.events_url,
            {
                'title' : 'Titulo de ejemplo',
                'body' : 'holamundo123',
            },
            format = 'json',
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, msg = response.data)

    #este caso testea que la respuesta en el get a eventos sea correcta
    def test_event_get_by_logged_user(self):
        self.events_url = 'http://localhost:8000/api/v1/events/'
        response = self.client.get(
            self.events_url,
            format = 'json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg = response.data)
    
    def test_event_get_by_no_logged_user(self):
        self.events_url = 'http://localhost:8000/api/v1/events/'
        self.client = APIClient()
        response = self.client.get(
            self.events_url,
            format = 'json',
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, msg = response.data)


    
    def test_event_post_by_admin(self):
        self.events_url = 'http://localhost:8000/api/v1/events/'
        User.objects.filter(email = 'dev@gmail.com').update(is_staff = True)
        response = self.client.post(
            self.events_url,
            {
                'title' : 'Titulo de ejemplo',
                'body' : 'holamundo123',
                'short_description' : 'descripcion corta',
                'short_description' : 'descripcion corta',
                'event_date' : '2022-10-20T15:11:31Z',
                'event_type' : 'Bienvenida a familias de primer año',
                'uploaded_images' : ''
            },
            format = 'json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg = response.data)