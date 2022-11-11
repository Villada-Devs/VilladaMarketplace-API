
from allauth.account.views import ConfirmEmailView
from allauth.account.models import EmailAddress
from django.utils.translation import gettext_lazy as _
from pyparsing import empty
from requests import request
from rest_framework import status, viewsets
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import GenericViewSet
from dj_rest_auth.registration.serializers import (
    VerifyEmailSerializer, ResendEmailVerificationSerializer
)
from dj_rest_auth.views import LoginView

from apiauth.serializers import ProfileSerializer
from .models import Profile
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


class ProfileView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileSerializer
    lookup_field = "id"

    def get_queryset(self):
        return Profile.objects.filter()

    def listaaaa(self, request):  
        queryset = Profile.objects.filter()
        user = request.GET.get('created_by')
        if user:
            if str(request.user.id) != user:
                print(request.user.id, user)
                return Response({'error' : 'You can not see the pool list from other user'}, status=status.HTTP_401_UNAUTHORIZED)
            queryset = queryset.filter(created_by=user)
        
        serializer = poolsSerializer(queryset, many=True)
        return Response(serializer.data)

    def list(self, request):
        user = request.GET.get('created_by')