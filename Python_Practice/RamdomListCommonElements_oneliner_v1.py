import random

RamList1 = random.sample(range(1,20),10)
RamList2 = random.sample(range(1,20),13)
newlist = []
print(f"RamList1 : {RamList1}")
print(f"RamList2 : {RamList2}\n")

#List comprehension [value iteration filter]

print([x for a in RamList1 for x in RamList1 if x == a])