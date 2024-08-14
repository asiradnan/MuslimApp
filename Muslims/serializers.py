from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Muslim

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name","last_name","username","password","email"]

class MuslimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Muslim
        fields = ["is_male","age","is_married"]

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()