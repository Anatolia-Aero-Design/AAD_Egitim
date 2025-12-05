vize1 = float(input("Vize 1 notunuzu girin : "))
vize2 = float(input("Vize 2 notunuzu girin : "))
final = float(input("Final notunuzu girin : "))


toplam = (vize1 * 0.30) + (vize2 * 0.30) + (final * 0.40)

harfnot = ""
if toplam >= 90:
            harfnot = "AA"
elif toplam >= 85:
            harfnot = "BA"
elif toplam >= 80:
            harfnot = "BB"
elif toplam >= 75:
            harfnot = "CB"
elif toplam >= 70:
            harfnot = "CC"
elif toplam >= 65:
            harfnot = "DC"
elif toplam >= 60:
            harfnot = "DD"
elif toplam >= 55:
            harfnot = "FD"
else:
            harfnot = "FF"

    
print("--- Sonuç ---")
print(f"Dönem Sonu Ortalamanız: {toplam:}")
print(f"Harf Notunuz: {harfnot}")