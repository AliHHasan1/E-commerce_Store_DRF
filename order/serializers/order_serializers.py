import account.models
import django.db
from rest_framework import serializers
from order.models import Order, OrderItem # تأكد من استيراد كل النماذج اللازمة
from account.models.customer_models import Customer
from product.models.product_models import Product
# --- Nested Serializers (للعرض داخل OrderSerializer) ---

# ProductOrderSerializer: لعرض تفاصيل المنتج باختصار داخل عنصر الطلب.
class ProductOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'image_url']
        read_only_fields = fields # هذه المعلومات للقراءة فقط داخل الطلب

# OrderItemSerializer: لتسلسل عناصر الطلب (المنتجات ضمن طلب معين).
class OrderItemSerializer(serializers.ModelSerializer):
    # 'product_details' يعرض تفاصيل المنتج للقراءة فقط.
    product_details = ProductOrderSerializer(source='product', read_only=True)
    # 'product_id' يُستخدم عند إرسال البيانات (مثلاً عند إنشاء طلب جديد).
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )

    class Meta:
        model = OrderItem
        fields = ['id', 'product_id', 'product_details', 'quantity', 'unit_price']
        # 'unit_price' يتم حسابه تلقائيًا عند إنشاء الطلب، وليس من المدخلات.
        read_only_fields = ['unit_price']

    # التحقق من صحة بيانات عنصر الطلب (الكمية والمخزون).
    def validate(self, data):
        product = data.get('product')
        quantity = data.get('quantity')

        if product is None:
            raise serializers.ValidationError("معرف المنتج مطلوب لعنصر الطلب.")

        if not product.is_available:
            raise serializers.ValidationError(f"المنتج '{product.name}' غير متوفر للشراء حاليًا.")

        if product.stock_quantity < quantity:
            raise serializers.ValidationError(
                f"لا يوجد مخزون كافٍ للمنتج '{product.name}'. المتوفر: {product.stock_quantity}، المطلوب: {quantity}."
            )
        return data

# --- Main Order Serializers ---

# OrderSerializer: السيريالايزر الرئيسي لنموذج الطلب.
class OrderSerializer(serializers.ModelSerializer):
    # 'items' هو سيريالايزر متداخل لعناصر الطلب، ويجب أن يكون مطلوبًا (required=True)
    # لأنه لا معنى لطلب بدون منتجات.
    items = OrderItemSerializer(many=True, required=True)
    # 'customer_details' لعرض اسم العميل باختصار.
    customer_details = serializers.ReadOnlyField(source='customer.first_name') # أو source='customer.get_full_name' إذا كان موجودًا

    class Meta:
        model = Order
        fields = ['id', 'customer', 'customer_details', 'order_date', 'total_amount', 'status', 'notes', 'items']
        # هذه الحقول للقراءة فقط ويتم تعيينها بواسطة النظام (مثل المعرف، التاريخ، الإجمالي، الحالة).
        read_only_fields = ['id', 'order_date', 'total_amount', 'status', 'customer_details']

    # override create method: لإنشاء طلب جديد مع عناصر الطلب وتحديث المخزون.
    def create(self, validated_data):
        items_data = validated_data.pop('items') # استخراج بيانات عناصر الطلب
        
        # تعيين الحالة الافتراضية للطلب الجديد.
        validated_data['status'] = 'New' 
        
        # إنشاء الطلب نفسه.
        order = Order.objects.create(**validated_data)
        total_amount = 0

        # المرور على كل عنصر طلب لإنشائه وتحديث مخزون المنتج.
        for item_data in items_data:
            product = item_data['product'] # كائن المنتج الفعلي
            quantity = item_data['quantity']

            # سعر الوحدة عند الطلب هو السعر الحالي للمنتج.
            unit_price = product.price
            
            # تقليل كمية المخزون للمنتج.
            product.stock_quantity -= quantity
            product.save() # حفظ التغيير في مخزون المنتج.

            # إنشاء عنصر الطلب.
            OrderItem.objects.create(order=order, product=product, quantity=quantity, unit_price=unit_price)
            # إضافة قيمة العنصر إلى إجمالي الطلب.
            total_amount += unit_price * quantity
        
        # حفظ إجمالي الطلب المحسوب.
        order.total_amount = total_amount
        order.save() 
        return order

    # override update method: لتحديث الطلب (عادةً ما يقتصر على الملاحظات هنا).
    def update(self, instance, validated_data):
        # يمكنك تحديث الملاحظات أو أي حقول أخرى هنا.
        instance.notes = validated_data.get('notes', instance.notes)
        instance.save()
        return instance

# OrderStatusUpdateSerializer: سيريالايزر مخصص لتحديث حالة الطلب فقط.
class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']
        # كل الحقول الأخرى للقراءة فقط عند استخدام هذا السيريالايزر.
        read_only_fields = ['id', 'customer', 'order_date', 'total_amount', 'notes']

    # التحقق من صحة قيمة الحالة المدخلة.
    def validate_status(self, value):
        valid_statuses = [choice[0] for choice in Order.STATUS_CHOICES]
        if value not in valid_statuses:
            raise serializers.ValidationError(f"'{value}' ليست حالة طلب صالحة. الحالات الصالحة هي: {', '.join(valid_statuses)}")
        return value