unit = []

if unit:
    print("verified", unit)
else:
    print("unverified", unit)
    
if unit: print("I'm a banana")
elif not unit: print("I'm an apple")

tries = 3
for num in range(tries):
    print(num)

from random import randint   
print(int((randint(0,11)+randint(0,11)+randint(0,11)+randint(0,11))/4) - 5)

word = "Bakerton"
print(len(word))
print(word[2])
print(word[len(word)-1])


if (word[len(word)-1]) == "n" and (word[len(word)-2]) == "o":
    word = word.rstrip("ton")
    print(word)
    
word = "bakerman"
word = word.rstrip("ern")
print(word)
