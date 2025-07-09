"""
# 1)Kullanıcıdan aldığınız 3 tane sayıyı çarparak ekrana yazdırın. Ekrana yazdırma işlemini format metoduyla yapmaya çalışın
"""

sayı1 = int(input("sayı giriniz:"))
sayı2 = int(input("sayı giriniz"))
sayı3 = int(input("sayı giriniz:"))
ekle = sayı1 * sayı2 * sayı3


print(ekle)
# Soru 1 Feedback: Girdi kısmında sorun yok döngü kullanılabilirdi ama bu haliyle de çalışıyor.
# format() metodu kullanılmamış. yazdırma kısmını tekrar gözden geçir.


"""

# 2) Kullanıcıdan ad,soyad ve numara bilgisini alarak bunları alt alta ekrana yazdırın.
"""
isim = input("isim giriniz:")
soyisim = input("soyisminizi giriniz:")
numara = int(input("telefon numaranızı girin;):"))

print(isim + " " + soyisim + " " + str(numara))
# Soru 2 Feedback: Alt alta yazdırma işlemi yapılmamış. tekrar gözden geçir.


"""

# 3) Kullanıcıdan bir dik üçgenin dik olan iki kenarını(a,b) alın ve hipotenüs uzunluğunu bulmaya çalışın. Hipotenüs Formülü: a^2 + b^2 = c^2
"""
from math import sqrt

kenar1 = int(input("yatay kenar uzunluğunu giriniz:"))
kenar2 = int(input("dik kenarınızın uzunluğunu giriniz:"))
hipotenus = sqrt(kenar1**2 + kenar2**2)


print(hipotenus)

"""
4) Kullanıcıdan alınan boy ve kilo değerlerine göre beden kitle indeksini hesaplayın ve şu kurallara göre ekrana şu yazıları yazdırın.
#Beden Kitle İndeksi: Kilo / Boy(m) * Boy(m)

#BKİ 18.5'un altındaysa -------> Zayıf

#BKİ 18.5 ile 25 arasındaysa ------> Normal

#BKİ 25 ile 30 arasındaysa --------> Fazla Kilolu

#BKİ 30'un üstündeyse -------------> Obez
"""

boy = float(input("boyunuz kaç (m):"))
kilo = int(input("kilonuz nedir(kg):"))
bedenkitleindeksi = kilo / ((boy * boy))


print(bedenkitleindeksi)

if bedenkitleindeksi < 18.5:

    print("zayıf")

elif 25 > bedenkitleindeksi > 18.5:

    print("normal")

elif 30 > bedenkitleindeksi > 25:

    print("fazla kilolu")

elif bedenkitleindeksi < 30:

    print("obez")

# Soru 4 Feedback: Beden kitle indeksi hesaplaması doğru ancak son elif hatalı mantığı gözden geçir.

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


vize1 = int(input("birinci vize notu:"))
vize2 = int(input("ikinci vize notu:"))
final = int(input("final notu:"))

x = float(vize1 * 30 / 100) + float(vize2 * 30 / 100) + float(final * 40 / 100)

print(x)

if x >= 90:

    print("x , AA")

elif x >= 85:

    print("x , BA")

elif x >= 80:

    print("x , BB")

elif x >= 75:

    print("x , CB")

elif x >= 70:

    print("x , CC")

elif x >= 65:

    print("x , DC")

elif x >= 60:

    print("x , DD ")

elif x >= 55:

    print("x , FD")

elif x < 55:

    print("x , FF")

# Soru 5 Feedback: Hesaplama doğru ancak harf notu yazdırma kısmında x string olduğundan değeri gözükmüyor
# Örnek çıktı:
# 51.9
# x , FF.
# Tekrar gözden geçir.

# Hesaplama kısmında float() fonksiyonuna gerek yok çünkü zaten bölme işlemi float olarak sonuç verecektir
# Ancak kullandığın değişkenin tipini belli etmek iyi bir yöntemdir.

"""
6)
1'den 10'kadar olan sayılarla ekrana çarpım tablosu bastırmaya çalışın.
İpucu: İç içe 2 tane for döngüsü kullanın. Aynı zamanda sayıları range() fonksiyonunu kullanarak elde edin.
"""

for i in range(1, 11):

    print(i, "ler")

    for k in range(1, 11):

        print(i, "x", k, "=", i * k)


"""
7)
Her bir while döngüsünde kullanıcıdan bir sayı alın ve kullanıcının girdiği sayıları "toplam" isimli bir değişkene ekleyin. Kullanıcı "q" tuşuna bastığı 
zaman döngüyü sonlandırın ve ekrana "toplam değişkenini" bastırın.
İpucu : while döngüsünü sonsuz koşulla başlatın ve kullanıcı q'ya basarsa döngüyü break ile sonlandırın.
"""

