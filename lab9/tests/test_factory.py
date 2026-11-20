import unittest

from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from product_factory import ProductFactory


class TestProductFactory(unittest.TestCase):
    def setUp(self) -> None:
        self.supplier = Supplier("S001", "Test Supplier", "test@example.com")

    def test_creates_physical_product(self) -> None:
        product = ProductFactory.create("physical", "P001", "Lamp", 25.00, 10, self.supplier, 1.2)
        self.assertIsInstance(product, PhysicalProduct)
        self.assertIsInstance(product, Product)

    def test_creates_digital_product(self) -> None:
        product = ProductFactory.create("digital", "D001", "Editor", 49.90, 100, self.supplier, 1200)
        self.assertIsInstance(product, DigitalProduct)
        self.assertIsInstance(product, Product)

    def test_unknown_type_raises_value_error(self) -> None:
        with self.assertRaisesRegex(ValueError, "Unknown product type: service"):
            ProductFactory.create("service", "S001", "Installation", 30.00, 5, self.supplier)


if __name__ == "__main__":
    unittest.main()