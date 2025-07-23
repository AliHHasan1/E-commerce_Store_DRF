from rest_framework import serializers
from order.models import OrderItem
from product.models import Product

class OrderItemSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'quantity', 'price_at_time', 'total_price']

    def validate(self, data):
        product = data['product']
        requested_qty = data['quantity']

        # التحقق من توفر المخزون
        if product.stock < requested_qty:
            raise serializers.ValidationError({
                "quantity": f"الكمية المطلوبة ({requested_qty}) أكبر من المتوفر ({product.stock})"
            })

        return data

    def create(self, validated_data):
        product = validated_data['product']
        quantity = validated_data['quantity']

        # حفظ السعر عند لحظة إنشاء الطلب
        validated_data['price_at_time'] = product.price

        # خصم الكمية من المخزون
        product.stock -= quantity
        product.save()

        return super().create(validated_data)

    def get_total_price(self, obj):
        return obj.quantity * obj.price_at_time
