import random

RamList1 = random.sample(range(1,20),10)
RamList2 = random.sample(range(1,20),13)

print(f"RamList1 : {RamList1}")
print(f"RamList2 : {RamList2}\n")

print(f"{set(RamList1) & set(RamList2)}")