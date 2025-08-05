from django.core.management.base import BaseCommand
from product.models import Category, Product, ProductReview
from account.models import Customer
from order.models import Order, OrderItem
from django.contrib.auth.hashers import make_password
from django.utils import timezone
import random


class Command(BaseCommand):
    help = 'Loads sample data into the database'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Deleting old data...'))
        Category.objects.all().delete()
        Product.objects.all().delete()
        Customer.objects.all().delete()
        Order.objects.all().delete()
        OrderItem.objects.all().delete()
        ProductReview.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Creating sample data...'))

        # Create Categories
        categories_data = [
            {'name': 'Electronics', 'description': 'Gadgets and electronic devices'},
            {'name': 'Apparel', 'description': 'Clothing and fashion items'},
            {'name': 'Books', 'description': 'Various genres of books'},
            {'name': 'Home & Kitchen', 'description': 'Appliances and decor for home'},
            {'name': 'Sports & Outdoors', 'description': 'Equipment for sports and outdoor activities'},
        ]
        categories = []
        for data in categories_data:
            category = Category.objects.create(**data)
            categories.append(category)
            self.stdout.write(self.style.SUCCESS(f'Created Category: {category.name}'))

        # Create Customers
        customers_data = [
            {'username': 'admin_user', 'email': 'admin@example.com', 'password': 'password123', 'first_name': 'Admin',
             'last_name': 'User', 'phone': '1234567890', 'address': '123 Admin St', 'role': 'admin'},
            {'username': 'seller_user', 'email': 'seller@example.com', 'password': 'password123',
             'first_name': 'Seller', 'last_name': 'User', 'phone': '0987654321', 'address': '456 Seller Ave',
             'role': 'seller'},
            {'username': 'customer1', 'email': 'customer1@example.com', 'password': 'password123', 'first_name': 'John',
             'last_name': 'Doe', 'phone': '1112223333', 'address': '789 Customer Rd', 'role': 'customer'},
            {'username': 'customer2', 'email': 'customer2@example.com', 'password': 'password123', 'first_name': 'Jane',
             'last_name': 'Smith', 'phone': '4445556666', 'address': '101 Client Blvd', 'role': 'customer'},
            {'username': 'customer3', 'email': 'customer3@example.com', 'password': 'password123',
             'first_name': 'Peter', 'last_name': 'Jones', 'phone': '7778889999', 'address': '202 Buyer Lane',
             'role': 'customer'},
        ]
        customers = []
        for data in customers_data:
            data['password'] = make_password(data['password'])
            customer = Customer.objects.create(**data)
            customers.append(customer)
            self.stdout.write(self.style.SUCCESS(f'Created Customer: {customer.email}'))

        # Create Products
        products_data = [
            {'name': 'Laptop', 'description': 'Powerful laptop for work and gaming', 'price': 1200.00,
             'category': categories[0], 'stock_quantity': 10, 'is_available': True,
             'image_url': 'https://example.com/laptop.jpg'},
            {'name': 'Smartphone', 'description': 'Latest model smartphone with great camera', 'price': 800.00,
             'category': categories[0], 'stock_quantity': 25, 'is_available': True,
             'image_url': 'https://example.com/smartphone.jpg'},
            {'name': 'Headphones', 'description': 'Noise-cancelling over-ear headphones', 'price': 150.00,
             'category': categories[0], 'stock_quantity': 50, 'is_available': True,
             'image_url': 'https://example.com/headphones.jpg'},
            {'name': 'T-Shirt', 'description': 'Comfortable cotton t-shirt', 'price': 25.00, 'category': categories[1],
             'stock_quantity': 100, 'is_available': True, 'image_url': 'https://example.com/tshirt.jpg'},
            {'name': 'Jeans', 'description': 'Stylish denim jeans', 'price': 60.00, 'category': categories[1],
             'stock_quantity': 70, 'is_available': True, 'image_url': 'https://example.com/jeans.jpg'},
            {'name': 'Dress', 'description': 'Elegant evening dress', 'price': 90.00, 'category': categories[1],
             'stock_quantity': 40, 'is_available': True, 'image_url': 'https://example.com/dress.jpg'},
            {'name': 'The Great Gatsby', 'description': 'Classic novel by F. Scott Fitzgerald', 'price': 15.00,
             'category': categories[2], 'stock_quantity': 30, 'is_available': True,
             'image_url': 'https://example.com/gatsby.jpg'},
            {'name': '1984', 'description': 'Dystopian social science fiction novel by George Orwell', 'price': 12.00,
             'category': categories[2], 'stock_quantity': 20, 'is_available': True,
             'image_url': 'https://example.com/1984.jpg'},
            {'name': 'Kitchen Mixer', 'description': 'Stand mixer for baking', 'price': 200.00,
             'category': categories[3], 'stock_quantity': 15, 'is_available': True,
             'image_url': 'https://example.com/mixer.jpg'},
            {'name': 'Coffee Maker', 'description': 'Automatic drip coffee maker', 'price': 75.00,
             'category': categories[3], 'stock_quantity': 35, 'is_available': True,
             'image_url': 'https://example.com/coffee.jpg'},
            {'name': 'Yoga Mat', 'description': 'Non-slip yoga mat for fitness', 'price': 30.00,
             'category': categories[4], 'stock_quantity': 60, 'is_available': True,
             'image_url': 'https://example.com/yogamat.jpg'},
            {'name': 'Camping Tent', 'description': 'Lightweight 2-person camping tent', 'price': 180.00,
             'category': categories[4], 'stock_quantity': 10, 'is_available': True,
             'image_url': 'https://example.com/tent.jpg'},
            {'name': 'Smartwatch', 'description': 'Fitness tracker and smartwatch', 'price': 250.00,
             'category': categories[0], 'stock_quantity': 18, 'is_available': True,
             'image_url': 'https://example.com/smartwatch.jpg'},
            {'name': 'Running Shoes', 'description': 'Comfortable running shoes for daily use', 'price': 85.00,
             'category': categories[4], 'stock_quantity': 55, 'is_available': True,
             'image_url': 'https://example.com/runningshoes.jpg'},
            {'name': 'Cookware Set', 'description': 'Non-stick cookware set', 'price': 120.00,
             'category': categories[3], 'stock_quantity': 22, 'is_available': True,
             'image_url': 'https://example.com/cookwareset.jpg'},
        ]
        products = []
        for data in products_data:
            product = Product.objects.create(**data)
            products.append(product)
            self.stdout.write(self.style.SUCCESS(f'Created Product: {product.name}'))

        # Create Orders and OrderItems
        for i in range(5):
            customer = random.choice(customers)
            order = Order.objects.create(customer=customer, order_date=timezone.now(), status='New', total_amount=0.00)
            self.stdout.write(self.style.SUCCESS(f'Created Order {order.id} for {customer.email}'))

            num_items = random.randint(1, 3)  # Each order has 1 to 3 items
            order_total = 0
            selected_products = random.sample(products, num_items)

            for prod in selected_products:
                quantity = random.randint(1, prod.stock_quantity // 2 if prod.stock_quantity > 1 else 1)
                if quantity == 0:  # Ensure quantity is at least 1 if stock is 1
                    quantity = 1

                order_item = OrderItem.objects.create(
                    order=order,
                    product=prod,
                    quantity=quantity,
                    price_at_time=prod.price
                )
                order_total += order_item.get_total()
                prod.stock_quantity -= quantity
                prod.save()
                self.stdout.write(self.style.SUCCESS(f'  - Added {quantity} of {prod.name}'))

            order.total_amount = order_total
            order.save()
            self.stdout.write(self.style.SUCCESS(f'  - Order {order.id} total: {order.total_amount}'))

        # Create some Product Reviews
        for _ in range(5):
            product = random.choice(products)
            customer = random.choice(customers)
            rating = random.randint(1, 5)
            comment = f'This is a great product! Rating: {rating} stars.'
            try:
                ProductReview.objects.create(product=product, user=customer, rating=rating, comment=comment)
                self.stdout.write(self.style.SUCCESS(f'Created review for {product.name} by {customer.username}'))
            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(f'Could not create review for {product.name} by {customer.username}: {e}'))

        self.stdout.write(self.style.SUCCESS('Sample data loading complete.'))


