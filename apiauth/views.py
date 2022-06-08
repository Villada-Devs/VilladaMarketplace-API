from allauth.account import app_settings as allauth_settings
from allauth.account.views import ConfirmEmailView
from allauth.account.models import EmailAddress
from allauth.socialaccount import signals
from django.conf import settings
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework import status, viewsets
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Event,User
from rest_framework.permissions import IsAuthenticated, IsAdminUser



#docs

from dj_rest_auth.app_settings import (
    JWTSerializer, TokenSerializer, create_token,
)
from dj_rest_auth.models import TokenModel
from dj_rest_auth.registration.serializers import (
    SocialAccountSerializer, SocialConnectSerializer, SocialLoginSerializer,
    VerifyEmailSerializer, ResendEmailVerificationSerializer
)
from dj_rest_auth.utils import jwt_encode
from dj_rest_auth.views import LoginView

from apiauth.serializers import EventsSerializer

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters('password1', 'password2'),
)


#api 

class EventsViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    """
    GET ver todos los eventos existentes
    """
    def list(self, request):
        queryset = Event.objects.all()
        EventSerializer = EventsSerializer(queryset, many=True)
        return Response(EventSerializer.data)

    """
    Create view POST pueden postear todos
    """   
    def post(self, request, *args, **kwargs):
        serializer = EventsSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

"""
    GET de un objeto, PUT a un objeto, DELETE a un objeto (PK como parametro)
"""


class EventsDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = EventsSerializer
    permission_classes = [IsAuthenticated]
    lookup_field =  "id"
    
    def get_queryset(self):
        return Event.objects.filter()


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)



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

#register view override

