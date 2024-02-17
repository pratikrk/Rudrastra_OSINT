from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import PhoneNumber


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "username", "email"]
        extra_kwargs = {'password': {'write_only': True}}

class SignupSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)

        if user and user.is_active:
            data['user'] = user
        else:
            raise serializers.ValidationError('Unable to log in with provided credentials')

        return data

# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField(max_length=150, required=True)
#     password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})


class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = ['phone_number']

class CheckWhatsAppSerializer(serializers.Serializer):
    your_number = serializers.CharField(max_length=15)
    number_to_check = serializers.CharField(max_length=15)

    def validate(self, data):
        your_number = data.get('your_number')
        number_to_check = data.get('number_to_check')

        if not your_number or not number_to_check:
            raise serializers.ValidationError("Both your number and number to check are required.")

        return data