__Author__ = "Alperen Burak Yeşil"

# (Algoritma ##)

sayi1 = float(input("1.Sayı: "))
sayi2 = float(input("2. Sayı: "))
sayi3 = float(input("3. Sayı: "))

sonuc = sayi1 * sayi2 * sayi3

print("\n{} * {} * {} = {} ".format(sayi1,sayi2,sayi3,sonuc))

# (Algoritma #1)

isim = input("Adınız: ")
soyisim = input("Soyadınız: ")
numara = input("Numaranız: ")

print("\n", "Adı: ", isim, "\n", "Soyadı: ", soyisim, "\n",  "Numarası: ", numara)

# (Algoritma #2)

Dik1 = float(input("1. Dik Kenar: "))
Dik2 = float(input("2. Dik Kenar: "))

Hipotenüs = (Dik1**2 + Dik2**2)**0.5

print("Hipotenüs Uzunluğu: ", round(Hipotenüs, 2))

# (Algoritma #3)

print("Boyunuzu Metre Kilonuzu Kilogram Cinsinden Giriniz...")
Boy = float(input("Boyunuz: "))
Kg = float(input("Kilonuz: "))
VKI = round(Kg/(Boy**2),2)

print("\nVücut Kitle İndeksiniz: {}".format(VKI))

if VKI >= 0:
    if VKI < 18.5:
        print("Zayıf")
    elif 18.5 <= VKI < 25:
        print("Normal")
    elif 25 <= VKI < 30:
        print("Fazla Kilolu")
    else:
        print("Obez")
else:
    print("Hatalı Giriş Yaptınız Lütfen Tekrar Deneyiniz")

# (Algoritma #4)

vize1 = float(input("1. Vize Notunuz: "))
vize2 = float(input("2. Vize Notunuz: "))
Final = float(input("Final Notunuz: "))
Not = (vize1*0.3) + (vize2*0.3) + (Final*0.4)

if 0 <= Not <=100:
    if Not >= 90:
        print("Harf Notu: AA")
    elif Not >= 85:
        print("Harf Notu: BA")
    elif Not>= 80:
        print("Harf Notu: BB")
    elif Not >= 75:
        print("Harf Notu: CB")
    elif Not >= 70:
        print("Harf Notu: CC")
    elif Not>= 65:
        print("Harf Notu: DC")
    elif Not>= 60:
        print("Harf Notu: DD")
    elif Not>= 55:
        print("Harf Notu: FD")
    else:
        print("Harf Notu: FF")
else:
    print("Hatalı Giriş Yaptınız Lütfen Tekrar Deneyiniz")

# (Algoritma #5)

for a in range(1,11):
    print("-" * 20)
    print(a,"'ler")

    print("-" * 20)
    for b in range(1,11):
        print(a, "x", b, "= ",a*b)

# (Algoritma #6)

toplam=0
while (True):
    newsayi = input("Sayınız: ")
    if newsayi =="q":
        break
    try :
        newsayi = int(newsayi)
        toplam += newsayi
    except:
        print("Lütfen Tekrar Deneyiniz")
print("\nToplam: ", toplam)

# (Algoritma #7)

ksayi = int(input("Sayı: "))
b =0
bölen = 1

while (True):
    if ksayi / bölen == 1:
        break
    else:
        if ksayi % bölen == 0:
            b = b  + bölen
            bölen = bölen +1
        else:
            bölen +=1

if b == ksayi:
    print(ksayi, "Mükemmel Sayı'dır")
else:
    print(ksayi, "Mükemmel Sayı Değildir")

# (Algoritma #8)

def EBOB(esay1,esay2):
    ysl = 1
    bolen = 2
    ornek1 = esay1   # ana sayıyı değiştirmemek için
    ornek2 = esay2   # ana sayıyı değiştirmemek için
    while True:
        if ornek1 == 1 and ornek2 == 1:
            break
        else:
            if ornek1 % bolen == 0 and ornek2 % bolen == 0:
                ornek1 /= bolen
                ornek2 /= bolen
                ysl *= bolen
            elif ornek1 % bolen == 0:
                ornek1 /= bolen
            elif ornek2 % bolen == 0:
                ornek2 /= bolen
            else:
                bolen += 1
    return ysl

esay1 = int(input("1. Sayı: "))
esay2 = int(input("2.Sayı: "))

print("EBOB: ", EBOB(esay1,esay2))


# (Algoritma #9)

def EKOK(say1,say2):
    orn = say1   #ana sayıyı değiştirmemek için
    orn2 = say2   #ana sayıyı değiştirmemek için
    ysl1=1
    bolen =2

    while (True):
        if orn == 1 and orn2 == 1:
            break
        else:
            if orn % bolen == 0 or orn2 % bolen == 0:
                if orn % bolen == 0 and orn2 % bolen == 0: #Her iki sayıyıda bölüyorsa
                    orn /= bolen
                    orn2 /= bolen
                    ysl1 *= bolen
                elif orn % bolen == 0: # sadece 1. sayıyı bölüyorsa
                    orn /= bolen
                    ysl1 *= bolen
                else: # sadece 2. sayıyı bölüyorsa
                    orn2 /= bolen
                    ysl1 *= bolen
            else: # hiçbir sayıyı bölmüyorsa
                bolen += 1
    return ysl1


say1 = int(input("1. Sayı: "))
say2 = int(input("2.Sayı: "))
print("EKOK: ", EKOK(say1,say2))

