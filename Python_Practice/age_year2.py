from datetime import datetime

dob = input("Enter your DOB year:" )

x = int(input("Age at Target year:" ))

now = datetime.now()

year = now.year
age = int(year) - int(dob)
print(f"Current age: {age}")
print(f"Current year: {year}")

result = (int(x) - year)

if x > year:
    print(f"Hey Buddy.. at year {x} you will be {age+result}!!")
elif x == year:
    print(f"Hey Buddy.. at year {x} your age is {age}!!")
else:
    print(f"Hey Buddy.. at year {x} your were {age+result}!!")    
