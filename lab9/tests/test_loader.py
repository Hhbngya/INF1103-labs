import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout

from supplier import Supplier
from inventory import Inventory
from product_loader import load_products

CSV_TEXT = """product_type,product_id,name,price,stock_quantity
physical,P001,Desk Lamp,25.00,10
digital,D001,Photo Editor,49.90,100
service,S001,Installation,30.00,5
physical,P002,Office Chair,abc,3
physical,P003,Monitor Stand,39.50,7
"""


class TestLoadProducts(unittest.TestCase):
    def setUp(self) -> None:
        self.supplier = Supplier("S001", "Test Supplier", "test@example.com")
        self.inventory = Inventory()

    def test_bad_rows_skipped_and_valid_rows_loaded(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "products.csv")
            with open(path, "w", newline="") as file:
                file.write(CSV_TEXT)
            output = io.StringIO()
            with redirect_stdout(output):
                load_products(path, self.inventory, self.supplier)

        ids = [product.get_id() for product in self.inventory.get_products()]
        self.assertEqual(ids, ["P001", "D001", "P003"])
        self.assertIn("Skipped row", output.getvalue())
        self.assertIn("3 products loaded.", output.getvalue())

    def test_missing_file_handled_gracefully(self) -> None:
        output = io.StringIO()
        with redirect_stdout(output):
            load_products("no_such_file.csv", self.inventory, self.supplier)
        self.assertEqual(len(self.inventory.get_products()), 0)
        self.assertIn("Products file not found", output.getvalue())
        self.assertIn("Load attempt finished.", output.getvalue())


if __name__ == "__main__":
    unittest.main()