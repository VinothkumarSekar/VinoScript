text = str(input("Enter a word to check PALINDROME : " ))

n = len(text)
y = 1
z = 0
for x in text:
    if text[n-y] == text[z] :
        y += 1
        z += 1 
        pal = "paal"
    else:
        pal = "npaal"
        break    

if pal == "paal":
    print("\n========================================\n")
    print(f"Entered word '{text}' is Palindrome!!\n")
elif pal == "npaal":
    print("\n========================================\n")
    print(f"Entered word '{text}' is NOT Palindrome!!\n")

        madam