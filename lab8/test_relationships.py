from supplier import Supplier
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory
from order import Order
from product import Product

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

def test_composition() -> None:
    print("\n=== Composition: Order and OrderLine ===")
    supplier = Supplier("S001", "TechWorld Pte Ltd", "sales@techworld.com")
    keyboard = PhysicalProduct("P003", "Keyboard", 45.00, 25, supplier, 0.8)
    ebook = DigitalProduct("D001", "Python eBook", 19.90, 100, supplier, 15.5)

    order_1 = Order("O001")
    order_1.add_order_line(keyboard, 2)
    order_1.add_order_line(ebook, 3)
    order_1.display_order()

    order_2 = Order("O002")
    order_2.add_order_line(keyboard, 1)
    order_2.display_order()

    line_1 = order_1.get_order_lines()[0]
    line_2 = order_2.get_order_lines()[0]
    print("\nSame OrderLine object in both orders?", line_1 is line_2)
    print("Same Product object in both order lines?",
          line_1.get_product() is line_2.get_product())
    print("OrderLine ids:", id(line_1), id(line_2))
    print("Product ids:  ", id(line_1.get_product()), id(line_2.get_product()))

    order_1.remove_order_line("D001")
    print("\nOrder O001 after removing the eBook line:")
    order_1.display_order()

    del order_2
    print("\nAfter 'del order_2', its order line is gone, but the keyboard still exists:")
    keyboard.display_information()

def show_product_details(product: Product) -> None:
    product.display_information()
    print(product.get_fulfilment_info())


def test_lsp_and_polymorphism() -> None:
    print("\n=== LSP and Polymorphism ===")
    supplier = Supplier("S001", "TechWorld Pte Ltd", "sales@techworld.com")
    monitor = PhysicalProduct("P004", "Monitor", 299.99, 10, supplier, 5.0)
    licence = DigitalProduct("D002", "Antivirus Licence", 59.00, 50, supplier, 350.0)

    print("\nshow_product_details() with a PhysicalProduct:")
    show_product_details(monitor)
    print("\nshow_product_details() with a DigitalProduct:")
    show_product_details(licence)

    print("\nupdate_stock() keeps the same meaning for both types:")
    monitor.update_stock(8)
    licence.update_stock(45)
    monitor.update_stock(-1)
    licence.update_stock(-1)
    print("Monitor stock:", monitor.get_stock(), "| Licence stock:", licence.get_stock())

    inventory = Inventory()
    inventory.add_product(monitor)
    inventory.add_product(licence)

    print("\nOne loop over the Product collection, no isinstance():")
    for product in inventory.get_products():
        product.display_information()
        print(product.get_fulfilment_info())

    print("\nInventory operations work for both types:")
    inventory.display_all_products()
    found = inventory.find_product("D002")
    if found is not None:
        show_product_details(found)

if __name__ == "__main__":
    test_association()
    test_aggregation()
    test_composition()
    test_lsp_and_polymorphism()