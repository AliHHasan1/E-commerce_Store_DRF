from rest_framework import serializers
from order.models import Order, OrderItem
from product.models import Product
from account.models.customer_models import Customer

# 🔹 عرض مختصر للمنتج داخل عنصر الطلب
class ProductOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'image_url']
        read_only_fields = fields

# 🔹 Serializer لعناصر الطلب
class OrderItemSerializer(serializers.ModelSerializer):
    product_details = ProductOrderSerializer(source='product', read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )
    total_price = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product_id', 'product_details', 'quantity', 'price_at_time', 'total_price']
        read_only_fields = ['price_at_time', 'total_price']

    def validate(self, data):
        product = data.get('product')
        quantity = data.get('quantity')

        if not product:
            raise serializers.ValidationError("معرف المنتج مطلوب.")
        if not product.is_available:
            raise serializers.ValidationError(f"المنتج '{product.name}' غير متوفر.")
        if product.stock_quantity < quantity:
            raise serializers.ValidationError(
                f"المخزون غير كافٍ للمنتج '{product.name}'. المتوفر: {product.stock_quantity}، المطلوب: {quantity}."
            )
        return data

    def create(self, validated_data):
        product = validated_data['product']
        quantity = validated_data['quantity']
        validated_data['price_at_time'] = product.price
        product.stock_quantity -= quantity
        product.save()
        return super().create(validated_data)

    def get_total_price(self, obj):
        return obj.quantity * obj.price_at_time

# 🔹 Serializer رئيسي للطلب
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, required=True)
    customer_details = serializers.ReadOnlyField(source='customer.first_name')

    class Meta:
        model = Order
        fields = ['id', 'customer', 'customer_details', 'order_date', 'total_amount', 'status', 'notes', 'items']
        read_only_fields = ['id', 'order_date', 'total_amount', 'status', 'customer_details']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        validated_data['status'] = 'New'
        order = Order.objects.create(**validated_data)
        total = 0

        for item in items_data:
            product = item['product']
            quantity = item['quantity']
            unit_price = product.price

            product.stock_quantity -= quantity
            product.save()

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price_at_time=unit_price
            )
            total += unit_price * quantity

        order.total_amount = total
        order.save()
        return order

    def update(self, instance, validated_data):
        instance.notes = validated_data.get('notes', instance.notes)
        instance.save()
        return instance

# 🔹 Serializer لتحديث حالة الطلب فقط
class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']
        read_only_fields = ['id', 'customer', 'order_date', 'total_amount', 'notes']

    def validate_status(self, value):
        valid_statuses = [choice[0] for choice in Order.STATUS_CHOICES]
        if value not in valid_statuses:
            raise serializers.ValidationError(
                f"'{value}' ليست حالة صالحة. الحالات المسموحة: {', '.join(valid_statuses)}"
            )
        return value
