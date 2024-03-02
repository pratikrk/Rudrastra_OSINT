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
          
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests

class ThirdPartyIntegrationView(APIView):
    def post(self, request):
        try:
            input_fields = {
                "phone": request.data.get("phone_number"),
                "email_address": request.data.get("email_address"),
                "country_code": request.data.get("country_code")
            }
            response_data = {}


            #whatsapp details
            phone_number = input_fields.get("phone")
            phone_number = self.format_phone_number(phone_number, input_fields.get("country_code"))
            url = "https://whatsapp-osint.p.rapidapi.com/wspic/dck"
            querystring = {"phone":f"{phone_number}"}

            headers = {
	            "X-RapidAPI-Key": "b95fd8411bmsh0848506b3e8609bp11583cjsnc7dd84f5f6ec",
	            "X-RapidAPI-Host": "whatsapp-osint.p.rapidapi.com"
            }

            response = requests.get(url, headers=headers, params=querystring)

            whatsapp_details=response.json()
            response_data["whatsapp_data"] = whatsapp_details


            # Phone Lookup Module
            phone_data = None
            phone_number = input_fields.get("phone")
            if phone_number:
                phone_number = self.format_phone_number(phone_number, input_fields.get("country_code"))
                url = "https://number-validator1.p.rapidapi.com/NumberVerificationValidate"
                payload = { "number": f"{phone_number}" }
                headers = {
	                "content-type": "application/json",
	                "X-RapidAPI-Key": "b95fd8411bmsh0848506b3e8609bp11583cjsnc7dd84f5f6ec",
	                "X-RapidAPI-Host": "number-validator1.p.rapidapi.com"
                }
                response = requests.post(url, json=payload, headers=headers)
                phone_data = response.json()
                response_data["phone_lookup"] = phone_data

            # Data Breach Module
            combined_messages = []
            combined_errors = []
            api_key = "6f958468aa79132c9a854736d3df9d14"
            for field, value in input_fields.items():
                if value and field != "country_code":
                    payload = {
                        "key": api_key,
                        "type": field,
                        "query": value
                    }
                    endpoint = "https://leak-lookup.com/api/search"
                    headers = {"Content-Type": "application/x-www-form-urlencoded"}
                    response = requests.post(endpoint, headers=headers, data=payload)
                    response.raise_for_status()
                    response_data_field = response.json()
                    combined_messages.append(response_data_field.get("message"))
                    if "error" in response_data_field:
                        combined_errors.append(response_data_field["error"])

            response_data["breach_data1"] = {"messages": combined_messages, "errors": combined_errors}
            email = input_fields.get("email_address")
            if email:
                url = "https://breachdirectory.p.rapidapi.com/"
                querystring = {"func": "auto", "term": email}
                headers = {
                    "X-RapidAPI-Key": "a5b8ce1fe5msh7f15b23eb92ebd8p1014a0jsnc22250e96caa",
                    "X-RapidAPI-Host": "breachdirectory.p.rapidapi.com"
                }
                response = requests.get(url, headers=headers, params=querystring)
                data = response.json()
                response_data["breach_data2"]= data

            return Response(response_data, status=status.HTTP_200_OK)
        
        except requests.RequestException as e:
            return Response({"error": "Failed to query third-party API"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def format_phone_number(self, phone_number, country_code):
        return  country_code + phone_number


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