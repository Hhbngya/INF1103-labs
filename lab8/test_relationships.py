from supplier import Supplier
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory

def test_association() -> None:
    print("=== Association: Supplier and Product ===")
    supplier = Supplier("S001", "TechWorld Pte Ltd", "sales@techworld.com")
    laptop = PhysicalProduct("P001", "Laptop", 1200.00, 15, supplier, 2.5)
    ebook = DigitalProduct("D001", "Python eBook", 19.90, 100, supplier, 15.5)

    print("\nSupplier accessed through each product:")
    laptop.get_supplier().display_information()
    ebook.get_supplier().display_information()

    print("\nBoth products share the same Supplier object?",
          laptop.get_supplier() is ebook.get_supplier())

    del supplier
    print("\nAfter 'del supplier':")
    laptop.get_supplier().display_information()
    ebook.get_supplier().display_information()

    del laptop
    print("\nAfter 'del laptop', the supplier still exists through the eBook:")
    ebook.get_supplier().display_information()
    
def test_aggregation() -> None:
    print("\n=== Aggregation: Inventory and Product ===")
    supplier = Supplier("S002", "Gadget Hub", "orders@gadgethub.com")
    mouse = PhysicalProduct("P002", "Mouse", 25.50, 45, supplier, 0.2)
    print("\nProduct created before any Inventory exists:")
    mouse.display_information()

    inventory_a = Inventory()
    inventory_b = Inventory()

    inventory_a.add_product(mouse)
    print("\nInventory A after adding the mouse:")
    inventory_a.display_all_products()

    removed = inventory_a.remove_product("P002")
    print("\nInventory A after removing the mouse:")
    inventory_a.display_all_products()

    print("\nThe removed mouse still works:")
    print("Removed object is the same Product?", removed is mouse)
    mouse.update_stock(40)
    mouse.display_information()

    inventory_b.add_product(mouse)
    print("\nThe same mouse added to Inventory B:")
    inventory_b.display_all_products()

if __name__ == "__main__":
    test_association()
    test_aggregation()