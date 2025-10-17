# 1)Kullanıcıdan aldığınız 3 tane sayıyı çarparak ekrana yazdırın. Ekrana yazdırma işlemini format metoduyla yapmaya çalışın

# İstenilen tipte veri almak için yeni input fonk
def get_input(text, input_type=str):
    while True:
        the_input = input(text)
        if input_type == int:
            try:
                return int(the_input)
            except:print("Sizden tam sayı istendi.")
        elif input_type == str and the_input.isalpha():
            return str(the_input)
        elif input_type == float:
            try:
                return float(the_input)
            except:print("Sizden virgüllü sayı istendi.")

# Kök alma fonk
def sqrt(kök):
    return kök**(1/2)

#Faktorize fonk
def primes_sieve(limit):
    limitn = limit+1
    primes = dict()
    for i in range(2, limitn): primes[i] = True

    for i in primes:
        factors = range(i,limitn, i)
        for f in factors[1:]:
            primes[f] = False
    return [i for i in primes if primes[i]==True]


def test_1():
    sayi1 = get_input("Sayı 1: ", int)
    sayi2 = get_input("Sayı 2: ", int)
    sayi3 = get_input("Sayı 3: ", int)

    print("Çarpımları:",sayi1*sayi2*sayi3)

# 2) Kullanıcıdan ad,soyad ve numara bilgisini alarak bunları alt alta ekrana yazdırın.

def test_2():
    isim = get_input("İsminiz: ", str)
    soyad = get_input("Soyadanız: ", str)
    numara = get_input("Numarınız: ", int)

    print("İsim: ", isim, "\nSoyad: ", soyad, "\nNumara: ", numara)

# 3) Kullanıcıdan bir dik üçgenin dik olan iki kenarını(a,b) alın ve hipotenüs uzunluğunu bulmaya çalışın. Hipotenüs Formülü: a^2 + b^2 = c^2

def test_3():
    kenar1 = get_input("Üçgenin ilk kenarı: ", int)
    kenar2 = get_input("Üçgenin diğer kenarı: ", int)

    print("Hipotenüs: ", sqrt(kenar1**2 + kenar2**2))

"""
4) Kullanıcıdan alınan boy ve kilo değerlerine göre beden kitle indeksini hesaplayın ve şu kurallara göre ekrana şu yazıları yazdırın.
#Beden Kitle İndeksi: Kilo / Boy(m) * Boy(m)

#BKİ 18.5'un altındaysa -------> Zayıf

#BKİ 18.5 ile 25 arasındaysa ------> Normal

#BKİ 25 ile 30 arasındaysa --------> Fazla Kilolu

#BKİ 30'un üstündeyse -------------> Obez"""

def test_4():
    boy = get_input("Metre cinsiden boyunuz: ", float)
    kilo = get_input("Kilogram cinsinden kilonuz: ", float)
    BKİ = kilo/boy**2

    print("BKİ: ", BKİ)
    if BKİ < 18.5:
        print("Zayıf")
    elif 18.5 <= BKİ < 25:
        print("Normal")
    elif 25 <= BKİ < 30:
        print("Fazla Kilolu")
    else:
        print("Obez")

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

Toplam Not <  55 -----> FF"""

def test_5():
    vize1 = get_input("İlk vize notunuz: ", int)
    vize2 = get_input("Diğer vize notunuz: ", int)
    final = get_input("Final notunuz: ", int)
    toplam_not = int((vize1*0.3 + vize2*0.3 + final*0.4)/5)

    match toplam_not:
        case 20 | 19 | 18:
            print("AA")
        case 17:
            print("BA")
        case 16:
            print("BB")
        case 15:
            print("CB")
        case 14:
            print("CC")
        case 13:
            print("DC")
        case 12:
            print("DD")
        case 11:
            print("FD")
        case _:
            print("FF")
    
"""
6)
1'den 10'kadar olan sayılarla ekrana çarpım tablosu bastırmaya çalışın.
İpucu: İç içe 2 tane for döngüsü kullanın. Aynı zamanda sayıları range() fonksiyonunu kullanarak elde edin.
"""
def test_6():
    for bir in range(1, 11):
        for iki in range(1,11):
            print(bir, " x ", iki, " = ", bir*iki)

"""
7)
Her bir while döngüsünde kullanıcıdan bir sayı alın ve kullanıcının girdiği sayıları "toplam" isimli bir değişkene ekleyin. Kullanıcı "q" tuşuna bastığı 
zaman döngüyü sonlandırın ve ekrana "toplam değişkenini" bastırın.
İpucu : while döngüsünü sonsuz koşulla başlatın ve kullanıcı q'ya basarsa döngüyü break ile sonlandırın."""

