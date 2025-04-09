from django.urls import path, re_path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import register, login
from .views import GoogleLoginURL, GoogleLogin
from dj_rest_auth.views import LogoutView
from .views import (
    CustomerListCreateView,
    CustomerDetailView,
    AddressListCreateView,
    AddressDetailView,
    JobListCreateView,
    JobDetailView
)
schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="API documentation for authentication",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("google-login-url/", GoogleLoginURL.as_view(), name="google-login-url"),
    path("google-login/", GoogleLogin.as_view(), name="google-login"),
    path('accounts/', include('allauth.urls')),
    path('customers/', CustomerListCreateView.as_view(), name='customer-list-create'),

    # 🏠 Address API
    path('addresses/', AddressListCreateView.as_view(), name='address-list-create'),
    path('addresses/<uuid:pk>/', AddressDetailView.as_view(), name='address-detail'),      

    # 💼 Job API
    path('jobs/', JobListCreateView.as_view(), name='job-list-create'),
    path('jobs/<uuid:pk>/', JobDetailView.as_view(), name='job-detail'),   
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    re_path(r'^swagger\.json$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]
