#allauth
from multiprocessing import Pool, context
from allauth.account.views import ConfirmEmailView
from allauth.account.models import EmailAddress
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from pyparsing import empty
from requests import request
from rest_framework import status, viewsets
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Event, Pool
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import GenericViewSet
from dj_rest_auth.registration.serializers import (
    VerifyEmailSerializer, ResendEmailVerificationSerializer
)
from dj_rest_auth.views import LoginView
from apiauth.serializers import EventsSerializer, poolsSerializer

#google login test
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

#auth override functions

class VerifyEmailView(APIView, ConfirmEmailView):
    permission_classes = (AllowAny,)
    allowed_methods = ('POST', 'OPTIONS', 'HEAD')

    def get_serializer(self, *args, **kwargs):
        return VerifyEmailSerializer(*args, **kwargs)

    def get(self, *args, **kwargs):
        raise MethodNotAllowed('GET')

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.kwargs['key'] = serializer.validated_data['key']
        confirmation = self.get_object()
        confirmation.confirm(self.request)
        return Response({'detail': _('ok')}, status=status.HTTP_200_OK)

class ResendEmailVerificationView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ResendEmailVerificationSerializer
    queryset = EmailAddress.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = EmailAddress.objects.filter(**serializer.validated_data).first()
        if email and not email.verified:
            email.send_confirmation(request)

        return Response({'detail': _('email sent')}, status=status.HTTP_200_OK)

# API (EVENTS, POOLS)

class EventsViewSet(viewsets.ViewSet):
    """
    GET (List all events, all users can list)
    """
    def list(self, request):
        queryset = Event.objects.all()
        EventSerializer = EventsSerializer(queryset, many=True)
        return Response(EventSerializer.data)

    """
    POST (Create event only admin can post)
    """   
    def post(self, request):
        user_state = request.user.is_staff
        if user_state == True:
            serializer = EventsSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save(created_by = self.request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error' : 'Authorization Required'}, status=status.HTTP_401_UNAUTHORIZED)
    
class EventsDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = EventsSerializer
    lookup_field =  "id"
    
    def get_queryset(self):
        return Event.objects.filter()

    """
    DELETE (delete an event passing ID, only admin can delete)
    """
    def destroy(self, request, *args, **kwargs):
        user_state = request.user.is_staff
        if user_state == True:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({'ok' : 'Event deleted succesfully'},status=status.HTTP_200_OK)
        else:
            return Response({'error' : 'Authorization Required'}, status=status.HTTP_401_UNAUTHORIZED)

    """
    PATCH (update an event passing ID, only admin can delete)
    """
    def update(self, request, *args, **kwargs):
        user_state = request.user.is_staff
        if user_state == True:
            return super().update(request, *args, **kwargs)

        else:
            return Response({'error' : 'Authorization Required'}, status=status.HTTP_401_UNAUTHORIZED)


class poolsListView(viewsets.ViewSet):

    """
    LIST (retrieve a list of all pools, if a user id is sent in the url retrieve user pools list)
    """
    def list(self, request):
        user = request.GET.get('created_by')
        queryset = Pool.objects.all()
        if user:
            if str(request.user.id) != user:
                print(request.user.id, user)
                return Response({'error' : 'You can not see the pool list from other user'}, status=status.HTTP_401_UNAUTHORIZED)
            queryset = queryset.filter(created_by=user)
        
        serializer = poolsSerializer(queryset, many=True)
        return Response(serializer.data)

    """
    POST (create a carpool entry)
    """

    def post(self, request):
        serializer = poolsSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(created_by = self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    DELETE (delete a pool sending the id in the url, the user only can delete her own pools)
    """
    def delete(self, request, *args, **kwargs): 
        pool_id = request.query_params.get('id')
        if not pool_id:
            return Response({'error' : 'You need to send pool id in the url'}, status=status.HTTP_403_FORBIDDEN)
        
        if not Pool.objects.filter(id=pool_id).exists():
            return Response({'error' : 'There is not a pool with this id'}, status=status.HTTP_403_FORBIDDEN)
        
        instance = Pool.objects.filter(id=pool_id).last()

        if instance.created_by != self.request.user:
            return Response({'error' : 'You are not the owner of this pool'}, status=status.HTTP_401_UNAUTHORIZED)
        
        instance.delete()
        return Response({'ok' : 'Pool deleted succesfully'}, status=status.HTTP_200_OK)
    

    #CODING (METODO PATCH PONER JUNTO CON EL DELETE PARA APROVECHAR, REVISAR QUE REQUEST SE RECIVE)
    def update(self, request, *args, **kwargs):
        pool_id= request.query_params.get('id')
        instance = self.get_object()
        print(instance)


## prueba google
class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter