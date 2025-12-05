sayi = int(input("Bir sayı girin: "))

toplam = 0

for a in range(1, sayi):
    
    if sayi % a == 0:
        toplam += a 

if toplam == sayi:
    print(f"{sayi} Mükemmel bir sayıdır!")
else:
    print(f"{sayi} Mükemmel bir sayı değildir.")