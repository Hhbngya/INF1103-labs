import unittest

from supplier import Supplier
from product_factory import ProductFactory
from order import Order


class TestValidation(unittest.TestCase):
    def setUp(self) -> None:
        self.supplier = Supplier("S001", "Test Supplier", "test@example.com")

    def test_zero_price_rejected(self) -> None:
        with self.assertRaises(ValueError):
            ProductFactory.create("physical", "P001", "Pen", 0, 10, self.supplier)

    def test_negative_price_rejected(self) -> None:
        with self.assertRaises(ValueError):
            ProductFactory.create("digital", "D001", "App", -5.00, 10, self.supplier)

    def test_negative_stock_rejected_for_both_types(self) -> None:
        for product_type in ["physical", "digital"]:
            with self.assertRaises(ValueError):
                ProductFactory.create(product_type, "X001", "Item", 10.00, -1, self.supplier)

    def test_update_stock_negative_rejected_and_stock_unchanged(self) -> None:
        product = ProductFactory.create("digital", "D001", "eBook", 18.00, 50, self.supplier)
        with self.assertRaises(ValueError):
            product.update_stock(-5)
        self.assertEqual(product.get_stock(), 50)

    def test_order_quantity_zero_rejected(self) -> None:
        product = ProductFactory.create("physical", "P001", "Lamp", 25.00, 10, self.supplier)
        order = Order("O1")
        with self.assertRaises(ValueError):
            order.add_order_line(product, 0)
        self.assertEqual(len(order.get_order_lines()), 0)


if __name__ == "__main__":
    unittest.main()