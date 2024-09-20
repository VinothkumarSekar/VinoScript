from datetime import datetime

age = input("Enter your age:" )

x = input("Your age at year:" )

print(f"Current age: {age}")



now = datetime.now()

year = now.year

print(f"Current year: {year}")

#result = (int(x) - int(age) ) + year
#result = (int(x) - year) + int(age)

print(f"Hey Buddy.. at year {result} you will be {x}!!")