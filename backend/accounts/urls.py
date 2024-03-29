from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from . import views
from .views import CheckWhatsAppView, ThirdPartyIntegrationView
app_name = "accounts"

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("user/", views.UserProfile.as_view(), name="user"),
    path('submit-data/', ThirdPartyIntegrationView.as_view(), name='third_party_integration'),
    path('check-whatsapp/<your_number>/<number_to_check>/', CheckWhatsAppView.as_view(), name='check_whatsapp'),

]