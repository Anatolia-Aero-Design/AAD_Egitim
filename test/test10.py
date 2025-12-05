# EKOK
sayi1 = int(input("1. sayıyı giriniz:"))
sayi2 = int(input("2. sayıyı giriniz"))


buyuk_sayi = max(sayi1, sayi2)
while True:
    if buyuk_sayi % sayi1 == 0 and buyuk_sayi % sayi2 == 0:
        ekok = buyuk_sayi
        break
    buyuk_sayi += 1
print("Girdiğiniz iki sayının ekok'u :", ekok)