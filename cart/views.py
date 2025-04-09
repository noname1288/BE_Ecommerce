from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem
from products.models import Book, Phone, Clothes
from .serializers import CartSerializer, CartItemSerializer
from customer.models import Customer
import uuid

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    lookup_field = "id"
    def create(self, request, *args, **kwargs):
        customer_id = request.data.get("customer")
        if not customer_id:
            return Response({"error": "Customer ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            customer_uuid = uuid.UUID(customer_id)
        except ValueError:
            return Response({"error": "Invalid UUID format for customer ID"}, status=status.HTTP_400_BAD_REQUEST)

        customer = get_object_or_404(Customer, id=customer_uuid)
        cart, created = Cart.objects.get_or_create(customer=customer)

        # Update the total price after creating the cart
        cart.update_total_price()

        return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        request.data.pop('total_price', None)  # Prevent modifying total_price
        return super().update(request, *args, **kwargs)


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    lookup_field = "id"
    def create(self, request, *args, **kwargs):
        cart_id = request.data.get("cart_id")
        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))
        print(f"Received product_id: {product_id}, type: {type(product_id)}")

        # Convert to UUID
        try:
            cart_uuid = uuid.UUID(cart_id)
            product_uuid = uuid.UUID(str(product_id))
        except ValueError:
            return Response({"error": "Invalid UUID format"}, status=status.HTTP_400_BAD_REQUEST)

        cart = Cart.objects.filter(id=cart_uuid).first()
        if not cart:
            return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)

        # Find the correct product subclass
        product = None
        for model in [Book, Phone, Clothes]:
            product = model.objects.filter(id=product_uuid).first()
            if product:
                break

        if not product:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check stock availability
        if quantity > product.stock:
            return Response({"error": f"Only {product.stock} items left in stock"}, status=status.HTTP_400_BAD_REQUEST)

        # Get ContentType for product
        content_type = ContentType.objects.get_for_model(product)

        # Check if the product is already in the cart
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, content_type=content_type, object_id=product.id,
            defaults={"quantity": quantity}
        )

        if not created:
            if quantity > product.stock:
                return Response(
                    {"error": f"Cannot add {quantity} items. Only {product.stock - cart_item.quantity} left in stock."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            cart_item.quantity += quantity
            cart_item.price_item = cart_item.quantity * product.price
            cart_item.save()

        # 🟢 Update product stock
        product.stock -= quantity
        product.save()

        return Response(CartItemSerializer(cart_item).data, status=status.HTTP_201_CREATED)
