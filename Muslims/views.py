from django.shortcuts import render
from rest_framework.decorators import api_view
from .serializers import MuslimSerializer,UserSerializer
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import Muslim

@api_view(["GET"])
def list(request):
    muslims = User.objects.all()
    serializer = UserSerializer(muslims,many=True)
    return Response(serializer.data)

@api_view(["POST"])
def register(request):
    if User.objects.filter(username=request.data["username"]).exists():
        return Response({"Error":"User exists"})
    userserializer = UserSerializer(data=request.data)
    muslimserializer = MuslimSerializer(data=request.data)
    if userserializer.is_valid() and muslimserializer.is_valid():
        try:
            validate_password(request.data["password"])
            try:
                user = User.objects.create_user(first_name=request.data["first_name"],last_name=request.data["last_name"],username=request.data["username"],email=request.data["email"])
                user.set_password(request.data["password"])
                user.save()
                muslim = Muslim.objects.create(user=user, age=request.data["age"],is_married=request.data["is_married"],is_male=request.data["is_male"])
                muslim.save()
            except:
                return Response({"Error":"Data error"})
        except:
            return Response({"Error":"Try better password"})
    else: return Response({"Error":"Data error"})
    return Response(muslimserializer.data)