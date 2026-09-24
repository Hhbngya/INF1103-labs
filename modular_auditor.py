print("Weekly Lab 3")

# Function 1: Ask for input, check it, and return a number or "quit"
def get_valid_input():
    user_entry = input("Enter the stock quantity (or 'quit' to finish): ")

    if user_entry == "quit":
        return "quit"

    elif not user_entry.lstrip('-').isdigit():
        print("WARNING Please enter a number!")
        return None

    elif int(user_entry) < 0:
        print("ERROR Please enter positive digit!")
        return None

    else:
        return int(user_entry)
    
# Function 2: Add the new delivery to the total and return the new total
def process_delivery(current_total, new_value):
    new_total = current_total + new_value
    return new_total

# Function 3: Work out the 10% tax on one delivery
def calculate_tax(amount):
    tax = round(amount *0.10, 2)
    return tax

# Function 4: Print the final summary
def generate_report(total_units, failed_attempts):
    print("Total Deliveries Processed:", total_units)
    print("Number of Failed/Rejected Entries:", failed_attempts)

# Main program
# Initialize the inventory to 0
total_inventory = 0
failed_entries = 0
delivery_count = 0

# Continuous loop until user quits
while True:
    quantity = get_valid_input()

    if quantity == "quit":
        print("You have quit the program.")
        break

    elif quantity is None:
        failed_entries += 1  # increment the counter

    else:
        total_inventory = process_delivery(total_inventory, quantity)
        tax = calculate_tax(quantity)
        delivery_count += 1
        print("Delivery", delivery_count, "- Quantity:", quantity, "| Tax:", tax)

generate_report(total_inventory, failed_entries)