from rest_framework import serializers
from .models import Book, Phone, Clothes, Product


class BaseProductSerializer(serializers.ModelSerializer):
    # Define the images field in the base serializer
    id = serializers.UUIDField(read_only=True)  # UUID support
    images = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = Product  # Common base model, shared by all child serializers
        fields = "__all__"  # Includes all fields from the Product model


class BookSerializer(BaseProductSerializer):
    class Meta(BaseProductSerializer.Meta):
        model = Book  # Override the model for the Book serializer


class PhoneSerializer(BaseProductSerializer):
    class Meta(BaseProductSerializer.Meta):
        model = Phone  # Override the model for the Phone serializer


class ClothesSerializer(BaseProductSerializer):
    class Meta(BaseProductSerializer.Meta):
        model = Clothes  # Override the model for the Clothes serializer
