text = str(input("Enter a word to check PALINDROME : " ))
reverse_text = text[::-1]

if text == reverse_text:
    print("Palindrome")
else:
    print("Its Not")