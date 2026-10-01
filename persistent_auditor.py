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

print("Current Orders:")
print()
show_orders(products, history)
print()
print("Total:", total_inventory)