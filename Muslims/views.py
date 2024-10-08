from rest_framework.decorators import api_view, permission_classes
from .serializers import MuslimSerializer,UserSerializer,LoginSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from .models import Muslim
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken 
from django.contrib.auth import logout

@api_view(["GET"])
def list(request):
    muslims = User.objects.all()
    serializer = UserSerializer(muslims,many=True)
    return Response(serializer.data)

@api_view(["POST"])
def register(request):
    if User.objects.filter(username=request.data["username"]).exists():
        return Response({"Error":"User exists"},status=status.HTTP_409_CONFLICT)
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
            return Response({"Error":"Try better password"},status=status.HTTP_401_UNAUTHORIZED)
    else: return Response({"Error":"Data error"},status=status.HTTP_401_UNAUTHORIZED)
    return Response({"Success: Created Account Successfully!"})

@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data = request.data)
    if serializer.is_valid():
        user = authenticate(username = request.data['username'],password = request.data['password'])
        if user is None:
            return Response({"Error":"Incorrect Credentials"},status=status.HTTP_401_UNAUTHORIZED)
        refresh = RefreshToken.for_user(user)
        return Response({'refresh': str(refresh),'access': str(refresh.access_token),},status = status.HTTP_200_OK)
    return Response({"Error":"Data error"})

@api_view(['POST'])  
def log_out(request):
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist() 
        return Response({"message": "Logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])  
def user_detail(request):
    if request.user.is_authenticated:
        userserializer =  UserSerializer(request.user)
        muslimserializer =  MuslimSerializer(Muslim.objects.get(user = request.user))
        data = {}
        for key in userserializer.data.keys():
            data[key]=userserializer[key].value
        for key in muslimserializer.data.keys():
            data[key]=muslimserializer[key].value
        del data["password"]
        return Response(data)
    else:
        return Response({"Success":"You are not logged in"},status = status.HTTP_401_UNAUTHORIZED)
    

@api_view(['POST'])
def change_email(request):
    if request.user.is_authenticated:
        user = request.user
        user.email = request.data["email"]
        user.save()
        return Response({"Success":"Email Changed"})
    return Response({"Error":"Please Log In first!"},status = status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def change_password(request):
    if request.user.is_authenticated:
        user = request.user
        user.set_password(request.data["password"])
        return Response({"Success":"Password Changed"})
    return Response({"Error":"Please Log In first!"},status = status.HTTP_401_UNAUTHORIZED)

@api_view(["POST"])
def update_profile(request):
    if request.user.is_authenticated:
        user = request.user
        userserializer = UserSerializer(user, data=request.data, partial=True)
        muslimserializer = MuslimSerializer(user.muslim, data=request.data, partial=True)
        if userserializer.is_valid() and muslimserializer.is_valid():
            userserializer.save()
            muslimserializer.save()
            return Response({"Success: Profile Updated Successfully!"})
    return Response({"Error":"Please Log In first!"},status = status.HTTP_401_UNAUTHORIZED)

    
        