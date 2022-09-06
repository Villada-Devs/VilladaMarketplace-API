import pytest
from django.test import Client
from rest_framework import status
from marketplace.models import Clothing
from marketplace.views.clothesView import ClothViewSet
from django.contrib.auth.models import User


from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from rest_framework.test import APIRequestFactory
from rest_framework.test import RequestsClient



@pytest.mark.django_db
def test_clothes():
    
    #factory = APIRequestFactory()
    #request = factory.get('/api/v1/marketplace/clothes/')
    #view = ClothViewSet.as_view()


    #token = Token.objects.get(user__email='gastonrancic04@gmail.com')
    #client = APIClient() # La APIClient clase admite la misma interfaz de solicitud que la Client clase estándar de Django. 

    #client.login(email = 'gastonrancic04@gmail.com', password = 'Laplazita123')
    #client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    User.objects.create(
        email = 'gastonrancic04@gmail.com',
        username = 'gastoneta',
        password = 'Laplazita123',
    )


    client = APIClient()

    response3 = client.post('/api/v1/register/',{
    "email": "gastonrancic04@gmail.com",
    "first_name": "gaston",
    "last_name": "rancic",
    "username": "gastoneta",
    "password1": "Laplazita123"
    }, format='json')

    response2 = client.post('/api/v1/login/', {'email': 'gastonranci04@gmail.com', 'password': 'Laplazita123'}, format='json')

    #client.login(email='gastonrancic04@gmail.com', password='Laplazita123')
    print(response2)

    response = client.get('/api/v1/marketplace/clothes/')
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    #assert response2.status_code == status.HTTP_200_OK  
    #assert response3.status_code == status.HTTP_201_CREATED


    
    

@pytest.mark.django_db
def test_list_clothes():

    client = Client() # es como un cliente que hace la peticion al navegador tiene un response

    response = client.get('/api/v1/marketplace/clothes/')
    print(response)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


    user = User.objects.create(
        email = 'gastonrancic04@gmail.com',
        username = 'gastoneta',
        password = 'Laplazita123',
    )
    cloth = Clothing.objects.create(
        type_of_cloth = 'bermuda',
        created_by = user,
        price = 150,
        tel = 3517059561,
        status = 'Casi nuevo'
    )
    assert cloth.type_of_cloth == 'bermuda'

