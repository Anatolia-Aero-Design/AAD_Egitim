import math

# 1)Kullanıcıdan aldığınız 3 tane sayıyı çarparak ekrana yazdırın. Ekrana yazdırma işlemini format metoduyla yapmaya çalışın

#k = 3
#sonuc = 1
#
#print(f"{k} adet sayı girin:")
#for i in range(k):
#    sonuc *= float(input(f"Sayı {i+1}: "))
#
#print(f"{k} sayinin çarpimi: {sonuc}")

# 2) Kullanıcıdan ad,soyad ve numara bilgisini alarak bunları alt alta ekrana yazdırın.

#ad, soyad, numara = input("Ad, Soyad, Numara (Boşluklu): ").split()
#print(f"{ad}\n{soyad}\n{numara}")

# 3) Kullanıcıdan bir dik üçgenin dik olan iki kenarını(a,b) alın ve hipotenüs uzunluğunu bulmaya çalışın. Hipotenüs Formülü: a^2 + b^2 = c^2

#karsi = float(input("Karşi kenar: "))
#komsu = float(input("Komşu kenar: "))
#hipotenüs = math.sqrt(karsi**2 + komsu**2)
#print("Hipotenüs: ", hipotenüs)

"""
4) Kullanıcıdan alınan boy ve kilo değerlerine göre beden kitle indeksini hesaplayın ve şu kurallara göre ekrana şu yazıları yazdırın.
#Beden Kitle İndeksi: Kilo / Boy(m) * Boy(m)

#BKİ 18.5'un altındaysa -------> Zayıf

#BKİ 18.5 ile 25 arasındaysa ------> Normal

#BKİ 25 ile 30 arasındaysa --------> Fazla Kilolu

#BKİ 30'un üstündeyse -------------> Obez"""

#bki_list = {
#    18.5: "zayıf",
#    25  : "Normal",
#    30  : "Fazla kilolu",
#    math.inf: "Obez"
#}
#
#boy  = int(input("Boy: "))
#kilo = int(input("Kilo: "))
#bki = kilo / (boy**2)
#
#for i in bki_list.keys():
#    if bki<i:
#        print(f"Bki: {bki} | {bki_list[i]}")
#        break


"""
5) Kullanıcının girdiği vize1,vize2,final notlarına notlarına göre harf notunu hesaplayın.
Vize1 toplam notun %30'una etki edecek.

Vize2 toplam notun %30'una etki edecek.

Final toplam notun %40'ına etki edecek.


Toplam Not >=  90 -----> AA

Toplam Not >=  85 -----> BA

Toplam Not >=  80 -----> BB

Toplam Not >=  75 -----> CB

Toplam Not >=  70 -----> CC

Toplam Not >=  65 -----> DC

Toplam Not >=  60 -----> DD

Toplam Not >=  55 -----> FD

Toplam Not <  55 -----> FF


"""

#vize_list = {
#    55: "FF",
#    60: "FD",
#    65: "DD",
#    70: "DC",
#    75: "CC",
#    80: "CB",
#    85: "BB",
#    90: "BA",
#    math.inf: "AA"
#}
#
#vize1 = int(input("Vize1: "))
#vize2 = int(input("Vize2: "))
#final = int(input("Final: "))
#sayi_not = (vize1 * 30 + vize2 *30 + final*40)/100
#
#for i in vize_list.keys():
#    if sayi_not < i :
#        print(f"not: {sayi_not}, harf nout: {vize_list[i]}")
#        break

"""
6)
1'den 10'kadar olan sayılarla ekrana çarpım tablosu bastırmaya çalışın.
İpucu: İç içe 2 tane for döngüsü kullanın. Aynı zamanda sayıları range() fonksiyonunu kullanarak elde edin.
"""

#text = ""
#for i in range(1,11):
#    for j in range(1,11):
#        text += str(i*j) + "\t"
#    text += "\n"
#
#print(text)


"""
7)
Her bir while döngüsünde kullanıcıdan bir sayı alın ve kullanıcının girdiği sayıları "toplam" isimli bir değişkene ekleyin. Kullanıcı "q" tuşuna bastığı 
zaman döngüyü sonlandırın ve ekrana "toplam değişkenini" bastırın.
İpucu : while döngüsünü sonsuz koşulla başlatın ve kullanıcı q'ya basarsa döngüyü break ile sonlandırın.

"""

