# Function 1: Ask for product name and quantity, check them
def get_valid_input():
    global failed_entries
    product_name = input("Enter Product Name: ")

    if product_name == 'quit':
        return 'quit'

    elif product_name.lstrip('-').isdigit():
        print("error...Product name cannot be a number.")
        return None
    while True:
        quantity = input("Enter Quantity: ")

        if quantity == "quit":
            return "quit"
        
        elif not quantity.isdigit():
            print("error...Please enter positive digit!")
            failed_entries += 1

        else:
            return product_name, int(quantity)

# Function 2: read total, products and history from orders.txt
def load_inventory():
    total = 0
    products = []
    history = []

    try:
        with open('orders.txt', 'r') as file:
            lines = file.readlines()
            total = int(lines[0])
            for line in lines[1:]:
                name, amount = line.strip().split(',')
                products.append(name)
                history.append(int(amount))
    except FileNotFoundError:
        pass    # no file yet, start with empty orders

    return total, products, history

# Function 4: Show every order numbered from 1001
def show_orders(products, history):
    for i in range(len(history)):
        order_number = 1001 + i
        print(str(order_number) + ", " + products[i] + ", " + str(history[i]))

# Main program, load saved data
total_inventory, products, history = load_inventory()
failed_entries = 0

print("Current Orders:")
print()
show_orders(products, history)
print()

# Continuous loop until user quits
while True:
    result = get_valid_input()

    if result == "quit":
        print("You have quit the program.")
        break

    elif result is None:
        failed_entries += 1
    else:
        product_name, quantity = result
        products.append(product_name)
        history.append(quantity)
        total_inventory = total_inventory + quantity
        order_number = 1000 + len(history)
        print()
        print("New Order Added:")
        print(str(order_number) + "," + product_name + "," + str(quantity))
        print()

print("\nFinal Total:", total_inventory)
print("Transaction History:", history)
print("Failed Entries:", failed_entries)