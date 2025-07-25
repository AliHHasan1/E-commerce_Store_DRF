from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.db import transaction
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from order.models import Order, OrderItem
from product.models.product_models import Product  
from account.models import Customer  

from order.serializers.order_serializers import OrderSerializer, OrderStatusUpdateSerializer


class OrderViewSet(
    mixins.ListModelMixin,       # GET /api/orders/
    mixins.RetrieveModelMixin,    # GET /api/orders/{id}/
    mixins.CreateModelMixin,      # POST /api/orders/
    mixins.DestroyModelMixin,     # DELETE /api/orders/{id}/
    viewsets.GenericViewSet
):
  
    queryset = Order.objects.all().select_related('customer').prefetch_related('items__product')
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['customer', 'status']  # تصفية الطلبات حسب العميل والحالة
    permission_classes = [IsAuthenticated]  # افتراضيًا، جميع الإجراءات تتطلب مصادقة

    def get_queryset(self):
        """
        يقوم بتصفية مجموعة الاستعلام بناءً على أذونات المستخدم:
        - يمكن للمشرفين (is_superuser) رؤية جميع الطلبات.
        - يمكن للعملاء (customer) رؤية طلباتهم فقط.
        - لـ `/customers/{id}/orders/`، يتم تصفية الطلبات حسب العميل المحدد.
        """
        user = self.request.user
        queryset = super().get_queryset() # ابدأ بمجموعة الاستعلام الافتراضية للـ ViewSet

        # إذا كان الطلب من نقطة نهاية 'customer_orders' (مسار مخصص)
        if self.action == 'customer_orders':
            customer_id = self.kwargs.get('pk') # الـ pk هنا هو معرف العميل
            customer = get_object_or_404(Customer, pk=customer_id)

            # فقط المشرفون يمكنهم رؤية طلبات أي عميل
            if user.is_superuser:
                return queryset.filter(customer=customer)
            # العميل نفسه يمكنه رؤية طلباته فقط
            elif hasattr(user, 'customer') and user.customer == customer:
                return queryset.filter(customer=customer)
            else:
                raise PermissionDenied("ليس لديك الإذن لرؤية طلبات هذا العميل.")
        
        # المنطق الافتراضي لـ list و retrieve
        if user.is_superuser:
            return queryset
        elif hasattr(user, 'customer') and user.customer:
            return queryset.filter(customer=user.customer)
        return Order.objects.none() # إذا لم يكن المستخدم مشرفًا أو عميلاً مرتبطًا، فلا يرى أي طلبات

    def create(self, request, *args, **kwargs):
        """
        ينشئ طلبًا جديدًا، ويتحقق من توفر المنتج والمخزون، ويخصم الكمية، ويحسب الإجمالي.
        يتوقع بيانات الطلب الأساسية في جذر الـ JSON، وقائمة 'items' منفصلة.
        """
        # 1. تحقق من صحة بيانات الطلب الأساسية (Order data)
        order_serializer = self.get_serializer(data=request.data)
        order_serializer.is_valid(raise_exception=True)

        # 2. استخراج بيانات عناصر الطلب
        items_data = request.data.get('items', [])
        if not items_data:
            raise ValidationError({"items": "يجب أن يحتوي الطلب على عناصر."})

        # 3. معالجة وتدقيق كل عنصر طلب قبل الإنشاء الفعلي
        processed_items = []
        for item_data in items_data:
            product_id = item_data.get('product_id')
            quantity = item_data.get('quantity')

            # التحقق من المدخلات الأساسية لعنصر الطلب
            if not product_id or not quantity:
                raise ValidationError({"items": "كل عنصر يجب أن يحتوي على معرف المنتج والكمية."})
            if not isinstance(quantity, int) or quantity <= 0:
                raise ValidationError({"items": f"الكمية للمنتج {product_id} يجب أن تكون عددًا صحيحًا موجبًا."})

            # جلب المنتج والتحقق من وجوده وتوفره
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                raise ValidationError({"items": f"المنتج بمعرف {product_id} غير موجود."})

            if not product.is_available:
                raise ValidationError({"items": f"المنتج '{product.name}' غير متوفر للشراء حاليًا."})

            # التحقق من المخزون الكافي
            if product.stock_quantity < quantity:
                raise ValidationError({
                    "items": f"لا يوجد مخزون كافٍ للمنتج '{product.name}'. المتوفر: {product.stock_quantity}، المطلوب: {quantity}."
                })
            
            # تخزين بيانات العنصر التي تم التحقق منها للاستخدام لاحقًا
            processed_items.append({
                'product': product,
                'quantity': quantity,
                'price_at_time': product.price  # حفظ سعر المنتج وقت الطلب
            })
        
        # 4. تنفيذ عملية الإنشاء الفعلية (معاملة ذرية)
        self.perform_create(order_serializer, processed_items)
        headers = self.get_success_headers(order_serializer.data)
        return Response(order_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer, processed_items):
        """
        طريقة الإنشاء المخصصة لحفظ الطلب، وإنشاء عناصر الطلب، وتقليل المخزون، وحساب الإجمالي.
        """
        customer_instance = None
        # تعيين العميل بناءً على المستخدم المصدق عليه (إذا كان عميلاً)
        if hasattr(self.request.user, 'customer') and self.request.user.customer:
            customer_instance = self.request.user.customer
        # السماح للمشرفين بتحديد العميل يدوياً
        elif 'customer' in serializer.validated_data:
            customer_instance = serializer.validated_data['customer']
            # تحقق إضافي إذا كان المستخدم ليس مشرفًا وحاول تحديد عميل آخر
            if not self.request.user.is_superuser:
                raise PermissionDenied("ليس لديك الإذن لإنشاء طلبات لعملاء آخرين.")
        else:
            raise ValidationError({"customer": "يجب تحديد العميل لإنشاء الطلب."})

        total_amount = 0
        order_items_to_create = []

        with transaction.atomic():  # ضمان أن العملية بأكملها تتم بنجاح أو تفشل بالكامل
            # إنشاء الطلب الأساسي
            order = serializer.save(customer=customer_instance, status='New', total_amount=0.00)

            # المرور على كل عنصر لإنشاء OrderItem وتقليل المخزون
            for item_data in processed_items:
                product = item_data['product']
                quantity = item_data['quantity']
                price_at_time = item_data['price_at_time']

                # خصم كمية المخزون
                product.stock_quantity -= quantity
                product.save()

                # إضافة قيمة العنصر إلى الإجمالي الكلي للطلب
                total_amount += price_at_time * quantity

                # تجميع عناصر الطلب ليتم إنشاؤها بالجملة
                order_items_to_create.append(
                    OrderItem(order=order, product=product, quantity=quantity, price_at_time=price_at_time)
                )

            # إنشاء جميع عناصر الطلب دفعة واحدة لأداء أفضل
            OrderItem.objects.bulk_create(order_items_to_create)

           
            order.total_amount = total_amount
            order.save()

    @action(detail=True, methods=['put'], serializer_class=OrderStatusUpdateSerializer,
            url_path='status')
    def update_status(self, request, pk=None):
        """
        إجراء مخصص لتحديث حالة الطلب.
        فقط المستخدمون المشرفون يمكنهم تحديث الحالة.
        """
        order = self.get_object()
        user = request.user

        
        if not user.is_superuser:
            raise PermissionDenied("ليس لديك الإذن لتحديث حالة الطلب.")

        serializer = self.get_serializer(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        طريقة مخصصة لحذف الطلبات.
        تقييد الحذف للمشرفين فقط.
        """
        user = request.user
        if not user.is_superuser:
            raise PermissionDenied("ليس لديك الإذن لحذف الطلب.")

        return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=['get'], url_path='by-customer/(?P<pk>[^/.]+)', name='customer-orders')
    def customer_orders(self, request, pk=None):
        """
        نقطة نهاية مخصصة لسرد جميع طلبات عميل محدد.
        المشرفون يمكنهم رؤية طلبات أي عميل.
        العميل يمكنه رؤية طلباته فقط.
        """
      
        queryset = self.get_queryset()
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)