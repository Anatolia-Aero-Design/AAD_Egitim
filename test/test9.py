# EBOB
sayi1 = int(input("1. sayıyı giriniz:"))
sayi2 = int(input("2. sayıyı giriniz"))

ebob = 1
i = 1

while i <= sayi1 and i <= sayi2:
    if sayi1 % i == 0 and sayi2 % i == 0:
        ebob = i
    i+= 1

print("Girdiğiniz iki sayının EBOB'u = ", ebob)
