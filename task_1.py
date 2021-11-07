#@copyright Mustafa SEVİNÇ


class Font:
   EKLE = '\033[95m'+'\033[1m'+'\033[4m'
   BITIR = '\033[0m'
   MAVI = '\033[94m'
   KIRMIZI = '\033[91m'
   KALIN = '\033[1m'

##Kullanıcıdan aldığınız 3 tane sayıyı çarparak ekrana yazdırın. Ekrana yazdırma işlemini format metoduyla yapmaya çalışın

print(Font.EKLE+"3 Sayının Çarpımını Hesaplama\n"+Font.BITIR)

while True:
        try:
            sayi1 = float(input("1. Sayıyı Giriniz: "))
            sayi2 = float(input("2. Sayıyı Giriniz: "))
            sayi3 = float(input("3. Sayıyı Giriniz: "))
            break
        except:
            print(Font.KIRMIZI+"Lütfen Geçerli Sayı Dizisi Giriniz!"+Font.BITIR)

print(Font.KALIN+"Sonuç: {0} * {1} * {2} = {3}\n".format(sayi1,sayi2,sayi3,sayi1*sayi2*sayi3)+Font.BITIR)


#1) Kullanıcıdan ad,soyad ve numara bilgisini alarak bunları alt alta ekrana yazdırın.

print(Font.EKLE+"Kartvizit Oluşturma\n"+Font.BITIR)
ad = input("İsminizi Giriniz: ")
soyad = input("Soyadınızı Giriniz: ")
numara = input("Numaranızı Giriniz: ")
print(Font.KALIN+"""
Ad: {0}
Soyad: {1}
Numara: {2}
\n""".format(ad,soyad,numara)+Font.BITIR)


#2) Kullanıcıdan bir dik üçgenin dik olan iki kenarını(a,b) alın ve hipotenüs uzunluğunu bulmaya çalışın. Hipotenüs Formülü: a^2 + b^2 = c^2

import math
print(Font.EKLE+"2 Kenarı Bilinen Üçgenin Hipotenüsünü Hesaplama\n"+Font.BITIR)

while True:
        try:
            kenar1 = float(input("1. Kenar Uzunluğu: "))
            kenar2 = float(input("2. Kenar Uzunluğu: "))
            break
        except:
            print(Font.KIRMIZI+"Lütfen Geçerli Kenar Uzunlukları Giriniz!"+Font.BITIR)

print(Font.KALIN+"Hipotenüs Uzunluğu: {}\n".format(math.sqrt(kenar1**2+kenar2**2))+Font.BITIR)


"""
3) Kullanıcıdan alınan boy ve kilo değerlerine göre beden kitle indeksini hesaplayın ve şu kurallara göre ekrana şu yazıları yazdırın.
#Beden Kitle İndeksi: Kilo / Boy(m) * Boy(m)"""

print(Font.EKLE+"Beden Kütle İndeksi Hesaplama\n"+Font.BITIR)

while True:
        try:
            boy = float(input("Boyunuzu Metre Cinsinden Giriniz: "))
            kilo = float(input("Kilonuzu Giriniz: "))
            break
        except:
            print(Font.KIRMIZI+"Lütfen Geçerli Ölçüler Giriniz!"+Font.BITIR)

beden_indeks = kilo/boy**2
print(Font.KALIN+"Beden Kütle İndeksiniz: {}".format(beden_indeks)+Font.BITIR)

#BKİ 18.5'un altındaysa -------> Zayıf
if(beden_indeks<18.5):
    print("Zayıfsınız.\n")

#BKİ 18.5 ile 25 arasındaysa ------> Normal
if(18.5<=beden_indeks<25):
    print("Normalsiniz.\n")

#BKİ 25 ile 30 arasındaysa --------> Fazla Kilolu
if(25<=beden_indeks<30):
    print("Fazla Kilolusunuz.\n")

