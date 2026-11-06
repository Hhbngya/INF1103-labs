from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct

laptop = PhysicalProduct("P001", "Laptop", 1200.00, 15, 2.5)
desk = PhysicalProduct("P007", "Desk", 150.00, 5, 20)
ebook = DigitalProduct("D001", "Python eBook", 19.90, 100, 15.5)

print("--- Display information (overriding) ---")
laptop.display_information()
ebook.display_information()

print("\n--- Fulfilment info (abstract method) ---")
print("Laptop:", laptop.get_fulfilment_info())
print("eBook:", ebook.get_fulfilment_info())

print("\n--- Shipping cost (interface) ---")
print(f"Laptop (2.5 kg): ${laptop.calculate_shipping_cost():.2f}")
print(f"Desk (20 kg): ${desk.calculate_shipping_cost():.2f}")

print("\n--- Trying to create a plain Product ---")
try:
    item = Product("X001", "Mystery Item", 10.00, 1)
except TypeError as error:
    print("Error:", error)