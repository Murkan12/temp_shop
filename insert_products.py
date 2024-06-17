import os
import django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'temp_shop.settings')
django.setup()

from temp_shop_ecommerce.models import Product

products = [
    Product(
        name="Wireless Bluetooth Earbuds",
        description="High-quality sound with noise-canceling feature. Long battery life and comfortable fit.",
        price=49.99,
        stored_quantity=120,
        category="Electronics",
        is_active=True,
        created_at=datetime.now(),
        updated_at=datetime.now()
    ),
    Product(
        name="Smartphone Holder for Car",
        description="Universal smartphone holder with 360-degree rotation and strong suction cup.",
        price=15.99,
        stored_quantity=200,
        category="Automotive",
        is_active=True,
        created_at=datetime.now(),
        updated_at=datetime.now()
    ),
    Product(
        name="Organic Green Tea",
        description="100% organic green tea leaves. Rich in antioxidants and great for health.",
        price=9.49,
        stored_quantity=150,
        category="Food & Beverages",
        is_active=True,
        created_at=datetime.now(),
        updated_at=datetime.now()
    ),
    Product(
        name="Waterproof Fitness Tracker",
        description="Track your daily activities and monitor your heart rate with this waterproof fitness tracker.",
        price=29.99,
        stored_quantity=90,
        category="Fitness",
        is_active=True,
        created_at=datetime.now(),
        updated_at=datetime.now()
    ),
    Product(
        name="Portable Power Bank 10000mAh",
        description="Compact and lightweight power bank with fast charging capabilities. Suitable for all devices.",
        price=22.99,
        stored_quantity=75,
        category="Electronics",
        is_active=True,
        created_at=datetime.now(),
        updated_at=datetime.now()
    ),
    Product(
        name="Ergonomic Office Chair",
        description="Comfortable and adjustable office chair with lumbar support. Ideal for long hours of work.",
        price=199.99,
        stored_quantity=30,
        category="Furniture",
        is_active=True,
        created_at=datetime.now(),
        updated_at=datetime.now()
    ),
    Product(
        name="Stainless Steel Water Bottle",
        description="Insulated stainless steel water bottle keeps your drinks hot or cold for hours.",
        price=18.99,
        stored_quantity=120,
        category="Home & Kitchen",
        is_active=True,
        created_at=datetime.now(),
        updated_at=datetime.now()
    ),
    Product(
        name="Noise Cancelling Headphones",
        description="Premium over-ear headphones with noise cancellation and superior sound quality.",
        price=89.99,
        stored_quantity=60,
        category="Electronics",
        is_active=True,
        created_at=datetime.now(),
        updated_at=datetime.now()
    ),
    Product(
        name="Yoga Mat with Carrying Strap",
        description="Non-slip yoga mat with a convenient carrying strap. Perfect for all types of yoga and exercise.",
        price=24.99,
        stored_quantity=100,
        category="Fitness",
        is_active=True,
        created_at=datetime.now(),
        updated_at=datetime.now()
    ),
    Product(
        name="LED Desk Lamp",
        description="Adjustable LED desk lamp with touch control and multiple brightness levels.",
        price=34.99,
        stored_quantity=85,
        category="Home & Kitchen",
        is_active=True,
        created_at=datetime.now(),
        updated_at=datetime.now()
    ),
    Product(
        name="Stainless Steel Cookware Set",
        description="10-piece stainless steel cookware set with glass lids. Suitable for all cooktops.",
        price=129.99,
        stored_quantity=45,
        category="Home & Kitchen",
        is_active=True,
        created_at=datetime.now(),
        updated_at=datetime.now()
    ),
    Product(
        name="Wireless Gaming Mouse",
        description="High-precision wireless gaming mouse with customizable DPI settings and RGB lighting.",
        price=39.99,
        stored_quantity=70,
        category="Electronics",
        is_active=True,
        created_at=datetime.now(),
        updated_at=datetime.now()
    ),
    Product(
        name="Electric Kettle",
        description="1.7L electric kettle with auto shut-off and boil-dry protection. Fast boiling.",
        price=25.99,
        stored_quantity=110,
        category="Home & Kitchen",
        is_active=True,
        created_at=datetime.now(),
        updated_at=datetime.now()
    ),
    Product(
        name="Digital Bathroom Scale",
        description="Accurate digital bathroom scale with a large display and step-on technology.",
        price=19.99,
        stored_quantity=95,
        category="Home & Kitchen",
        is_active=True,
        created_at=datetime.now(),
        updated_at=datetime.now()
    ),
    Product(
        name="Camping Tent for 4 People",
        description="Spacious and easy-to-set-up camping tent for 4 persons. Waterproof and durable.",
        price=79.99,
        stored_quantity=50,
        category="Outdoors",
        is_active=True,
        created_at=datetime.now(),
        updated_at=datetime.now()
    ),
]

# Save the products to the database
for product in products:
    product.save()