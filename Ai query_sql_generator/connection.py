from datetime import datetime

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Numeric,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import declarative_base, sessionmaker


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

DATABASE_URL = "sqlite:///sql_agent_demo.db"

engine = create_engine(
    DATABASE_URL,
    echo=False,
)

Base = declarative_base()

SessionLocal = sessionmaker(
    bind=engine
)


# ============================================================
# CUSTOMER TABLE
# ============================================================

class Customer(Base):

    __tablename__ = "customers"

    customer_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    customer_name = Column(
        String(100),
        nullable=False,
    )

    email = Column(
        String(150),
        unique=True,
        nullable=False,
    )

    city = Column(
        String(100),
    )

    country = Column(
        String(100),
    )

    created_at = Column(
        DateTime,
        default=datetime.now,
    )


# ============================================================
# PRODUCT TABLE
# ============================================================

class Product(Base):

    __tablename__ = "products"

    product_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    product_name = Column(
        String(150),
        nullable=False,
    )

    category = Column(
        String(100),
    )

    price = Column(
        Numeric(10, 2),
        nullable=False,
    )

    stock_quantity = Column(
        Integer,
        default=0,
    )

    created_at = Column(
        DateTime,
        default=datetime.now,
    )


# ============================================================
# ORDER TABLE
# ============================================================

class Order(Base):

    __tablename__ = "orders"

    order_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    customer_id = Column(
        Integer,
        ForeignKey("customers.customer_id"),
        nullable=False,
    )

    order_date = Column(
        DateTime,
        nullable=False,
    )

    status = Column(
        String(50),
        nullable=False,
    )


# ============================================================
# ORDER ITEM TABLE
# ============================================================

class OrderItem(Base):

    __tablename__ = "order_items"

    order_item_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    order_id = Column(
        Integer,
        ForeignKey("orders.order_id"),
        nullable=False,
    )

    product_id = Column(
        Integer,
        ForeignKey("products.product_id"),
        nullable=False,
    )

    quantity = Column(
        Integer,
        nullable=False,
    )

    unit_price = Column(
        Numeric(10, 2),
        nullable=False,
    )


# ============================================================
# CREATE TABLES
# ============================================================

def create_tables():

    Base.metadata.create_all(engine)

    print("Tables created successfully.")


# ============================================================
# INSERT CUSTOMERS
# ============================================================

def insert_customers(session):

    customers = [
        Customer(
            customer_name="Rahul Sharma",
            email="rahul@example.com",
            city="Pune",
            country="India",
        ),

        Customer(
            customer_name="Amit Patel",
            email="amit@example.com",
            city="Mumbai",
            country="India",
        ),

        Customer(
            customer_name="Priya Deshmukh",
            email="priya@example.com",
            city="Pune",
            country="India",
        ),

        Customer(
            customer_name="Sneha Joshi",
            email="sneha@example.com",
            city="Delhi",
            country="India",
        ),

        Customer(
            customer_name="Rohan Mehta",
            email="rohan@example.com",
            city="Bangalore",
            country="India",
        ),

        Customer(
            customer_name="Neha Kulkarni",
            email="neha@example.com",
            city="Nashik",
            country="India",
        ),

        Customer(
            customer_name="Arjun Singh",
            email="arjun@example.com",
            city="Delhi",
            country="India",
        ),

        Customer(
            customer_name="Kavita Shah",
            email="kavita@example.com",
            city="Mumbai",
            country="India",
        ),

        Customer(
            customer_name="Vikram Patil",
            email="vikram@example.com",
            city="Pune",
            country="India",
        ),

        Customer(
            customer_name="Anjali Rao",
            email="anjali@example.com",
            city="Hyderabad",
            country="India",
        ),
    ]

    session.add_all(customers)

    session.flush()

    print("Customers inserted successfully.")


# ============================================================
# INSERT PRODUCTS
# ============================================================

