class Temprature():
    def degrees(self):
        return(temp)
class Celsius_and_Fahrenheit(Temprature):
    def change_to_Fahrenheit(self):
        return((celsius * 1.8) + 32)

    def change_to_Celsius(self):
        return((fahrenheit - 32)/1.8)
celsius=float(input("Enter celsius:"))
fahrenheit=float(input("Enter fahrenheit:"))
temp=("changing Temprature")
obj=Celsius_and_Fahrenheit
c=obj.degrees
a=obj.change_to_Fahrenheit(celsius)
b=obj.change_to_Celsius(fahrenheit)
print(temp)
print("change Celsius to fahrenheit",a)
print("change fahrenheit to Celsius",b)