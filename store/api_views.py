# store/api_views.py

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import Count, Sum


from product.models import Product
from order.models import Order, OrderItem
from account.models import Customer


from store.permissions import IsAdminOrSeller

class DashboardStatsAPIView(APIView):
    # تطبيق الصلاحية: فقط المشرفون والبائعون يمكنهم الوصول
    permission_classes = [IsAdminOrSeller]

    def get(self, request, format=None):
        # 1. إجمالي العملاء
        total_customers = Customer.objects.count()

        # 2. إجمالي الطلبات
        total_orders = Order.objects.count()

        # 3. إجمالي المنتجات
        total_products = Product.objects.count()

        # 4. أفضل 5 منتجات تم طلبها
        
        top_ordered_products_data = []
        top_products_query = Product.objects.annotate(
            total_ordered=Sum('orderitem__quantity')
        ).filter(
            total_ordered__isnull=False
        ).order_by(
            '-total_ordered'
        )[:5]

        for product in top_products_query:
            top_ordered_products_data.append({
                'id': product.id,
                'name': product.name,
                'total_ordered_quantity': product.total_ordered,
                'price': float(product.price), # تحويل Decimal إلى float لتجنب مشاكل JSON
                'image_url': product.image_url
            })
          # الإحصائية الجديدة: إجمالي الطلبات المكتملة
        # -----------------------------------------------------
        # افترض أن لديك حقلاً اسمه 'status' في نموذج Order وقيمته 'completed'
        total_completed_orders = Order.objects.filter(status='completed').count()
        
        # -----------------------------------------------------
        # تجميع كل الإحصائيات في قاموس واحد
        data = {
            'total_customers': total_customers,
            'total_orders': total_orders,
            'total_products': total_products,
            'top_5_ordered_products': top_ordered_products_data,
            'total_completed_orders': total_completed_orders,
        }
        return Response(data, status=status.HTTP_200_OK)