def insert_products(session):

    products = [
        Product(
            product_name="Laptop Pro 14",
            category="Laptops",
            price=85000,
            stock_quantity=25,
        ),

        Product(
            product_name="Laptop Air 13",
            category="Laptops",
            price=65000,
            stock_quantity=30,
        ),

        Product(
            product_name="Wireless Mouse",
            category="Accessories",
            price=1500,
            stock_quantity=100,
        ),

        Product(
            product_name="Mechanical Keyboard",
            category="Accessories",
            price=4500,
            stock_quantity=60,
        ),

        Product(
            product_name="27 Inch Monitor",
            category="Monitors",
            price=22000,
            stock_quantity=40,
        ),

        Product(
            product_name="USB-C Hub",
            category="Accessories",
            price=3500,
            stock_quantity=75,
        ),

        Product(
            product_name="Gaming Headset",
            category="Audio",
            price=7500,
            stock_quantity=50,
        ),

        Product(
            product_name="Webcam HD",
            category="Accessories",
            price=5500,
            stock_quantity=35,
        ),

        Product(
            product_name="Smartphone X",
            category="Mobile",
            price=55000,
            stock_quantity=45,
        ),

        Product(
            product_name="Tablet Pro",
            category="Tablets",
            price=42000,
            stock_quantity=20,
        ),
    ]

    session.add_all(products)

    session.flush()

    print("Products inserted successfully.")


# ============================================================
# INSERT ORDERS
# ============================================================

def insert_orders(session):

    orders = [
        Order(
            customer_id=1,
            order_date=datetime(2026, 1, 10, 10, 30),
            status="COMPLETED",
        ),

        Order(
            customer_id=2,
            order_date=datetime(2026, 1, 15, 14, 20),
            status="COMPLETED",
        ),

        Order(
            customer_id=3,
            order_date=datetime(2026, 2, 5, 11, 15),
            status="COMPLETED",
        ),

        Order(
            customer_id=4,
            order_date=datetime(2026, 2, 20, 16, 40),
            status="COMPLETED",
        ),

        Order(
            customer_id=5,
            order_date=datetime(2026, 3, 1, 9, 30),
            status="COMPLETED",
        ),

        Order(
            customer_id=1,
            order_date=datetime(2026, 3, 15, 12, 10),
            status="COMPLETED",
        ),

        Order(
            customer_id=6,
            order_date=datetime(2026, 4, 2, 15, 0),
            status="COMPLETED",
        ),

        Order(
            customer_id=7,
            order_date=datetime(2026, 4, 18, 18, 20),
            status="CANCELLED",
        ),

        Order(
            customer_id=8,
            order_date=datetime(2026, 5, 5, 13, 10),
            status="COMPLETED",
        ),

        Order(
            customer_id=9,
            order_date=datetime(2026, 5, 20, 11, 45),
            status="COMPLETED",
        ),

        Order(
            customer_id=10,
            order_date=datetime(2026, 6, 1, 17, 30),
            status="COMPLETED",
        ),

        Order(
            customer_id=2,
            order_date=datetime(2026, 6, 15, 10, 20),
            status="COMPLETED",
        ),

        Order(
            customer_id=3,
            order_date=datetime(2026, 7, 1, 14, 0),
            status="COMPLETED",
        ),

        Order(
            customer_id=5,
            order_date=datetime(2026, 7, 10, 16, 15),
            status="COMPLETED",
        ),

        Order(
            customer_id=1,
            order_date=datetime(2026, 7, 20, 12, 30),
            status="COMPLETED",
        ),
    ]

    session.add_all(orders)

    session.flush()

    print("Orders inserted successfully.")


# ============================================================
# INSERT ORDER ITEMS
# ============================================================

