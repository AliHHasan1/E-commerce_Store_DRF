from rest_framework import serializers
from product.models import Product
from django.db import models

class ProductSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews.exists():
            average = reviews.aggregate(avg=models.Avg('rating'))['avg']
            return round(average, 2)
        return None
