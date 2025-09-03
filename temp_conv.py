unit = input("is this temperature in Celcius or Fahrenhite (C/F): "  )
temp = float(input("enter the temperature: "))

if unit== "C":
    temp = round((9 * temp) / 5 + 32, 1)
    print(f"the temperature in Fanrenhite is:{temp} °F")

elif unit== "F":
    temp = round((temp -32) * 5 / 9, 1)
    print(f"the temperature in Cellcius is:{temp} °C")
else:
    print(f"{unit}is not valid for measurement" )