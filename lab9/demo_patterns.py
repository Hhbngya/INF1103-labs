from supplier import Supplier
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from order import Order
from discount import BulkDiscount, PercentageDiscount
from discount import BulkDiscount, PercentageDiscount, StudentDiscount
from product_factory import ProductFactory


def demo_strategy() -> None:
    print("=== Strategy: order discounts ===")
    supplier = Supplier("S001", "TechWorld Pte Ltd", "sales@techworld.com")
    desk = PhysicalProduct("P010", "Desk", 100.00, 10, supplier, 15.0)
    course = DigitalProduct("D010", "Design Course", 50.00, 20, supplier, 500.0)

    order = Order("O200", BulkDiscount(200, 20))
    order.add_order_line(desk, 2)
    order.add_order_line(course, 1)
    print("\nWith BulkDiscount(200, 20):")
    order.display_order()

    order.set_discount(PercentageDiscount(10))
    print("\nAfter set_discount(PercentageDiscount(10)):")
    order.display_order()

def demo_extension() -> None:
    print("\n=== Adding a new strategy without changing Order ===")
    supplier = Supplier("S001", "TechWorld Pte Ltd", "sales@techworld.com")
    ebook = DigitalProduct("D001", "Python eBook", 20.00, 100, supplier, 15.5)

    order = Order("O201", StudentDiscount())
    order.add_order_line(ebook, 5)
    print("\nWith StudentDiscount():")
    order.display_order()

    print("\n--- Two orders sharing one strategy object ---")
    ten_percent = PercentageDiscount(10)
    order_a = Order("O202", ten_percent)
    order_b = Order("O203", ten_percent)
    order_a.add_order_line(ebook, 1)
    order_b.add_order_line(ebook, 3)
    print(f"Order O202 total: ${order_a.calculate_total():.2f}")
    print(f"Order O203 total: ${order_b.calculate_total():.2f}")
    del order_a
    print("After 'del order_a', the shared discount still works for O203:",
          f"${order_b.calculate_total():.2f}")

def demo_factory() -> None:
    print("\n=== Factory: creating products ===")
    supplier = Supplier("S001", "TechWorld Pte Ltd", "sales@techworld.com")

    lamp = ProductFactory.create("physical", "P001", "Desk Lamp", 25.00, 10, supplier, 1.2)
    editor = ProductFactory.create("digital", "D001", "Photo Editor", 49.90, 100, supplier, 1200)
    for product in [lamp, editor]:
        print(f"\nFactory made a {type(product).__name__}:")
        product.display_information()
        print(product.get_fulfilment_info())

    print("\nAsking the factory for an unknown type:")
    try:
        ProductFactory.create("service", "S001", "Installation", 30.00, 5, supplier)
    except ValueError as error:
        print("Caught:", error)

def demo_validation() -> None:
    print("\n=== Validation ===")
    supplier = Supplier("S001", "TechWorld Pte Ltd", "sales@techworld.com")

    try:
        ProductFactory.create("physical", "P020", "Free Pen", 0, 10, supplier, 0.1)
    except ValueError as error:
        print("Price 0 rejected:", error)

    try:
        ProductFactory.create("digital", "D020", "Old Game", 15.00, -3, supplier, 800)
    except ValueError as error:
        print("Negative stock on a DigitalProduct rejected:", error)

    ebook = ProductFactory.create("digital", "D021", "Java eBook", 18.00, 50, supplier, 12)
    try:
        ebook.update_stock(-5)
    except ValueError as error:
        print("update_stock(-5) rejected:", error)
    print("eBook stock is still", ebook.get_stock())

    order = Order("O300")
    try:
        order.add_order_line(ebook, 0)
    except ValueError as error:
        print("Order quantity 0 rejected:", error)
    print("Order lines after the bad add:", len(order.get_order_lines()))

if __name__ == "__main__":
    demo_strategy()
    demo_extension()
    demo_factory()
    demo_validation()