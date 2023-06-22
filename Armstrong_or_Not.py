num = int(input("Please give a number: "))
sum = 0 
temp = num

count = len(str(num)) 

while temp > 0:
    digit = temp % 10
    sum += digit ** count
    temp //= 10 

if num == sum:
    print("Given ",num, "is an Armstrong number")
else:
    print("Given ",num, "is not an Armstrong number")