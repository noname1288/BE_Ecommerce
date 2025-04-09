import uuid
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from customer.models import Customer  # Ensure Customer model exists

class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def update_total_price(self):
        """Recalculate total price based on cart items."""
        self.total_price = sum([item.price_item for item in self.items.all()])
        self.save()

    def __str__(self):
        return f"Cart {self.id} - Total: ${self.total_price}"


class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()  # Change to UUID for consistency
    product = GenericForeignKey("content_type", "object_id")
    quantity = models.PositiveIntegerField(default=1)
    price_item = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        """Recalculate price_item before saving"""
        if self.product:
            self.price_item = self.quantity * self.product.price
        super().save(*args, **kwargs)
        if self.cart:
            self.cart.update_total_price()

    def delete(self, *args, **kwargs):
        """Update total price when item is deleted"""
        cart = self.cart  # Store reference before deletion
        super().delete(*args, **kwargs)
        if cart:
            cart.update_total_price()

    def __str__(self):
        return f"{self.quantity} x {self.product} - ${self.price_item}"
