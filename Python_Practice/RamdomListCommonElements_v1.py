import random

RamList1 = random.sample(range(1,20),10)
RamList2 = random.sample(range(1,20),13)
newlist = []
print(f"RamList1 : {RamList1}")
print(f"RamList2 : {RamList2}\n")


for x in RamList1:
    for y in RamList2:
        if x == y:
            newlist.append(x)
print(f"NewList : {newlist}")     
print(f"Final UniqueList :  {list(set(newlist))}")     
