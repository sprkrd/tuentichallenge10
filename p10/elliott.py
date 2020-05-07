from itertools import count


for i in count(1):
    X = 7*i
    if all(X%j == j-1 for j in range(2, 7)):
        print(X)
        break

print(X%2)
print(X%3)
print(X%4)
print(X%5)
print(X%6)
print(X%7)
