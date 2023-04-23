# import math module
from math import pi

# take input from user
r = float(input ("Input the radius of the circle : "))

# compute the area from radius of a circle given by user
calculateArea = str(pi * r**2);

#print result
print ("The area of the circle with radius " + str(r) + " is: " + calculateArea)

r = float(input("The circumference of the circle : "))

calculateCircumference = str (2 * pi * r);

print("The circumference of the circle with circumference "+ str(r) + " is: " + calculateCircumference)
