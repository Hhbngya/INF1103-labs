import unittest

from supplier import Supplier
from product_factory import ProductFactory
from order import Order
from discount import DiscountStrategy, PercentageDiscount, BulkDiscount, StudentDiscount


def make_order(discount: DiscountStrategy | None = None) -> Order:
    # 2 x $100 + 1 x $50 = $250 subtotal
    supplier = Supplier("S001", "Test Supplier", "test@example.com")
    desk = ProductFactory.create("physical", "P010", "Desk", 100.00, 10, supplier, 15.0)
    course = ProductFactory.create("digital", "D010", "Course", 50.00, 20, supplier, 500.0)
    order = Order("O1", discount)
    order.add_order_line(desk, 2)
    order.add_order_line(course, 1)
    return order


class TestDiscountStrategies(unittest.TestCase):
    def test_no_discount_is_the_default(self) -> None:
        self.assertAlmostEqual(make_order().calculate_total(), 250.00)

    def test_percentage_discount(self) -> None:
        self.assertAlmostEqual(make_order(PercentageDiscount(10)).calculate_total(), 225.00)

    def test_bulk_discount_over_threshold(self) -> None:
        self.assertAlmostEqual(make_order(BulkDiscount(200, 20)).calculate_total(), 230.00)

    def test_bulk_discount_under_threshold(self) -> None:
        self.assertAlmostEqual(make_order(BulkDiscount(300, 20)).calculate_total(), 250.00)

    def test_new_strategy_works_without_changing_order(self) -> None:
        self.assertAlmostEqual(make_order(StudentDiscount()).calculate_total(), 237.50)

    def test_set_discount_changes_the_strategy(self) -> None:
        order = make_order(BulkDiscount(200, 20))
        self.assertAlmostEqual(order.calculate_total(), 230.00)
        order.set_discount(PercentageDiscount(10))
        self.assertAlmostEqual(order.calculate_total(), 225.00)


if __name__ == "__main__":
    unittest.main()