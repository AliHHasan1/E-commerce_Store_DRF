from django.db import models
from django.utils import timezone

from account.models import Customer


# Create your models here.
class Order(models.Model):
    STATUS_CHOICES = [
        ('New', 'New'),
        ('Processing', 'Processing'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    customer = models.ForeignKey(Customer, related_name='orders', on_delete=models.CASCADE)
    order_date = models.DateTimeField(default=timezone.now)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New')
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-order_date'] # Order by most recent first

    def __str__(self):
        return f"Order {self.id} by {self.customer.first_name} {self.customer.last_name}"