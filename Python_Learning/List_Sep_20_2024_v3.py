#Ask the user for a number and return a list that contains only elements from the original list a that are smaller than that number given by the user.
a = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]

n = int(input("Enter a number :"  ))
b = []
for elm in a:
    if elm < n:
        b.append(elm)
print(b)        
