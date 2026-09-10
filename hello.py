print("========================")
print("Welcome here")
print("My first post!")
print("========================")
#Question 3a: Yes, the program display messages exactly as written.
#             Whatever text that is inside the print("")is ouput.
#Question 3b: Top to bottom. Python executes statements sequentially in the order they appear in the file.
#Question 3c: The output appear in the integrated terminal panel at the bottom of the VS code.

username = "cool_creator"
bio = "Fun Blogger"
followers = 100

print("Username:", username)
print("Bio:", bio)
print("Followers:", followers)

#Question 2a: They're containers holding the data that makes up the profile;
# username and bio hold text (strings), followers holds a number (integer).
# Store them in variables such that if the value changes, I only need to update in one place
#Question 2b: If I change the values, the output will change. 
# Since print("Username:", username)reads whatever username currently holds at the moment the line runs.

followers = 100

followers += 50
print("Day 1:", followers)

followers += 20
print("Day 2:", followers)

followers -= 10
print("Day 3:", followers)

# Question 2a: No, 
# since followers += 50, python reads the current value, 
# adds 50 and stores the result back into follwers, all in one line.
# Question 2b: The existing value, not the original 100. 
# Each line updates the variable in place, 
# so every subsequent operation builds on whatever the varibale holds at the point, not the original value. 
# Question 2c: They are compound assignment operators, combines an srithmetic operation with reassignment in one step.
# x += n means "add n to x and store it back to x";
# x -= n means "subtract n from x and store it back to x"

username = input("Enter Username: ")
age = input("Enter Age: ")
category = input("Enter Content Category: ")

print("\nInstagram Profile")
print("====================")
print("Username:", username)
print("Age:", age)
print("Category:", category)

#Question 2a: When python hits inout("Enter Username: "), it prints the prompt text,
# then pauses the program and waits the terminal for user to key in text.
# Whatever the text is, it will become the return value of that input() call,
# which then gets store into the variables.
#Question 2b: Dynamic. Activity 2, username = "cool_creator" was a fixed value, never change unless change the source
# but now username = input() which means the value comes from whoever runs the program.
#Question 2c: 