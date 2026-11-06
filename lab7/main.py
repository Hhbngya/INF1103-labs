# Week 8 Lab - Inventory Management System using OOP
import json
import os

from product import Product
from inventory import Inventory

FILENAME = "inventory.json"
LINE = "-" * 45


# ---------- Data Persistence ----------
def load_inventory(inventory):
    # Turn each product dictionary from the file into a Product object.
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as file:
            data = json.load(file)
        for item in data["products"]:
            product = Product(item["id"], item["name"], item["price"], item["stock"])
            inventory.add_product(product)
        print("inventory.json found.")
        print("Inventory loaded successfully.")
        return data["transactions"]
    print("inventory.json not found.")
    print("Starting with an empty inventory.")
    return []


def save_inventory(inventory, transactions):
    # Turn each Product object back into a dictionary so it can be saved.
    products = []
    for product in inventory.get_products():
        products.append({
            "id": product.get_id(),
            "name": product.get_name(),
            "price": product.get_price(),
            "stock": product.get_stock()
        })
    data = {"products": products, "transactions": transactions}
    with open(FILENAME, "w") as file:
        json.dump(data, file, indent=4)


# ---------- Menu Actions ----------
def add_product(inventory):
    print("\nAdd New Product")
    product_id = input("Product ID: ").upper()
    if inventory.search_product(product_id) is not None:
        print("\nProduct ID already exists.")
        return
    name = input("Product Name: ")
    price = float(input("Price: "))
    stock = int(input("Stock Quantity: "))

    product = Product(product_id, name, price, stock)
    inventory.add_product(product)
    print("\nProduct added successfully!")


def update_stock(inventory, transactions):
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").upper()
    product = inventory.search_product(product_id)
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


def search_product(inventory):
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").upper()
    product = inventory.search_product(product_id)
    if product is None:
        print("\nProduct not found.")
    else:
        print("\nProduct Found")
        print(LINE)
        print("ID:", product.get_id())
        print("Name:", product.get_name())
        print(f"Price: ${product.get_price():.2f}")
        print("Stock:", product.get_stock())
        print(LINE)


# ---------- Menu System ----------
def main():
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)
    print()

    inventory = Inventory()
    transactions = load_inventory(inventory)

    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("-" * 28)

    while True:
        choice = input("\nEnter option: ")

        if choice == "1":
            inventory.display_all()
        elif choice == "2":
            add_product(inventory)
        elif choice == "3":
            update_stock(inventory, transactions)
        elif choice == "4":
            search_product(inventory)
        elif choice == "5":
            print("\nSaving inventory...")
            save_inventory(inventory, transactions)
            print("Inventory saved successfully to inventory.json.")
        elif choice == "6":
            print("\nSaving inventory before exit...")
            save_inventory(inventory, transactions)
            print("Inventory saved successfully.")
            print("\nThank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("\nInvalid option. Please enter 1-6.")


if __name__ == "__main__":
    main()