import account.models
from django.db import models
from .order_models import Order
from product.models.product_models import Product
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price_at_time = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('order', 'product')  # يمنع تكرار نفس المنتج في نفس الطلب

    def get_total(self):
        return self.quantity * self.price_at_time

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order #{self.order.id}"