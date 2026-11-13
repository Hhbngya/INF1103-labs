# Week 10 Lab - Inventory Management System with object relationships
import json
import os

from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from can_be_shipped import CanBeShipped
from inventory import Inventory
from order import Order

FILENAME = "inventory.json"
LINE = "-" * 45


# ---------- Data Persistence ----------
def find_supplier(suppliers: list[Supplier], supplier_id: str) -> Supplier | None:
    for supplier in suppliers:
        if supplier.get_id() == supplier_id:
            return supplier
    return None


def load_inventory(inventory: Inventory, suppliers: list[Supplier]) -> list[float]:
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as file:
            data = json.load(file)

        # Suppliers are created first, on their own, then linked to products
        for item in data["suppliers"]:
            suppliers.append(Supplier(item["id"], item["name"], item["email"]))

        for item in data["products"]:
            supplier = find_supplier(suppliers, item["supplier_id"])
            if supplier is None:
                print(f"Supplier {item['supplier_id']} not found, skipping {item['id']}.")
                continue
            if item["type"] == "physical":
                product = PhysicalProduct(item["id"], item["name"], item["price"],
                                          item["stock"], supplier, item["weight"])
            else:
                product = DigitalProduct(item["id"], item["name"], item["price"],
                                         item["stock"], supplier, item["download_size"])
            inventory.add_product(product)

        print("inventory.json found.")
        print("Inventory loaded successfully.")
        return data["transactions"]

    print("inventory.json not found.")
    print("Starting with an empty inventory.")
    return []


def save_inventory(inventory: Inventory, suppliers: list[Supplier],
                   transactions: list[float]) -> None:
    supplier_data = []
    for supplier in suppliers:
        supplier_data.append({
            "id": supplier.get_id(),
            "name": supplier.get_name(),
            "email": supplier.get_contact_email()
        })

    products = []
    for product in inventory.get_products():
        item = {
            "id": product.get_id(),
            "name": product.get_name(),
            "price": product.get_price(),
            "stock": product.get_stock(),
            "supplier_id": product.get_supplier().get_id()
        }
        if isinstance(product, PhysicalProduct):
            item["type"] = "physical"
            item["weight"] = product.get_weight()
        else:
            item["type"] = "digital"
            item["download_size"] = product.get_download_size()
        products.append(item)

    data = {"suppliers": supplier_data, "products": products,
            "transactions": transactions}
    with open(FILENAME, "w") as file:
        json.dump(data, file, indent=4)


# ---------- Menu Actions ----------
def add_product(inventory: Inventory, suppliers: list[Supplier]) -> None:
    print("\nAdd New Product")
    print("1. Physical Product")
    print("2. Digital Product")
    product_type = input("Choose product type: ")
    if product_type not in ("1", "2"):
        print("\nInvalid product type.")
        return

    product_id = input("Product ID: ").upper()
    if inventory.find_product(product_id) is not None:
        print("\nProduct ID already exists.")
        return
    name = input("Product Name: ")
    price = float(input("Price: "))
    stock = int(input("Stock Quantity: "))

    print("\nSuppliers:")
    for supplier in suppliers:
        supplier.display_information()
    supplier = find_supplier(suppliers, input("Supplier ID: ").upper())
    if supplier is None:
        print("\nSupplier not found.")
        return

    product: Product
    if product_type == "1":
        weight = float(input("Weight (kg): "))
        product = PhysicalProduct(product_id, name, price, stock, supplier, weight)
    else:
        download_size = float(input("Download Size (MB): "))
        product = DigitalProduct(product_id, name, price, stock, supplier, download_size)

    inventory.add_product(product)
    print("\nProduct added successfully!")


def update_stock(inventory: Inventory, transactions: list[float]) -> None:
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").upper()
    product = inventory.find_product(product_id)
    if product is None:
        print("\nProduct not found.")
        return

    print("\nProduct Found:")
    print("Name:", product.get_name())
    print("Current Stock:", product.get_stock())

    new_stock = int(input("\nNew Stock Quantity: "))
    old_stock = product.get_stock()
    product.update_stock(new_stock)

    # only record the transaction if the Product accepted the new stock
    if product.get_stock() == new_stock:
        amount = (new_stock - old_stock) * product.get_price()
        transactions.append(round(amount, 2))
        print("\nStock updated successfully!")


def search_product(inventory: Inventory) -> None:
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").upper()
    product = inventory.find_product(product_id)
    if product is None:
        print("\nProduct not found.")
    else:
        print("\nProduct Found")
        print(LINE)
        product.display_information()
        product.get_supplier().display_information()
        print("Fulfilment:", product.get_fulfilment_info())
        # only products that signed the CanBeShipped contract have a shipping cost
        if isinstance(product, CanBeShipped):
            print(f"Shipping Cost: ${product.calculate_shipping_cost():.2f}")
        print(LINE)


def create_order(inventory: Inventory) -> None:
    print("\nCreate Order")
    order = Order(input("Order ID: ").upper())

    while True:
        product_id = input("\nProduct ID (press Enter to finish): ").upper()
        if product_id == "":
            break
        product = inventory.find_product(product_id)
        if product is None:
            print("Product not found.")
            continue
        quantity = int(input("Quantity: "))
        order.add_order_line(product, quantity)
        print("Added to order.")

    order.display_order()


# ---------- Menu System ----------
def main() -> None:
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)
    print()

    inventory = Inventory()
    suppliers: list[Supplier] = []
    transactions = load_inventory(inventory, suppliers)

    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Create Order")
    print("7. Exit")
    print("-" * 28)

    while True:
        choice = input("\nEnter option: ")

        if choice == "1":
            inventory.display_all_products()
        elif choice == "2":
            add_product(inventory, suppliers)
        elif choice == "3":
            update_stock(inventory, transactions)
        elif choice == "4":
            search_product(inventory)
        elif choice == "5":
            print("\nSaving inventory...")
            save_inventory(inventory, suppliers, transactions)
            print("Inventory saved successfully to inventory.json.")
        elif choice == "6":
            create_order(inventory)
        elif choice == "7":
            print("\nSaving inventory before exit...")
            save_inventory(inventory, suppliers, transactions)
            print("Inventory saved successfully.")
            print("\nThank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("\nInvalid option. Please enter 1-7.")


if __name__ == "__main__":
    main()