#BKİ 30'un üstündeyse -------------> Obez
if(30<=beden_indeks):
    print("Obezsiniz.\n")


"""
4) Kullanıcının girdiği vize1,vize2,final notlarına notlarına göre harf notunu hesaplayın.
Vize1 toplam notun %30'una etki edecek.
Vize2 toplam notun %30'una etki edecek.
Final toplam notun %40'ına etki edecek."""

print(Font.EKLE+"Vizeler ve Finale Göre Harf Notu Hesaplama\n"+Font.BITIR)

while True:
        try:
            vize1 = float(input("1. Vize Notu: "))
            vize2 = float(input("2. Vize Notu: "))
            final = float(input("Final Notu:"))
            break
        except:
            print(Font.KIRMIZI+"Lütfen Geçerli Not Değerleri Giriniz!"+Font.BITIR)

ortalama_not = (vize1+vize2)*30/100 + final*40/100
print(Font.KALIN+"Ortalama Notunuz: {}".format(ortalama_not)+Font.BITIR)

#Toplam Not >=  90 -----> AA
if(ortalama_not>=90):
    print("Notunuz: AA \n")
#Toplam Not >=  85 -----> BA
elif(ortalama_not>=85):
    print("Notunuz: BA \n")

#Toplam Not >=  80 -----> BB
elif(ortalama_not>=80):
    print("Notunuz: BB \n")

#Toplam Not >=  75 -----> CB
elif(ortalama_not>=75):
    print("Notunuz: CB \n")

#Toplam Not >=  70 -----> CC
elif(ortalama_not>=70):
    print("Notunuz: CC \n")

#Toplam Not >=  65 -----> DC
elif(ortalama_not>=65):
    print("Notunuz: DC \n")

#Toplam Not >=  60 -----> DD
elif(ortalama_not>=60):
    print("Notunuz: DD \n")

#Toplam Not >=  55 -----> FD
elif(ortalama_not>=55):
    print("Notunuz: FD \n")

#Toplam Not <  55 -----> FF
elif(ortalama_not<55):
    print("Notunuz: FF \n")


"""
5) 1'den 10'kadar olan sayılarla ekrana çarpım tablosu bastırmaya çalışın.
İpucu: İç içe 2 tane for döngüsü kullanın. Aynı zamanda sayıları range() fonksiyonunu kullanarak elde edin.
"""

print(Font.EKLE+"Çarpım Tablosu Oluşturma \n"+Font.BITIR)

while True:
 print(Font.MAVI+"Çarpım Tablosunu Görebilmek İçin Soruyu Çözün: 3*1= "+Font.BITIR)
 try:
    if(int(input())==3):
        break
 except:
    print(Font.KIRMIZI+"Lütfen Geçerli Sayı Deneyiniz \n"+Font.BITIR)

for satir in range(9):
    for sutun in range(9):
        if((satir+1)*(sutun+1)>9):
         print("{0}*{1}= {2}".format(sutun+1,satir+1,(satir+1)*(sutun+1)),end=" | ")
        else:
         print("{0}*{1}= {2}".format(sutun+1,satir+1,(satir+1)*(sutun+1)),end="  | ")
    print(end="\n")
    print("------------------------------------------------------------------------------------------")


"""
6)
Her bir while döngüsünde kullanıcıdan bir sayı alın ve kullanıcının girdiği sayıları "toplam" isimli bir değişkene ekleyin. Kullanıcı "q" tuşuna bastığı zaman döngüyü sonlandırın ve ekrana "toplam değişkenini" bastırın.
İpucu : while döngüsünü sonsuz koşulla başlatın ve kullanıcı q'ya basarsa döngüyü break ile sonlandırın.
"""

print(Font.EKLE+"Toplama Makinesi \n"+Font.BITIR)

toplam =0
hatirlatici_cik=0
toplama_while=input("Eklemek İstediğiniz Sayıyı Giriniz: ")

