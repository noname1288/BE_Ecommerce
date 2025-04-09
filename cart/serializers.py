from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from .models import Cart, CartItem
from products.models import Book, Phone, Clothes
import uuid

class CartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.UUIDField(write_only=True)  # Use UUID instead of IntegerField
    cart_id = serializers.UUIDField(write_only=True)  # Use UUID instead of IntegerField
    product_details = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ["id", "cart_id", "product_id", "quantity", "product_details", "price_item"]

    def get_product_details(self, obj):
        """Retrieve product details based on content_type and object_id."""
        product_model = obj.content_type.model_class()
        product = product_model.objects.filter(id=obj.object_id).first()
        if product:
            return {
                "name": str(product), 
                "price": getattr(product, "price", None),
                "description": getattr(product, "description", None),
                "stock":getattr(product, "stock", None),
                "images": getattr(product, "images", [])  # Assuming it's a list of image URLs
            }
        return None

    def create(self, validated_data):
        product_id = validated_data.pop("product_id")
        cart_id = validated_data.pop("cart_id")

        # Ensure cart exists
        cart = Cart.objects.filter(id=cart_id).first()
        if not cart:
            raise serializers.ValidationError({"cart_id": "Cart not found"})

        # Determine ContentType dynamically based on product ID
        product_model = None
        for model in [Book, Phone, Clothes]:
            if model.objects.filter(id=product_id).exists():
                product_model = model
                break

        if not product_model:
            raise serializers.ValidationError({"product_id": "Invalid product ID"})

        content_type = ContentType.objects.get_for_model(product_model)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            content_type=content_type,
            object_id=product_id,
            defaults={"quantity": validated_data.get("quantity", 1)}
        )

        if not created:
            cart_item.quantity += validated_data.get("quantity", 1)
            cart_item.save()
        cart.update_total_price()
        return cart_item


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)  # Ensure Cart ID is UUID
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        exclude = ['total_price']

    def to_representation(self, instance):
        """Add total_price to the response."""
        data = super().to_representation(instance)
        data['total_price'] = instance.total_price  # Include total_price in the response
        return data

    def create(self, validated_data):
        cart = super().create(validated_data)
        cart.update_total_price()  # Recalculate total price after creation
        return cart

    def update(self, instance, validated_data):
        validated_data.pop('total_price', None)  # Exclude total_price from update
        instance = super().update(instance, validated_data)
        instance.update_total_price()  # Recalculate total price after update
        return instance
