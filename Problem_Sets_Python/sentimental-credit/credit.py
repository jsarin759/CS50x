while True:
    num = input("Number: ")
    if num.isdigit():
        break

num = str(num)
length = int(len(num))

on_digits = []
off_digits = 0
checksum = 0

for i in range(length):  # 0 - 15, want -1 to -16
    j = (i + 1) * -1
    if j % 2 == 0:
        on_digits.append(int(num[j]) * 2)
    else:
        off_digits += int(num[j])

for digit in on_digits:
    if digit >= 10:
        index = on_digits.index(digit)
        a = digit % 10
        b = int((digit - a) / 10)
        on_digits.remove(digit)
        on_digits.insert(index, b)
        on_digits.insert(index + 1, a)

checksum = sum(on_digits) + off_digits

if checksum % 10 == 0:
    if length in [13, 16] and int(num[0]) == 4:
        print("VISA")
    elif length == 15 and int(num[0:2]) in [34, 37]:
        print("AMEX")
    elif length == 16 and int(num[0:2]) in [51, 52, 53, 54, 55]:
        print("MASTERCARD")
    else:
        print("INVALID")
else:
    print("INVALID")
