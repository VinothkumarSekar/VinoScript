import random
import sys

usr_inp = int(input('Enter a number (1-9) to Play "Guess the number Game" : '))
rand = random.randint(1,9)

if usr_inp == rand:
    print("\nGuessed the right number!! you rock!!")
elif usr_inp > rand:
    print("\nGuessed too low, Try again!")    
elif usr_inp < rand:
    print("\nGuessed too high, Try again!")

print(f"\nNumber generated by code : {rand}\n")