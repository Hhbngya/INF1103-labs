from supplier import Supplier
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from order import Order
from discount import BulkDiscount, PercentageDiscount
from discount import BulkDiscount, PercentageDiscount, StudentDiscount


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

if __name__ == "__main__":
    demo_strategy()
    demo_extension()