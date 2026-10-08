# Week 5 Lab - Stage 1: dictionaries and functions
LINE = "-" * 45


# ---------- Data Manipulation ----------
def display_all(data):
    print("\nCurrent Inventory")
    print(LINE)
    if len(data["products"]) == 0:
        print("Inventory is empty.")
    for product in data["products"]:
        print(f"ID: {product['id']} | Name: {product['name']} | "
              f"Price: ${product['price']:.2f} | Stock: {product['stock']}")
    print(LINE)


def add_product(data):
    print("\nAdd New Product")
    product_id = input("Product ID: ").upper()
    if search_product(data, product_id) is not None:
        print("\nProduct ID already exists.")
        return
    name = input("Product Name: ")
    price = float(input("Price: "))
    stock = int(input("Stock Quantity: "))

    product = {"id": product_id, "name": name, "price": price, "stock": stock}
    data["products"].append(product)
    print("\nProduct added successfully!")


def update_stock(data):
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").upper()
    product = search_product(data, product_id)
    if product is None:
        print("\nProduct not found.")
        return

    print("\nProduct Found:")
    print("Name:", product["name"])
    print("Current Stock:", product["stock"])

    new_stock = int(input("\nNew Stock Quantity: "))
    amount = (new_stock - product["stock"]) * product["price"]
    data["transactions"].append(round(amount, 2))
    product["stock"] = new_stock
    print("\nStock updated successfully!")


def search_product(data, product_id):
    for product in data["products"]:
        if product["id"] == product_id:
            return product
    return None


# ---------- Menu System ----------
def main():
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)

    # products stored as dictionaries inside a list
    data = {
        "products": [
            {"id": "P001", "name": "Laptop", "price": 1200.0, "stock": 15},
            {"id": "P002", "name": "Mouse", "price": 25.5, "stock": 40},
            {"id": "P003", "name": "Keyboard", "price": 45.0, "stock": 25},
        ],
        "transactions": [],
    }

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
            display_all(data)
        elif choice == "2":
            add_product(data)
        elif choice == "3":
            update_stock(data)
        elif choice == "4":
            print("\nSearch Product")
            product_id = input("Enter Product ID: ").upper()
            product = search_product(data, product_id)
            if product is None:
                print("\nProduct not found.")
            else:
                print("\nProduct Found")
                print(LINE)
                print("ID:", product["id"])
                print("Name:", product["name"])
                print(f"Price: ${product['price']:.2f}")
                print("Stock:", product["stock"])
                print(LINE)
        elif choice == "5":
            print("\nSave is not available yet.")
        elif choice == "6":
            print("\nThank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("\nInvalid option. Please enter 1-6.")


if __name__ == "__main__":
    main()