while toplama_while != "q":
   
    if(hatirlatici_cik%5==0):
        print(Font.MAVI+"Sonucu Görmek İçin q Gönderiniz."+Font.BITIR)
    
    try:
     float(toplama_while)
     toplam+=float(toplama_while)
     toplama_while=input("Eklemek İstediğiniz Sayıyı Giriniz:")
     hatirlatici_cik+=1
    
    except:
     print(Font.KIRMIZI+"Lütfen Geçerli Bir Sayi Giriniz"+Font.BITIR)
     toplama_while=input("Eklemek İstediğiniz Sayıyı Giriniz:")
     hatirlatici_cik+=1

print(Font.KALIN+"Girdiğiniz Sayıların Toplamı: {} \n".format(toplam)+Font.BITIR)


"""
7) 
Kullanıcıdan aldığınız bir sayının mükemmel olup olmadığını bulmaya çalışın.
Bir sayının kendi hariç bölenlerinin toplamı kendine eşitse bu sayıya "mükemmel sayı" denir. Örnek olarak, 6 mükemmel bir sayıdır. (1 + 2 + 3 = 6)
"""

print(Font.EKLE+"Sayınız Mükemmel mi? \n"+Font.BITIR)

mukemmel_toplam=0
while True:
    try:
        mukemmel_sayi=int(input("Kontrol Etmek İstediğiniz Sayiyi Giriniz: "))
        break
    except:
        print(Font.KIRMIZI+"Lütfen Geçerli Bir Değer Girin"+Font.BITIR)

for i in range(1,mukemmel_sayi):
    if(mukemmel_sayi%i==0):
        mukemmel_toplam+=i

if(mukemmel_toplam==mukemmel_sayi and mukemmel_sayi>0):
    print(Font.KALIN+"{} Sayısı Mükemmel Bir Sayı. \n".format(mukemmel_sayi)+Font.BITIR)
else:
    print(Font.KALIN+"{} Sayısı Mükemmel Bir Sayı Değil. \n".format(mukemmel_sayi)+Font.BITIR)
   

"""
8) 
Kullanıcıdan 2 tane sayı alarak bu sayıların en büyük ortak bölenini (EBOB) dönen bir tane fonksiyon yazın.
"""

print(Font.EKLE+"Fonksiyon İle EBOB Hesaplama \n"+Font.BITIR)

def ebob_bul(ebob_sayi1,ebob_sayi2):
    ebob_sonuc=0
   
    for x in range(1,ebob_sayi1+1):
     if(ebob_sayi1 % x==0 and ebob_sayi2 % x ==0):
         ebob_sonuc=x
    if(ebob_sayi1>0 and ebob_sayi2>0):
     return Font.KALIN+"{0} ve {1} 'nin EBOB'u: {2} \n".format(ebob_sayi1,ebob_sayi2,ebob_sonuc)+Font.BITIR
    else:
     print("EBOB Hesaplanamadı \n")       

while True:
    try:
        print(ebob_bul(int(input("1. Sayıyı Giriniz: ")),int(input("2. Sayıyı Giriniz: "))))
        break
    except:
        print(Font.KIRMIZI+"Lütfen Geçerli Bir Sayı Giriniz!"+Font.BITIR)


"""
9)
Kullanıcıdan 2 tane sayı alarak bu sayıların en küçük ortak katlarını (EKOK) dönen bir tane fonksiyon yazın.
"""

print(Font.EKLE+"Fonksiyon İle EKOK Hesaplama \n"+Font.BITIR)

def ekok_bul(ekok_sayi1,ekok_sayi2):
    for ekok_sonuc in range(1,10000000):
     if(ekok_sayi1 >0 and ekok_sayi2>0):
         if(ekok_sonuc % ekok_sayi1 == 0 and ekok_sonuc % ekok_sayi2 == 0):
            return Font.KALIN+"{0} ve {1} 'nin EKOK'u: {2} \n".format(ekok_sayi1,ekok_sayi2,ekok_sonuc)+Font.BITIR
     else:
         print(Font.KALIN+"EKOK Hesaplanamadı!\n"+Font.BITIR)
         break


