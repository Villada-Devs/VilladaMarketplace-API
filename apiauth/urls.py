
from rest_framework_simplejwt import views as jwt_views
from django.urls import path, include
from django.urls import include, path, re_path
from django.views.generic import RedirectView, TemplateView
from dj_rest_auth.registration.views import VerifyEmailView
from dj_rest_auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordResetConfirmView,
    PasswordResetView, UserDetailsView,
)
from allauth.account.views import ConfirmEmailView
from .views import ResendEmailVerificationView
from apiauth import views
from rest_framework import routers
from .views import ProfileView
router = routers.SimpleRouter()

urlpatterns = [
    
    path('', include('dj_rest_auth.urls')),
    re_path(r'password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,40})/$', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('register/', include('dj_rest_auth.registration.urls')),
    path('verify-email/', VerifyEmailView.as_view(), name='rest_verify_email'),
    path('account-confirm-email/<str:key>/', ConfirmEmailView.as_view()),
    re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$', VerifyEmailView.as_view(), name='account_confirm_email'),
    path("resend-email-confirmation/", ResendEmailVerificationView.as_view(), name='Resend_verification_email'),
    path('jwt/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('jwt/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/<int:id>', ProfileView.as_view())
]


