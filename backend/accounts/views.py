import requests
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import SignupSerializer, LoginSerializer, UserSerializer,PhoneNumberSerializer,CheckWhatsAppSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import PhoneNumber
from django.http import JsonResponse

class UserProfile(APIView):
    permission_classes = (IsAuthenticated,)
    # authentication_classes = [JWTAuthentication]

    def get(self, request):
        user = User.objects.get(pk=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer(self, *args, **kwargs):
        return SignupSerializer(*args, **kwargs)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        refresh, access = self.get_tokens_for_user(user)

        tokens = {'access': str(access), 'refresh': str(refresh)}
        return Response(tokens, status=status.HTTP_200_OK)

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        return refresh, access

    def get_serializer(self, *args, **kwargs):
        return LoginSerializer(*args, **kwargs)

# class LoginView(APIView):
#     permission_classes = [AllowAny]
#     authentication_classes = [JWTAuthentication]

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         user = serializer.validated_data['user']

#         refresh = RefreshToken.for_user(user)
#         tokens = {'access': str(refresh.access_token), 'refresh': str(refresh)}
#         return Response(tokens, status=status.HTTP_200_OK)

#     def get_serializer(self, *args, **kwargs):
#         return LoginSerializer(*args, **kwargs)

class LogoutView(APIView):
     permission_classes = (IsAuthenticated,)
     authentication_classes = [JWTAuthentication]
     def post(self, request):
          try:
               refresh_token = request.data["refresh_token"]
            #    print(refresh_token)
               token = RefreshToken(refresh_token)
               token.blacklist()
               return Response(status=status.HTTP_205_RESET_CONTENT)
          except Exception as e:
               return Response(status=status.HTTP_400_BAD_REQUEST)


# class LogoutView(APIView):
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [JWTAuthentication]

#     def post(self, request, *args, **kwargs):
#         try:
#             refresh_token = request.data.get('refresh_token', None)
#             if refresh_token:
#                 token = RefreshToken(refresh_token)
#                 token.blacklist()
#                 return Response({"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
          
class SubmitPhoneNumberView(APIView):
    def post(self, request):
        phone_number = request.data.get("phone_number")
        if not phone_number:
            return Response({"error": "Phone number is required"}, status=status.HTTP_400_BAD_REQUEST)

        phone_number_obj = PhoneNumber.objects.create(phone_number=phone_number)

        serializer = PhoneNumberSerializer(phone_number_obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    


class CheckWhatsAppView(APIView):
    def get(self, request, your_number, number_to_check):
        serializer = CheckWhatsAppSerializer(data={'your_number': your_number, 'number_to_check': number_to_check})
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        api_url = f'https://api.p.2chat.io/open/whatsapp/check-number/{your_number}/{number_to_check}'
        headers = {
            'X-User-API-Key': 'UAKf8a47ef7-869f-423b-aa30-407a93b99988'  
        }

        try:
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()
            return Response(response.json(), status=response.status_code)
        except requests.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)