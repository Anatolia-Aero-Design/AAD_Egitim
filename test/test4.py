print("BKİ Hesaplama Programı")

agirlik = float(input("Ağırlığınızı yazınız (Kilogram)"))
boy = float(input("Boyunuzu yazınız (Metre)"))

bki = agirlik / ( boy * boy)

if bki < 18.5:
    hal = "Zayıf"
elif bki <= 24.9:  
    hal = "Normal"
elif bki <= 29.9:
    hal = "Fazla Kilolu"
else:
    hal = "Obez"

print("Sonuç : " , bki , hal )