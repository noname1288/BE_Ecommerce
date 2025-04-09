from django.conf import settings
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from cart.models import Cart
from .models import Order, OrderItem
from .serializers import OrderSerializer
from django.shortcuts import get_object_or_404
from customer.models import Customer

from django.contrib.auth import get_user_model

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(detail=False, methods=["get"])
    def customer_orders(self, request):
        """Get all orders for a specific customer"""
        customer_id = request.query_params.get("customer_id")
        
        if not customer_id:
            return Response({"error": "customer_id is required"}, status=400)
        
        customer = get_object_or_404(Customer, id=customer_id)
        orders = Order.objects.filter(customer=customer)
        
        return Response(OrderSerializer(orders, many=True).data, status=200)

    @action(detail=False, methods=["post"])
    def checkout(self, request):
        """Checkout from cart to create an order"""
        User = get_user_model()  # Get the User model dynamically
        customer_id = request.data.get("customer")  # Get customerId from request

        if not customer_id:
            return Response({"error": "customerId is required"}, status=400)

        try:
            customer = User.objects.get(id=customer_id)  # Fetch customer
        except User.DoesNotExist:
            return Response({"error": "Invalid customerId"}, status=404)

        cart = Cart.objects.filter(customer=customer).first()

        if not cart or not cart.items.exists():
            return Response({"error": "Cart is empty"}, status=400)

        # Create order
        order = Order.objects.create(customer=customer, total_price=cart.total_price)

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product_name=str(item.product),
                quantity=item.quantity,
                price_item=item.price_item,
            )

        cart.items.all().delete()  # Empty the cart after checkout

        return Response({"order": OrderSerializer(order).data})