while True:
    try:
        print(ekok_bul(int(input("1. Sayıyı Giriniz: ")),int(input("2. Sayıyı Giriniz: "))))
        break
    except:
        print(Font.KIRMIZI+"Lütfen Geçerli Sayı Giriniz!\n"+Font.BITIR)               


"""
10)
Bu projede ise 4 tane sınıfı oluşturun.
Hayvan Sınıfı ------> Bütün hayvanların ortak özelliklerinin toplandığı sınıf olacak."""

class Hayvan:
    def __init__(self,ismi,ayak_sayisi,rengi,binekmi,cinsiyeti,ucabiliyormu,tehlikelimi,uyku_saati):
        self.ismi=ismi
        self.rengi=rengi
        self.binekmi=binekmi
        self.cinsiyeti=cinsiyeti
        self.tehlileklimi=tehlikelimi
        self.uyku_saati=uyku_saati
    def uykuManager(self,uyku_saati):
      if(8<uyku_saati<23):
          print("Akşam Uyumayı Seven Bir Hayvan")
      else:
          print("Sabah Uyumayı Seven Bir Hayvan")

 

"""
Köpek Sınıfı ------> Bu sınıf, hayvan sınıfından miras alan bir sınıf olacak. Ayrıca bu sınıfa köpeklere ait ek özellikler ve metodlar ekleyin."""

class Kopek(Hayvan):
    def __init__ (self,kulak_tipi,asi_tarihi):
     self.kulak_tipi=kulak_tipi
     self.asi_tarihi=asi_tarihi
    def havla():
        print("HAVHAV, HRR!")

    def kuyruk_salla():
        print("(Köpek Mutlu, Kuyruğunu Sallıyor")


"""
Kuş Sınıfı ------> Bu sınıf, hayvan sınıfından miras alan bir sınıf olacak. Ayrıca bu sınıfa kuşlara ait ek özellikler ve metodlar ekleyin."""

class Kus(Hayvan):
    def __init__(self,kanat_boyutu,gaga_tipi,ucabiliyormu):
     self.kanat_boyutu=kanat_boyutu
     self.gaga_tipi=gaga_tipi
     self.ucabiliyormu=ucabiliyormu
     
    def kanat_cirp():
        print("Uçacakmış Edasıyla Kanat Çırpıyor")   
   
    def inis_yap():
        print("IHA'ninki Kadar Keskin Hedefleme Sistemi İle İniş Yapacağı Yeri Belirledi ve İndi :D")


"""
At Sınıfı ------> Bu sınıf, hayvan sınıfından miras alan bir sınıf olacak. Ayrıca bu sınıfa atlara ait ek özellikler ve metodlar ekleyin."""

class At(Hayvan):
    def __init__(self,max_hiz,tasima_kapasitesi):
        self.max_hiz=max_hiz
        self.tasima_kapasitesi=tasima_kapasitesi
    
    def yarisa_basla():
        print("At Koşturmaya Başladı. Hadi Baydar Kupon Yaptık!")
    
    def kisne():
        print("BRUSHHŞŞ")


sahbatur= At(100,300)
sahbatur.ismi="Sahbatur"
sahbatur.tehlileklimi=True
sahbatur.uyku_saati=21
sahbatur.cinsiyeti="Erkek"
sahbatur.rengi="Siyah"
sahbatur.kisne
print(Font.KALIN+"""Yarış Atı Özellikleri
Adı: {}
Cinsiyeti: {}
Rengi: {}
Uyku Saati: {}
Max Hızı: {}km/s
Yük Kapasitesi: {}kg
""".format(sahbatur.ismi,sahbatur.cinsiyeti,sahbatur.rengi,sahbatur.uyku_saati,sahbatur.max_hiz,sahbatur.tasima_kapasitesi)+Font.BITIR)
