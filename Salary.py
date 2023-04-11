salary = int(input("Enter your salary:"))

service_yrs = int(input("Enter Years of service:"))

if service_yrs > 5:

 print("Yours salary(+Bonus) = ",salary + (salary)*5/100)

else:

  print("You are not eligible for bonus as you have less service years.")