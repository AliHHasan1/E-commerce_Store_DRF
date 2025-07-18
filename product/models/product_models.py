from django.db import models
from product.models.category_models import Category

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True,null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    stock_quantity = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    image_url = models.URLField(blank=True,null=True)

    def __str__(self):
        return self.name
