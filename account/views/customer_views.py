from rest_framework import viewsets
from account.models import Customer
from account.serializers import CustomerSerializer
from store.permissions import UserPermissions
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [UserPermissions]