# (Algoritma #10)

class Hayvanlar():
    def __init__(self, Beslenme_Şekilleri, Hücre_sayısı, Üreme_Şekilleri, Hareket_Tipi):
        self.beslenme_şekilleri = Beslenme_Şekilleri
        self.hücre_sayısı = Hücre_sayısı
        self.üreme_şekilleri = Üreme_Şekilleri
        self.hareket_tipi = Hareket_Tipi
    def Bilgileri_Göster(self):
        print("""
        ******** Hayvanların Genel Özellikleri ********
        Beslenme Şekilleri: {}
        Hücre Sayıları: {}
        Üreme Şekilleri: {}
        Hareket Tipleri: {}
        """.format(self.beslenme_şekilleri, self.hücre_sayısı, self.üreme_şekilleri, self.hareket_tipi))
hayvanlar = Hayvanlar("Heterotrof Beslenme (Hazır Beslenme)", "Çok Hücreli", "Eşeyli Üreme", "Aktif Hareket")

class Köpekler(Hayvanlar):
    def __init__(self, Beslenme_Şekilleri, Hücre_sayısı, Üreme_Şekilleri, Hareket_Tipi, Hücre_Tipi, Vücut_Örtüleri, Engeli):
        super().__init__(Beslenme_Şekilleri, Hücre_sayısı, Üreme_Şekilleri, Hareket_Tipi)
        self.hücre_tipi = Hücre_Tipi
        self.vücut_örtüleri = Vücut_Örtüleri
        self.engeli = Engeli

    def Bilgileri_Göster(self):
        print("""
        ******** Köpeklerin Genel Özellikleri ********
        Beslenme Şekli: {}
        Hücre Sayısı: {}
        Üreme Şekli: {}
        Hareket Tipi: {}
        Hücre Tipi: {}
        Vücut Örtüsü: {}
        Engeli: {}
        """.format(self.beslenme_şekilleri, self.hücre_sayısı, self.üreme_şekilleri, self.hareket_tipi,self.hücre_tipi,self.vücut_örtüleri,self.engeli))

köpekler = Köpekler("Heterotrof Beslenme [Omnivor(Hem et Hem ot)]", "Çok Hücreli", "Eşeyli Üreme", "Aktif Hareket (Yürüme)", "Ökaryot", "Kıllar" ,"Doğduklarında Hem Kör Hem de Sağırdır")

class Kuşlar(Hayvanlar):
    def __init__(self, Beslenme_Şekilleri, Hücre_sayısı, Üreme_Şekilleri, Hareket_Tipi, Hücre_Tipi, Vücut_Örtüleri, Ses_Taklidi):
        super().__init__(Beslenme_Şekilleri, Hücre_sayısı, Üreme_Şekilleri, Hareket_Tipi)
        self.hücre_tipi = Hücre_Tipi
        self.vücut_örtüleri = Vücut_Örtüleri
        self.ses_taklidi = Ses_Taklidi
    def Bilgileri_Göster(self):
        print("""
        ******** Kuşların Genel Özellikleri ********
        Beslenme Şekli: {}
        Hücre Sayısı: {}
        Üreme Şekli: {}
        Hareket Tipi: {}
        Hücre Tipi: {}
        Vücut Örtüsü: {}
        Ses Taklidi: {}
        """.format(self.beslenme_şekilleri, self.hücre_sayısı, self.üreme_şekilleri, self.hareket_tipi,self.hücre_tipi,self.vücut_örtüleri,self.ses_taklidi))

kuşlar = Kuşlar("Heterotrof Beslenme [Çoğu Herbivor(Otçul)]", "Çok Hücreli", "Eşeyli Üreme", "Aktif Hareket (Uçma)", "Ökaryot", "Tüyler", "İnsanların Seslerini Taklit Edebilirler")

class Atlar(Hayvanlar):
    def __init__(self, Beslenme_Şekilleri, Hücre_sayısı, Üreme_Şekilleri, Hareket_Tipi, Hücre_Tipi, Vücut_Örtüleri, Engeli):
        super().__init__(Beslenme_Şekilleri, Hücre_sayısı, Üreme_Şekilleri, Hareket_Tipi)
        self.hücre_tipi = Hücre_Tipi
        self.vücut_örtüleri = Vücut_Örtüleri
        self.engeli = Engeli
    def Bilgileri_Göster(self):
        print("""
        ******** Atların Genel Özellikleri ********
        Beslenme Şekli: {}
        Hücre Sayısı: {}
        Üreme Şekli: {}
        Hareket Tipi: {}
        Hücre Tipi: {}
        Vücut Örtüsü: {}
        Engeli: {}
        """.format(self.beslenme_şekilleri, self.hücre_sayısı, self.üreme_şekilleri, self.hareket_tipi,self.hücre_tipi,self.vücut_örtüleri,self.engeli))

atlar = Atlar("Heterotrof Beslenme [Herbivor(Otçul)]", "Çok Hücreli", "Eşeyli Üreme", "Aktif Hareket (Yürüme)", "Ökaryot","Kıllar", "Gri ve Yeşili Ayırt Edemezler")

print(hayvanlar.Bilgileri_Göster())
print(köpekler.Bilgileri_Göster())
print(kuşlar.Bilgileri_Göster())
print(atlar.Bilgileri_Göster())