from rest_framework import serializers
from .models import Customer, Address, Job

class RegisterSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)  # Ensure UUID is properly handled
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'email', 'username', 'password']  # Include `id` in response

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class AddressSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Address
        fields = "__all__"

class JobSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Job
        fields = "__all__"

class CustomerSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    addresses = AddressSerializer(many=True, read_only=True)
    job = JobSerializer(read_only=True)

    class Meta:
        model = Customer
        exclude = ['password']  
