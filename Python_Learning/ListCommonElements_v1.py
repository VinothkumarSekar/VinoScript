a = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 13, 5, 2, 3, 5]
b = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 5, 13, 9]
c = []

for elm in a:
    for x in b: 
        if elm == x:
            #print (f"elm: {elm} , x: {x}")
            c.append(x)
            #print (f"c: {c}")

print(f"Final result : {list(set(c))}")     

        