# account/admin.py
from django.contrib import admin
from .models import Customer # استيراد نموذج Customer الخاص بك

# تسجيل نموذج Customer في لوحة الإدارة
admin.site.register(Customer)