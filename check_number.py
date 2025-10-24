"""
In-class Task:

Write a program to check the input number:

If number is an even number, print "A"

But if number is an even number that is not divisible by 3, print "B"
instead, and print "C" instead if yes.

Instead, if z is not an even number, print "D"
"""

# number = 3 -> D
# number = 4 -> B
# number = 12 -> C
# number = 182 -> B
# number = 0 -> C
# number = -7 -> D
# number = -1.5 -> D
# number = 2.2 -> D

number = float(input())

if number % 2 == 0:
    if number % 3 != 0:
        print("B")
    elif number % 3 == 0:
        print("C")
else:
    print("D")