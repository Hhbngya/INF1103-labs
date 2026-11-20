from supplier import Supplier
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from order import Order
from discount import BulkDiscount, PercentageDiscount


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


if __name__ == "__main__":
    demo_strategy()