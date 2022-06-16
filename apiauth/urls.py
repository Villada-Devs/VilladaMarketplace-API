
from django.urls import path, include
from django.urls import include, path, re_path
from django.views.generic import RedirectView, TemplateView
from dj_rest_auth.registration.views import  VerifyEmailView
from dj_rest_auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordResetConfirmView,
    PasswordResetView, UserDetailsView,
)
from allauth.account.views import ConfirmEmailView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import EventsDetailView, EventsViewSet, ResendEmailVerificationView, poolsListView
from apiauth import views
from rest_framework import routers
router = routers.SimpleRouter()
from django.conf import settings

schema_view = get_schema_view(
   openapi.Info(
      title="API DOCS",
      default_version='v1',
      description="La documentacion numa peshasho",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
from rest_framework_simplejwt import views as jwt_views
urlpatterns = [

     #auth API
     re_path(r'^dj-rest-auth/password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,40})/$', PasswordResetConfirmView.as_view(),
            name='password_reset_confirm'),
     path('dj-rest-auth/', include('dj_rest_auth.urls')),
     path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
     path('verify-email/',
         VerifyEmailView.as_view(), name='rest_verify_email'),
     path('account-confirm-email/<str:key>/', ConfirmEmailView.as_view()),
     re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$',
         VerifyEmailView.as_view(), name='account_confirm_email'),
     path("resend-email-confirmation/", ResendEmailVerificationView.as_view(), name ='Resend_verification_email' ),

     #docs
     path('playground/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
     path('docs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
     #upfapi
     path("events/<int:id>/", EventsDetailView.as_view(), name='Events_detail'),
     
     #jwt token (token and refresh)
     path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
     path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

     #pool
     
    
    
]



#api urls with router
router.register('pools', poolsListView, basename='PoolsModelGetALL')
router.register('events', EventsViewSet, basename='EventsModelGetALL')
urlpatterns += router.urls
