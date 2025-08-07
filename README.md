# ARABIC
# 🛒 E-commerce_Store_DRF

مشروع متجر إلكتروني مبني باستخدام Django و Django REST Framework، يوفّر واجهات API لإدارة المنتجات، الطلبات، والعملاء، مع دعم للمصادقة، التصفية، والتحكم في الصلاحيات.

---

## 🚀 الميزات

- إدارة المنتجات: إضافة، تعديل، عرض، والتحكم في المخزون
- إدارة الطلبات: إنشاء طلبات متعددة العناصر، حساب الإجمالي، وتحديث الحالة
- إدارة العملاء: تسجيل، ربط الطلبات، والتحقق من الصلاحيات
- مصادقة JWT
- صلاحيات مخصصة (مشرف، بائع، عميل)
- تصفية واستعلام ديناميكي باستخدام `django-filter`
- اختبارات باستخدام `pytest` و `pytest-django`

---

## 🧱 الهيكلية

E-commerce_Store_DRF/ ├── account/ # إدارة العملاء والمستخدمين ├── product/ # إدارة المنتجات والمخزون ├── order/ # إدارة الطلبات وعناصر الطلب ├── store/ # صلاحيات مخصصة ├── config/ # إعدادات المشروع ├── requirements.txt ├── README.md


---

## ⚙️ التشغيل المحلي

### 1. إنشاء البيئة الافتراضية

```bash
python -m venv venv
source venv/Scripts/activate  # على Windows
2. تثبيت المتطلبات
bash
pip install -r requirements.txt
3. إعداد قاعدة البيانات
bash
python manage.py makemigrations
python manage.py migrate
4. تشغيل الخادم
bash
python manage.py runserver
🔐 المصادقة
يتم استخدام JWT عبر مكتبة djangorestframework-simplejwt. بعد تسجيل الدخول، يتم إرسال التوكن في الهيدر:

http
Authorization: Bearer <your_token>
🧪 الاختبارات
تشغيل جميع الاختبارات:
bash
pytest
اختبار ملف معين:
bash
pytest order/tests/test_views.py
📦 واجهات API
المسار	الوظيفة
/api/products/	عرض المنتجات
/api/orders/	إنشاء وعرض الطلبات
/api/orders/<id>/status/	تحديث حالة الطلب
/api/order-items/	عرض عناصر الطلب
/api/account/register/	تسجيل عميل جديد
👨‍💻 الفريق
Essa — Backend Developer & Architect
Ali — Backend Developer & Architect
Rama — Backend Developer & Architect
Zahraa — Backend Developer & Architect

📄 الرخصة
هذا المشروع مفتوح المصدر لأغراض تعليمية وتطويرية. يمكنك استخدامه وتعديله بحرية.


---

# ENGLISH
# 🛒 E-commerce_Store_DRF

A modular and scalable e-commerce backend built with Django and Django REST Framework (DRF). This project provides secure APIs for managing products, orders, and customers, with support for JWT authentication, role-based permissions, and dynamic filtering.

---

## 🚀 Features

- **Product Management**: Create, update, list, and manage stock
- **Order System**: Multi-item orders, automatic total calculation, status updates
- **Customer Accounts**: Registration, role-based access, and order history
- **JWT Authentication**: Secure login and token-based access
- **Custom Permissions**: Admin, Seller, and Customer roles
- **Filtering & Pagination**: Powered by `django-filter` and DRF pagination
- **Testing Suite**: Built with `pytest` and `pytest-django`

---

## 🧱 Project Structure

E-commerce_Store_DRF/ ├── account/ # Customer and user management ├── product/ # Product and inventory logic ├── order/ # Orders and order items ├── store/ # Custom permissions ├── config/ # Django settings and root URLs ├── requirements.txt ├── README.md


---

## ⚙️ Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/E-commerce_Store_DRF.git
cd E-commerce_Store_DRF
2. Create and activate a virtual environment
bash
python -m venv venv
source venv/Scripts/activate  # On Windows
3. Install dependencies
bash
pip install -r requirements.txt
4. Set up the database
bash
python manage.py makemigrations
python manage.py migrate
5. Create a superuser (optional)
bash
python manage.py createsuperuser
6. Run the development server
bash
python manage.py runserver
🔐 Authentication
JWT is used for secure authentication via djangorestframework-simplejwt. After login, include the token in your request headers:

http
Authorization: Bearer <your_token>
📦 API Endpoints
Endpoint	Description
/api/products/	List and manage products
/api/orders/	Create and view orders
/api/orders/<id>/status/	Update order status
/api/order-items/	View order items
/api/account/register/	Register a new customer
🧪 Running Tests
Run all tests:
bash
pytest
Run a specific test file:
bash
pytest order/tests/test_views.py
🧰 Technologies Used
Django

Django REST Framework

MySQL (or SQLite for local testing)

Pytest

JWT (via djangorestframework-simplejwt)

Django Filter

👨‍💻 Developer
Essa — Backend Developer & System Architect
Ali — Backend Developer & System Architect
Rama — Backend Developer & System Architect
Zahraa — Backend Developer & System Architect

📄 License
This project is open-source and intended for educational and development purposes. Feel free to use, modify, and extend it.


---
