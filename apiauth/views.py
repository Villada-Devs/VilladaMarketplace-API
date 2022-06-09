#allauth
from multiprocessing import context
from allauth.account.views import ConfirmEmailView
from allauth.account.models import EmailAddress
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework import status, viewsets
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Event
from rest_framework.permissions import IsAuthenticated, AllowAny
from dj_rest_auth.registration.serializers import (
    VerifyEmailSerializer, ResendEmailVerificationSerializer
)
from dj_rest_auth.views import LoginView
from apiauth.serializers import EventsSerializer



#api 

class EventsViewSet(viewsets.ViewSet):
    """
    GET ver todos los eventos existentes
    """
    def list(self, request):
        queryset = Event.objects.all()
        EventSerializer = EventsSerializer(queryset, many=True)
        return Response(EventSerializer.data)

    """
    Create view solo pueden hacer POST los admins
    """   
    def post(self, request):
        user_state = request.user.is_staff
        user_id = request.user.id
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


    def destroy(self, request, *args, **kwargs):
        user_state = request.user.is_staff
        if user_state == True:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({'detail' : 'Event deleted succesfully'},status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error' : 'Authorization Required'}, status=status.HTTP_401_UNAUTHORIZED)

    def update(self, request, *args, **kwargs):
        user_state = request.user.is_staff
        if user_state == True:
            return super().update(request, *args, **kwargs)

        else:
            return Response({'error' : 'Authorization Required'}, status=status.HTTP_401_UNAUTHORIZED)

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



