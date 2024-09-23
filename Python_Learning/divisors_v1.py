num = int(input("Enter a number :" ))
divisors= []
for n in range(1,num+1):
    if num%n == 0:
        divisors.append(n)
print(divisors)        