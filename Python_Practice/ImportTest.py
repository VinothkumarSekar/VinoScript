# import Basic_function 

# #print (Basic_function.dance(2,6))
# for single in range(10):
#     single = single + 1
#     if single / 1 == single and single % single==0:
#          print(single)

# import sympy

# for single in range(5,10):
#     if sympy.isprime(single):
#         print(single)
# #print(sympy.isprime(5)) 

num = 9
# Negative numbers, 0 and 1 are not primes
if num > 1:
  
    # Iterate from 2 to n // 2
    for i in range(2, (num//2)+1):
      
        # If num is divisible by any number between
        # 2 and n / 2, it is not prime
        if (num % i) == 0:
            print(num, "is not a prime number")
            break
    else:
        print(num, "is a prime number")
else:
    print(num, "is not a prime number")