from django.contrib.auth.models import AbstractUser
from django.db import models


class Customer(AbstractUser):
    ROLE_CHOICES = (
    ('admin', 'Admin'),
    ('seller', 'Seller'),
    ('customer', 'Customer'),
    )


    # تم جعل الemail حقل unique
    email = models.EmailField(unique=True, null=False, blank=False)
    phone = models.CharField(max_length=20)
    address = models.TextField(max_length=500)
    registration_date = models.DateTimeField(auto_now_add=True)
    role = models.CharField(choices=ROLE_CHOICES, max_length=20,default='customer')

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
