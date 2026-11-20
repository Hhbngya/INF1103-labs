from inventory import Inventory
from supplier import Supplier
from product_loader import load_products

supplier = Supplier("S001", "TechWorld Pte Ltd", "sales@techworld.com")
inventory = Inventory()
load_products("products.csv", inventory, supplier)
inventory.display_all_products()