def test_7():
    toplam_7 = 0
    while True:
        girdi = input("Sayı giriniz (q ile çıkın): ")
        if girdi == "q" or girdi == "Q":
            break
        else:
            toplam_7 += int(girdi)
    print("Sonuç: ", toplam_7)

"""
8) 
Kullanıcıdan aldığınız bir sayının mükemmel olup olmadığını bulmaya çalışın.
Bir sayının kendi hariç bölenlerinin toplamı kendine eşitse bu sayıya "mükemmel sayı" denir. Örnek olarak, 6 mükemmel bir sayıdır. (1 + 2 + 3 = 6)
"""
def test_8():
    sayı_8 = get_input("Mükemmel mi diye kontrol edilecek sayı: ",int)
    toplam = 0

    for i in range(1, sayı_8):
        if(sayı_8%i == 0):
            toplam +=i
    if(sayı_8 == toplam):
        print("Mükemmel Sayı.")
    else:
        print("Mükemmel Sayı değil.")

"""
9) 
Kullanıcıdan 2 tane sayı alarak bu sayıların en büyük ortak bölenini (EBOB) dönen bir tane fonksiyon yazın."""
def test_9():
    ilk_sayı_9 = get_input("EBOB ilk: ", int)
    küççük = ikinci_sayı_9 = get_input("EBOB ikinci: ", int)
    if ilk_sayı_9<ikinci_sayı_9: küççük = ilk_sayı_9

    for i in range(1, küççük+1):
        if ilk_sayı_9%i == 0 and ikinci_sayı_9%i == 0:
            ebob = i
    
    print(ebob)

"""
10)
Kullanıcıdan 2 tane sayı alarak bu sayıların en küçük ortak katlarını (EKOK) dönen bir tane fonksiyon yazın.

"""
def test_10():
    ilk_sayı_10 = get_input("EKOK ilk: ", int)
    küççük_10 = ikinci_sayı_10 = get_input("EKOK ikinci: ", int)
    if ilk_sayı_10<ikinci_sayı_10: küççük_10 = ilk_sayı_10

    for i in range(1, küççük_10+1):
        if ilk_sayı_10%i == 0 and ikinci_sayı_10%i == 0:
            ebob_10 = i
    print((ilk_sayı_10*ikinci_sayı_10)//ebob_10)
"""
11)

Bu projede ise 4 tane sınıfı oluşturun.
Hayvan Sınıfı ------> Bütün hayvanların ortak özelliklerinin toplandığı sınıf olacak.

Köpek Sınıfı ------> Bu sınıf, hayvan sınıfından miras alan bir sınıf olacak. Ayrıca bu sınıfa köpeklere ait ek özellikler ve metodlar ekleyin.

Kuş Sınıfı ------> Bu sınıf, hayvan sınıfından miras alan bir sınıf olacak. Ayrıca bu sınıfa kuşlara ait ek özellikler ve metodlar ekleyin.

At Sınıfı ------> Bu sınıf, hayvan sınıfından miras alan bir sınıf olacak. Ayrıca bu sınıfa atlara ait ek özellikler ve metodlar ekleyin.

"""
def test_11():
    class Hayvan:
        def __init__(self, isim, yaş):
            self.isim = isim
            self.yaş = yaş

        def __str__(self):
            return f"İsim: {self.isim}\nYaş: {self.yaş}"
        
        def alive(self):
            print("Canlı.")

        class Köpek:
            def __init__(self, et):
                self.et = et

            def __str__(self):
                return f"Et: {self.et}"
            
            def hav(self):
                print("Hav hav")
        
        class Kuş:
            def __init__(self, yumurta):
                self.yumurta = yumurta

            def __str__(self):
                return f"Yumurta: {self.yumurta}"

            def cik(self):
                print("Cik cik")
        
        class At:
            def __init__(self, havuç):
                self.havuç = havuç

            def __str__(self):
                return f"Havuç: {self.havuç}"

            def kişneme(self):
                print("Oink?")

    hayavan = Hayvan("Mahmut", 5)
    köpke = Hayvan.Köpek(20)
    guş = Hayvan.Kuş(72)
    ad = Hayvan.At(-1)

    print(hayavan)
    hayavan.alive()
    print(köpke)
    köpke.hav()
    print(guş)
    guş.cik()
    print(ad)
    ad.kişneme()

while True:
    test = get_input("Test seçiniz (12 ile çıkınız): ", int)
    match test:
        case 1:
            test_1()
        case 2:
            test_2()
        case 3:
            test_3()
        case 4:
            test_4()
        case 5:
            test_5()
        case 6:
            test_6()
        case 7:
            test_7()
        case 8:
            test_8()
        case 9:
            test_9()
        case 10:
            test_10()
        case 11:
            test_11()
        case 12:
            break
        case _:
            print("Yanlış girdiniz.")