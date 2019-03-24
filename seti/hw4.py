import math
from fractions import Fraction

#################################################################
# Part 1
# R = 50,000 LY; H = 1,000 LY

radius = 50000
height = 1000
pi = math.pi
Volume = pi * radius * radius * height

print(Volume)

# V = 7.854e+12 Light Years

#################################################################
# Part 2

expo = Fraction('1/3')

# N = 10
N_ONE = 10
Volume_One = Volume / N_ONE
d_one = Volume_One ** expo
print(d_one)

# Neighboring cubes for N=10 has distance d=9226.35 LY

# N = 10,000
N_TWO = 10000
Volume_Two = Volume / N_TWO
d_two = Volume_Two ** expo
print(d_two)

# Neighboring cubes for N=10,000 has distance d=922.635 LY

#################################################################
# Part 3

# 15,000 LY

# N=10
civilizations_one = 15000/d_one
print(civilizations_one)

# For N=10, 1.63 civilizations are necessary to establish contact

# N=10,000
civilizations_two = 15000/d_two
print(civilizations_two)

# For N=10,000, 16.3 civilizations are necessary