#toplam = 0
#while True:
#    command = input("Sayi girin (q çıkış): ")
#    
#    if command == "q":
#        break
#
#    toplam += int(command)


"""
8) 
Kullanıcıdan aldığınız bir sayının mükemmel olup olmadığını bulmaya çalışın.
Bir sayının kendi hariç bölenlerinin toplamı kendine eşitse bu sayıya "mükemmel sayı" denir. Örnek olarak, 6 mükemmel bir sayıdır. (1 + 2 + 3 = 6)
"""

#sayi = float(input("Mükemmel bir sayı girin: "))
#bolenler_toplam = 0
#for i in range(1,int(math.ceil(sayi))):
#    if sayi % i == 0:
#        bolenler_toplam += i
#
#if bolenler_toplam == sayi:
#    print(f"{sayi} bir mükemmel sayi!")
#else:
#    print(f"{sayi} bir mükemmel sayi değil...")



"""
9) 
Kullanıcıdan 2 tane sayı alarak bu sayıların en büyük ortak bölenini (EBOB) dönen bir tane fonksiyon yazın.

"""

#def EBOB(s1, s2):
#    smin = min(s1,s2)
#
#    for i in range(1,smin+1):
#        if s1 % i == 0 and s2 % i == 0:
#            ebob = i
#
#    return ebob
#
#print("EBOB alma fonksiyonu")
#ebob1 = int(input("Sayı 1: "))
#ebob2 = int(input("Sayı 2: "))
#print(f"İki sayının ebobu: {EBOB(ebob1, ebob2)}")

"""
10)
Kullanıcıdan 2 tane sayı alarak bu sayıların en küçük ortak katlarını (EKOK) dönen bir tane fonksiyon yazın.

"""

#def EKOK(s1, s2):
#    return s1*s2/EBOB(s1,s2)
#
#print("EKOK alma fonksiyonu")
#ekok1 = int(input("Sayı 1: "))
#ekok2 = int(input("Sayı 2: "))
#print(f"İki sayının ekoku: {EKOK(ekok1, ekok2)}")

"""
11)

Bu projede ise 4 tane sınıfı oluşturun.
Hayvan Sınıfı ------> Bütün hayvanların ortak özelliklerinin toplandığı sınıf olacak.

Köpek Sınıfı ------> Bu sınıf, hayvan sınıfından miras alan bir sınıf olacak. Ayrıca bu sınıfa köpeklere ait ek özellikler ve metodlar ekleyin.

Kuş Sınıfı ------> Bu sınıf, hayvan sınıfından miras alan bir sınıf olacak. Ayrıca bu sınıfa kuşlara ait ek özellikler ve metodlar ekleyin.

At Sınıfı ------> Bu sınıf, hayvan sınıfından miras alan bir sınıf olacak. Ayrıca bu sınıfa atlara ait ek özellikler ve metodlar ekleyin.

"""

class Hayvan:
    def __init__(self, name):
        self.name = name

class Kopek(Hayvan):
    def __init__(self, name, bark_power):
        super().__init__(name)
        self.bark_power = bark_power

    def bark(self):
        print(f"{self.name} harika bir {self.bark_power}db gücüyle havladı!")

    def sniff(self, object):
        print(f"{self.name} {object} objesini kokluyor...")

class Kus(Hayvan):
    def __init__(self, name, color):
        super().__init__(name)
        self.color = color

    def __str__(self):
        return f"{self.color} renkli {self.name}"

    def fly(self):
        print(f"{self.name} güzel {self.color} tüyleriyle gökyüzünü süslüyor!")

class At(Hayvan):
    def __init__(self, name, speed):
        super().__init__(name)
        self.speed = speed

    def run(self):
        print(f"{self.name} {self.speed}m/s hızıyla tozu dumana katıyor!")


hayvan = Hayvan("hayvan")
karabas = Kopek("Karabaş", 50)
boncuk = Kus("Boncuk", "Pennsylvania Üniversitesi kırmızısı")
boxer = At("Boxer", 9999999999999999999999999999999999999999)

karabas.sniff(boncuk)
boncuk.fly()
boxer.run()