toplam = 0
while True:

    girdi = input("sayı giriniz(q: quit):")

    if girdi == "q":

        break

    toplam += int(girdi)

print(toplam)


"""
8) 
Kullanıcıdan aldığınız bir sayının mükemmel olup olmadığını bulmaya çalışın.
Bir sayının kendi hariç bölenlerinin toplamı kendine eşitse bu sayıya "mükemmel sayı" denir. Örnek olarak, 6 mükemmel bir sayıdır. (1 + 2 + 3 = 6)
"""
sayı = int(input("sayı giriniz:"))

toplam = 0

for i in range(1, sayı):
    if sayı % i == 0:
        toplam += i

if toplam == sayı:
    print("sayı mükemmeldir")
else:
    print("sayı mükemmel değil")


"""
9) 
Kullanıcıdan 2 tane sayı alarak bu sayıların en büyük ortak bölenini (EBOB) dönen bir tane fonksiyon yazın.
"""
x = int(input("birinci sayıyı giriniz:"))
y = int(input("ikinci sayıyı giriniz:"))

ebob = 1

for i in range(2, x + 1):
    if x % i == 0 and y % i == 0:
        ebob = i

print("birinci sayı:", x)
print("ikinci sayı:", y)
print(ebob)

"""
10)
Kullanıcıdan 2 tane sayı alarak bu sayıların en küçük ortak katlarını (EKOK) dönen bir tane fonksiyon yazın.
"""
a = int(input("birinci sayıyı giriniz:"))
b = int(input("ikinci sayıyı giriniz:"))
ebob = 1

for i in range(2, a + 1):
    if a % i == 0 and b % i == 0:
        ebob = i

print("birinci sayı:", a)
print("ikinci sayı:", b)

ekok = int((a * b) / (ebob))
print(ekok)


"""
11)

Bu projede ise 4 tane sınıfı oluşturun.
Hayvan Sınıfı ------> Bütün hayvanların ortak özelliklerinin toplandığı sınıf olacak.

Köpek Sınıfı ------> Bu sınıf, hayvan sınıfından miras alan bir sınıf olacak. Ayrıca bu sınıfa köpeklere ait ek özellikler ve metodlar ekleyin.

Kuş Sınıfı ------> Bu sınıf, hayvan sınıfından miras alan bir sınıf olacak. Ayrıca bu sınıfa kuşlara ait ek özellikler ve metodlar ekleyin.

At Sınıfı ------> Bu sınıf, hayvan sınıfından miras alan bir sınıf olacak. Ayrıca bu sınıfa atlara ait ek özellikler ve metodlar ekleyin.

"""


class animal:
    def __init__(self, type, quality, food):
        self.type = type.title()
        self.quality = quality
        self.food = food


animal1 = animal("köpek", "iyi koku alır", "etçildir")
animal2 = animal("kuş", "uçabilir", "hepçildir")
animal3 = animal("at", "yelelidir", "otçuldur")


print(animal1.type, animal1.quality, animal1.food)
print(animal2.type, animal2.quality, animal2.food)
print(animal3.type, animal3.quality, animal3.food)

# Soru 11 Feedback: Yalnızca hayvan sınıfı oluşturulmuş. Diğer sınıflar oluşturulmamış.
# Nesneye dayalı programlama ile ilgili miras alma (inheritance) ve nesne oluşturma (instantiation) konularını gözden geçir.


# Son değerlendirme:# 1. Soru: Format metodu kullanılmamış.
# 2. Soru: Alt alta yazdırma işlemi yapılmamış.
# 3. Soru: Doğru.
# 4. Soru: Beden kitle indeksi hesaplaması doğru ancak son elif hatalı mantığı gözden geçir.
# 5. Soru: Hesaplama doğru ancak harf notu yazdırma kısmında x string olduğundan değeri gözükmüyor.
# 6. Soru: Doğru.
# 7. Soru: Doğru.
# 8. Soru: Doğru.
# 9. Soru: Doğru.
# 10. Soru: Doğru.
# 11. Soru: Yalnızca hayvan sınıfı oluşturulmuş. Diğer sınıflar oluşturulmamış.

# Kullanıcıdan input aldığın soruları tekrardan hata ayıklama yaparak gözden geçir.
# Örneğin sayı girdisi istenen bir senaryoda kullanıcı harf girdiğinde program hata verecektir.
# Bu tür durumları kontrol etmek için try-except bloklarını kullanabilirsin.
