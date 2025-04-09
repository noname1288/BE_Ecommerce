import uuid
from django.db import models

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # UUID instead of Integer
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    images = models.JSONField(null=True, blank=True, default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True  # No table will be created for this model

    def __str__(self):
        return self.name 


# -------------------
# Concrete Models
# -------------------

class Book(Product):
    author = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)

class Phone(Product):
    brand = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    storage = models.PositiveIntegerField()  # Example: 128 for 128GB
    ram = models.PositiveIntegerField()  # Example: 8 for 8GB

class Clothes(Product):
    size = models.CharField(max_length=10)  # Example: "M", "L", "XL"
    color = models.CharField(max_length=50)
    material = models.CharField(max_length=100)



# -------------------
# Product Images Model
# -------------------

# class ProductImage(models.Model):
#     product = models.ForeignKey(
#         "self",  # This allows linking images to all product types
#         on_delete=models.CASCADE,
#         related_name="images"
#     )
#     image = models.ImageField(upload_to="product_images/")

#     def __str__(self):
#         return f"Image for {self.product.name}"