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
            return Response({"Error":"Try better password"},status=status.HTTP_401_UNAUTHORIZED)
    else: return Response({"Error":"Data error"})
    return Response(muslimserializer.data)

@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data = request.data)
    if serializer.is_valid():
        user = authenticate(username = request.data['username'],password = request.data['password'])
        if user is None:
            return Response({"Error":"Try again"},status=status.HTTP_401_UNAUTHORIZED)
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            "Success":"You are logged in"
        },status = status.HTTP_200_OK)
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
def loggedin(request):
    if request.user.is_authenticated:
        return Response({"Success":f"You are still logged in {request.user.username}"})
    else:
        return Response({"Success":"You are not logged in"},status = status.HTTP_401_UNAUTHORIZED)
    
        