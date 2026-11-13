from supplier import Supplier
from physical_product import PhysicalProduct
from digital_product import DigitalProduct


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


if __name__ == "__main__":
    test_association()