def insert_order_items(session):

    order_items = [
        # Order 1
        OrderItem(
            order_id=1,
            product_id=1,
            quantity=1,
            unit_price=85000,
        ),

        OrderItem(
            order_id=1,
            product_id=3,
            quantity=2,
            unit_price=1500,
        ),

        # Order 2
        OrderItem(
            order_id=2,
            product_id=2,
            quantity=1,
            unit_price=65000,
        ),

        OrderItem(
            order_id=2,
            product_id=4,
            quantity=1,
            unit_price=4500,
        ),

        # Order 3
        OrderItem(
            order_id=3,
            product_id=5,
            quantity=1,
            unit_price=22000,
        ),

        OrderItem(
            order_id=3,
            product_id=6,
            quantity=2,
            unit_price=3500,
        ),

        # Order 4
        OrderItem(
            order_id=4,
            product_id=9,
            quantity=1,
            unit_price=55000,
        ),

        OrderItem(
            order_id=4,
            product_id=7,
            quantity=1,
            unit_price=7500,
        ),

        # Order 5
        OrderItem(
            order_id=5,
            product_id=10,
            quantity=1,
            unit_price=42000,
        ),

        OrderItem(
            order_id=5,
            product_id=8,
            quantity=1,
            unit_price=5500,
        ),

        # Order 6
        OrderItem(
            order_id=6,
            product_id=1,
            quantity=1,
            unit_price=85000,
        ),

        OrderItem(
            order_id=6,
            product_id=6,
            quantity=1,
            unit_price=3500,
        ),

        # Order 7
        OrderItem(
            order_id=7,
            product_id=4,
            quantity=2,
            unit_price=4500,
        ),

        OrderItem(
            order_id=7,
            product_id=3,
            quantity=1,
            unit_price=1500,
        ),

        # Order 8
        OrderItem(
            order_id=8,
            product_id=2,
            quantity=1,
            unit_price=65000,
        ),

        # Order 9
        OrderItem(
            order_id=9,
            product_id=9,
            quantity=1,
            unit_price=55000,
        ),

        OrderItem(
            order_id=9,
            product_id=7,
            quantity=1,
            unit_price=7500,
        ),

        # Order 10
        OrderItem(
            order_id=10,
            product_id=5,
            quantity=2,
            unit_price=22000,
        ),

        # Order 11
        OrderItem(
            order_id=11,
            product_id=10,
            quantity=1,
            unit_price=42000,
        ),

        OrderItem(
            order_id=11,
            product_id=3,
            quantity=2,
            unit_price=1500,
        ),

        # Order 12
        OrderItem(
            order_id=12,
            product_id=1,
            quantity=1,
            unit_price=85000,
        ),

        OrderItem(
            order_id=12,
            product_id=4,
            quantity=1,
            unit_price=4500,
        ),

        # Order 13
        OrderItem(
            order_id=13,
            product_id=2,
            quantity=1,
            unit_price=65000,
        ),

        OrderItem(
            order_id=13,
            product_id=8,
            quantity=1,
            unit_price=5500,
        ),

        # Order 14
        OrderItem(
            order_id=14,
            product_id=9,
            quantity=1,
            unit_price=55000,
        ),

        OrderItem(
            order_id=14,
            product_id=6,
            quantity=2,
            unit_price=3500,
        ),

        # Order 15
        OrderItem(
            order_id=15,
            product_id=1,
            quantity=1,
            unit_price=85000,
        ),

        OrderItem(
            order_id=15,
            product_id=7,
            quantity=1,
            unit_price=7500,
        ),
    ]

    session.add_all(order_items)

    session.flush()

    print("Order items inserted successfully.")


# ============================================================
# VERIFY DATA
# ============================================================

def verify_database(session):

    customer_count = session.query(Customer).count()
    product_count = session.query(Product).count()
    order_count = session.query(Order).count()
    order_item_count = session.query(OrderItem).count()

    print("\n========== DATABASE SUMMARY ==========")

    print(
        f"Customers   : {customer_count}"
    )

    print(
        f"Products    : {product_count}"
    )

    print(
        f"Orders      : {order_count}"
    )

    print(
        f"Order Items : {order_item_count}"
    )

    print("======================================\n")


# ============================================================
# MAIN
# ============================================================

def main():

    try:

        # ----------------------------------------------------
        # Create tables
        # ----------------------------------------------------

        create_tables()

        # ----------------------------------------------------
        # Create session
        # ----------------------------------------------------

        session = SessionLocal()

        try:

            # ------------------------------------------------
            # Insert sample data
            # ------------------------------------------------

            insert_customers(session)

            insert_products(session)

            insert_orders(session)

            insert_order_items(session)

            # ------------------------------------------------
            # Commit everything
            # ------------------------------------------------

            session.commit()

            print("\nSample data inserted successfully.")

            # ------------------------------------------------
            # Verify
            # ------------------------------------------------

            verify_database(session)

        except Exception as e:

            session.rollback()

            print(
                f"\nError while inserting data: {e}"
            )

            raise

        finally:

            session.close()

    except Exception as e:

        print(
            f"\nDatabase setup failed: {e}"
        )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()