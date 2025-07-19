from django.urls import path, include
from rest_framework.routers import DefaultRouter
from account.views import CustomerViewSet

router = DefaultRouter()
router.register(r'customer', CustomerViewSet)
urlpatterns = [
    path('api/', include(router.urls)),
]