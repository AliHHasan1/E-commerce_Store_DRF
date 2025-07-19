from django.contrib import admin
from product.models.category_models import Category
from product.models.product_models import Product

admin.site.register(Category)
admin.site.register(Product)
