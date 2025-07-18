from cs50 import get_int

while True:
    n = get_int("Height: ")
    if 0 < n < 9:
        break

for i in range(n):
    c = i + 1
    s = n - c
    print(" " * s, end="")
    print("#" * c, end="")
    print("  ", end="")
    print("#" * c)
