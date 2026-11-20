# Week 11 Lab - Inventory Management System with design patterns and error handling
import json
import os

from supplier import Supplier
from physical_product import PhysicalProduct
from can_be_shipped import CanBeShipped
from inventory import Inventory
from order import Order
from product_factory import ProductFactory
from discount import (DiscountStrategy, NoDiscount, PercentageDiscount,
                      BulkDiscount, StudentDiscount)
from input_helpers import get_positive_float, get_non_negative_int, get_positive_int

FILENAME = "inventory.json"
LINE = "-" * 45

# The menu picks a strategy object here. Order itself never checks discount types.
DISCOUNTS: dict[str, tuple[str, DiscountStrategy]] = {
    "1": ("No discount", NoDiscount()),
    "2": ("10% off", PercentageDiscount(10)),
    "3": ("$20 off orders of $200 or more", BulkDiscount(200, 20)),
    "4": ("Student discount (5% off)", StudentDiscount()),
}


# ---------- Data Persistence ----------
def find_supplier(suppliers: list[Supplier], supplier_id: str) -> Supplier | None:
    for supplier in suppliers:
        if supplier.get_id() == supplier_id:
            return supplier
    return None


def load_inventory(inventory: Inventory, suppliers: list[Supplier]) -> list[float]:
    if not os.path.exists(FILENAME):
        print("inventory.json not found.")
        print("Starting with an empty inventory.")
        return []

    try:
        with open(FILENAME, "r") as file:
            data = json.load(file)
    except json.JSONDecodeError:
        print("inventory.json is damaged and could not be read.")
        print("Starting with an empty inventory.")
        return []

    for item in data["suppliers"]:
        suppliers.append(Supplier(item["id"], item["name"], item["email"]))

    for item in data["products"]:
        supplier = find_supplier(suppliers, item["supplier_id"])
        if supplier is None:
            print(f"Supplier {item['supplier_id']} not found, skipping {item['id']}.")
            continue
        # weight for physical products, download size for digital ones
        detail = item.get("weight", item.get("download_size", 0.0))
        try:
            product = ProductFactory.create(item["type"], item["id"], item["name"],
                                            item["price"], item["stock"], supplier, detail)
            inventory.add_product(product)
        except ValueError as error:
            print(f"Skipped product {item['id']}: {error}")

    print("inventory.json found.")
    print("Inventory loaded successfully.")
    return data["transactions"]


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
    choice = input("Choose product type: ")
    if choice not in ("1", "2"):
        print("\nInvalid product type.")
        return

    product_id = input("Product ID: ").strip().upper()
    if inventory.find_product(product_id) is not None:
        print("\nProduct ID already exists.")
        return
    name = input("Product Name: ").strip()
    price = get_positive_float("Price: ")
    stock = get_non_negative_int("Stock Quantity: ")

    print("\nSuppliers:")
    for supplier in suppliers:
        supplier.display_information()
    supplier = find_supplier(suppliers, input("Supplier ID: ").strip().upper())
    if supplier is None:
        print("\nSupplier not found.")
        return

    if choice == "1":
        product_type = "physical"
        detail = get_positive_float("Weight (kg): ")
    else:
        product_type = "digital"
        detail = get_positive_float("Download Size (MB): ")

    product = ProductFactory.create(product_type, product_id, name, price,
                                    stock, supplier, detail)
    inventory.add_product(product)
    print("\nProduct added successfully!")


def update_stock(inventory: Inventory, transactions: list[float]) -> None:
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip().upper()
    product = inventory.find_product(product_id)
    if product is None:
        print("\nProduct not found.")
        return

    print("\nProduct Found:")
    print("Name:", product.get_name())
    print("Current Stock:", product.get_stock())

    new_stock = get_non_negative_int("\nNew Stock Quantity: ")
    old_stock = product.get_stock()
    try:
        product.update_stock(new_stock)
    except ValueError as error:
        print(f"\nStock not updated: {error}")
        return

    amount = (new_stock - old_stock) * product.get_price()
    transactions.append(round(amount, 2))
    print("\nStock updated successfully!")


def search_product(inventory: Inventory) -> None:
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip().upper()
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


def choose_discount() -> DiscountStrategy:
    print("\nDiscounts:")
    for key, (label, _) in DISCOUNTS.items():
        print(f"{key}. {label}")
    while True:
        choice = input("Choose discount: ")
        if choice in DISCOUNTS:
            return DISCOUNTS[choice][1]
        print(f"Please choose 1-{len(DISCOUNTS)}.")


def create_order(inventory: Inventory) -> None:
    print("\nCreate Order")
    order = Order(input("Order ID: ").strip().upper(), choose_discount())

    while True:
        product_id = input("\nProduct ID (press Enter to finish): ").strip().upper()
        if product_id == "":
            break
        product = inventory.find_product(product_id)
        if product is None:
            print("Product not found.")
            continue
        quantity = get_positive_int("Quantity: ")
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