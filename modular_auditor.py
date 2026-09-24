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

# Main program
# Initialize the inventory to 0
total_inventory = 0
failed_entries = 0

# Continuous loop until user quits
while True:
    quantity = get_valid_input()

    if quantity == "quit":
        print("You have quit the program.")
        break

    elif quantity is None:
        failed_entries += 1  # increment the counter

    else:
        total_inventory += quantity

print("Total Units Processed:", total_inventory)
print("Number of Failed/Rejected Entries:", failed_entries)