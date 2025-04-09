from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Customer
from .serializers import RegisterSerializer, LoginSerializer, CustomerSerializer, AddressSerializer, JobSerializer
from rest_framework.views import APIView
from allauth.socialaccount.models import SocialApp
from django.conf import settings
from django.contrib.auth import get_user_model
import requests
from rest_framework import generics
from .models import Customer, Address, Job

User = get_user_model()

def generate_jwt(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

@swagger_auto_schema(
    method='post',
    request_body=RegisterSerializer,
    responses={200: "User registered successfully", 400: "Email already exists"}
)
@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        name = serializer.validated_data['username']
        password = serializer.validated_data['password']

        if Customer.objects.filter(email=email).exists():
            return Response({"error": "Email already exists"}, status=400)

        user = Customer.objects.create_user(email=email, username=name, password=password)
        jwt_tokens = generate_jwt(user)
        user_data = CustomerSerializer(user).data
        return Response({"message": "User registered successfully", "tokens": jwt_tokens, "customer": user_data}, status=200)
    return Response(serializer.errors, status=400)

@swagger_auto_schema(
    method='post',
    request_body=LoginSerializer,
    responses={200: "Login successful", 400: "Invalid credentials"}
)
@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = authenticate(email=email, password=password)
        if user is not None:
            user_data = CustomerSerializer(user).data
            jwt_tokens = generate_jwt(user)
            return Response({"message": "Login successful", "tokens": jwt_tokens, "customer": user_data}, status=200)
    return Response({"error": "Invalid credentials"}, status=400)


class GoogleLoginURL(APIView):
    """Returns the Google login URL for OAuth"""

    def get(self, request):
        google_app = SocialApp.objects.filter(provider="google").first()
        if not google_app:
            return Response({"error": "Google provider is not configured"}, status=400)

        login_url = (
            "https://accounts.google.com/o/oauth2/auth"
            f"?client_id={google_app.client_id}"
            f"&redirect_uri={settings.SOCIALACCOUNT_PROVIDERS['google']['APP']['redirect_uri']}"
            "&response_type=code"
            "&scope=openid email profile"
            "&access_type=offline"
            "&prompt=consent"
        )
        return Response({"login_url": login_url})


class GoogleLogin(APIView):
    """Handles Google OAuth login and user creation"""

    def post(self, request):
        code = request.data.get("code")
        if not code:
            return Response({"error": "Authorization code is required"}, status=400)

        google_app = SocialApp.objects.filter(provider="google").first()
        if not google_app:
            return Response({"error": "Google provider is not configured"}, status=400)

        # Step 1: Exchange code for access token
        token_url = "https://oauth2.googleapis.com/token"
        token_data = {
            "code": code,
            "client_id": google_app.client_id,
            "client_secret": google_app.secret,
            "redirect_uri": settings.SOCIALACCOUNT_PROVIDERS["google"]["APP"]["redirect_uri"],
            "grant_type": "authorization_code",
        }
        token_response = requests.post(token_url, data=token_data)
        
        if token_response.status_code != 200:
            return Response({"error": "Failed to get access token"}, status=400)

        access_token = token_response.json().get("access_token")

        # Step 2: Fetch user info
        user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
        user_info_response = requests.get(user_info_url, headers={"Authorization": f"Bearer {access_token}"})
        
        if user_info_response.status_code != 200:
            return Response({"error": "Failed to fetch user info"}, status=400)

        user_data = user_info_response.json()
        email = user_data.get("email")
        name = user_data.get("name")

        if not email:
            return Response({"error": "Google account has no email"}, status=400)

        # Step 3: Get or create user
        user, created = User.objects.get_or_create(email=email, defaults={"username": name})

        # Step 4: Generate JWT Token
        jwt_tokens = generate_jwt(user)

        return Response({"message": "Login successful", "tokens": jwt_tokens}, status=200)


# 📧 Customer API Views
class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    lookup_field = 'id'  # Ensures UUID-based lookup


# 🏠 Address API Views
class AddressListCreateView(generics.ListCreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

class AddressDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    lookup_field = 'id'  # Ensures UUID-based lookup


# 💼 Job API Views
class JobListCreateView(generics.ListCreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

class JobDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    lookup_field = 'id'  # Ensures UUID-based lookup
