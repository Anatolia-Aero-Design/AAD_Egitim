toplam = 0

while True:
    girdi = input("Bir sayı girin (Çıkış için 'q' tuşuna basın): ")

    if girdi == 'q':
        print("Çıkış yapılıyor...")
        break 

    toplam = toplam + int(girdi)
    
print("Girdiğiniz sayıların toplamı:", toplam)