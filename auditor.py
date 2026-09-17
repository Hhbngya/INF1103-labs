print("Weekly Lab 2")

#Initialize the inventory to 0
total_inventory = 0
failed_entries = 0

#Continuous Loop until user quits
while True:
    user_entry = input("Enter the stock quantity (or 'quit' to finish): ")
    if user_entry == "quit":
        print("You have quit the program.") 
        break

    elif not user_entry.lstrip('-').isdigit():
        print("WARNING Please enter a number!")
        failed_entries += 1  # increment the counter

    elif int(user_entry) < 0:
        print("ERROR Please enter positive digit!")
        failed_entries += 1
    
    else:
        quantity = int(user_entry)
        total_inventory += quantity
        if total_inventory > 500:
            print("Overstock Alert! Inventory exceeds 500 units")
            break