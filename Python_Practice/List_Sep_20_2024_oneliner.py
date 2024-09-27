#Assigment
#Instead of printing the elements one by one, make a new list that has all the elements less than 5 from this list in it and print out this new list.
#Write this in one line of Python.

#=============================================================================



a = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]

#List comprehension [value iteration filter]
print([ elm for elm in a if elm < 5])