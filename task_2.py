"""
1.
Create a deck of cards class. Internally, the deck of cards should use another class, a card_class class. Your requirements are:
"""

import random
import os

gostersinmi=True
card_el=[]

class Card:
  #-The Card class should have a suit (Hearts, Diamonds, Clubs, Spades) and a value (A,2,3,4,5,6,7,8,9,10,J,Q,K)
   suit = ["Hearts","Diamonds","Clubs","Spades"]
   value = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
   cards = [] 
  
   def card_generator(self):
    self.cards.clear()
    card_el.clear()
    for s in self.suit:
       for v in self.value:
           self.cards.append(s+" "+v)
       
    print('\033[94m'+"Desteniz Sıralı Bir Şekilde Başarıyla Oluşturuldu. \n"+'\033[0m')
           
        
card_class=Card()

class Deck(Card):
   
    #-There should be a shuffle method which makes sure the deck of cards has all 52 cards and then rearranges them randomly.
    def shuffle(self):
        if(len(self.cards)==52):
         random.shuffle(self.cards)
         print('\033[94m'+"Deste Karıştırıldı. \n"+'\033[0m')
         
        else:
         print('\033[91m'+"Destede Eksik Kart Var! \n"+'\033[0m')
         card_class.card_generator()
    
    #-The Deck class should have a deal method to deal a single card_class from the deck. After a card_class is dealt, it is removed from the deck.
    def deal(self):
        if(len(self.cards)>0):
         print('\033[94m'+"{} desteden çıkarıldı. \n".format(self.cards[len(self.cards)-1])+'\033[0m')
         card_el.append(self.cards[len(self.cards)-1])
         self.cards.pop()
         
        else:
         print('\033[91m'+"Destede Kart Kalmamış. \n"+'\033[0m')
         card_class.card_generator()
      

deck=Deck()

while True:
 #C dillerinde olan switch'i python 3.10 da getirmişler. Önceki sürümlerde çalışır mı bilmiyorum.
 if(gostersinmi==True):
     print("Destedeki Kartlar:  {}".format(deck.cards))
 print("\n Eliniz:  {} \n".format(card_el))
 python_3_10_switch_statement = input('\033[95m'+'\033[1m'+"Kartları Oluşturmak İçin: g ,Kartları Karıştırmak İçin: s ,Kart Çekmek İçin: d ,Desteyi Göstermeyi Aç-Kapa: m , Çıkmak İçin: q Gönderiniz: \n"+'\033[0m') 
 match python_3_10_switch_statement:
     case "g":
         os.system("clear")
         card_class.card_generator()
     case "s":
         os.system("clear")
         deck.shuffle()
     case "d":
         os.system("clear")
         deck.deal()
     case "m":
         os.system("clear")
         gostersinmi = not gostersinmi
     case "q":
         os.system("clear")
         break
     case _:
         os.system("clear")
         print('\033[91m'+"Lütfen Geçerli Bir Girdi Gönderiniz. \n"+'\033[0m')


"""
#2.
basit bir drone classı yaratın her dronun sahip olması gerek standart özellikler:
"""

import math

class Drone:
    
    def __init__(self,id,kordinat,hiz,kapasite,batarya) :
        self.id=id                      #id,,
        self.kordinat_baslangic=kordinat
        self.kordinat_anlik=kordinat    #x,y,z kordinatları,
        self.hiz=hiz                    #hızı,
        self.kapasite=kapasite          #taşıyabiliceği yük,
        self.batarya=batarya            #batarya,
        self.yuk_durumu=False
        self.uzaklik =0
        

 #her dronun sahip olması gereken fonksiyonlar(Bu fonksiyonlar hayali bir drone için calışmalı mesela takeoff komutunu verdiğinizde ucağın kalkmasını değil sadece y değerinin takeoff komutunda verdiğiniz yüksekliğe eşitlenmesini istiyorum, aynı şekilde (10,5,20) noktasına git dediğinizde gercekten oraya giden bir drone deil xyz si bu birimlere eşitlenmesini istiyorum),

    def takeoff(self):                       #takeoff
        try:
            self.kordinat_anlik[1] = float(input("Kaç Birim Yükselmek İstiyorsunuz: ")) +float(self.kordinat_anlik[1])
            self.batarya-=5
            print("")
        except:
            print('\033[91m'+"Lütfen Geçerli Sayı Giriniz.\n"+'\033[0m')

    def return_to_launch(self):              #return to launch
       self.kordinat_anlik=self.kordinat_baslangic
       self.batarya-=5
       print("Baslangic Kordinatlarına Dönüldü")
       
    def move(self):                          #move
     varis_noktasi=input("Gitmek İstediğiniz Kordinatları x,y,z Şeklinde Giriniz: ").split(",")
     print("")
     try:  
        for i in range(3):
             float(varis_noktasi[i])

        if(len(varis_noktasi)==3):
            self.kordinat_anlik=varis_noktasi
            self.batarya-=5
        else:
            print('\033[91m'+"Lütfen Geçerli Sayı Dizisini x,y,z Şeklinde Giriniz.\n"+'\033[0m')
     except:
            print('\033[91m'+"Lütfen Geçerli Sayı Dizisini x,y,z Şeklinde Giriniz.\n"+'\033[0m')
   
    def yuk_al(self):                        #yük al
     try:
        if(self.yuk_durumu==False and self.kapasite>=float(input("Almak İstediğiniz Yükün Ağırlığını Giriniz: "))):
              print("\n Yük Başarıyla {} Kordinatlarından Alındı \n".format(self.kordinat_anlik))
              self.batarya-=5
              self.yuk_durumu=True
        elif(self.yuk_durumu == True):
              print("Hali Hazırda Ağırlık Taşıyor!\n")
        else:
              print("Yük, Kapasiteden Daha Fazla!\n")

     except:
        print('\033[91m'+"Lütfen Geçerli Bir Ağırlık Giriniz.\n"+'\033[0m')
       
    def yuk_birak(self):                     #yük bırak,
        if(self.yuk_durumu==True):
            self.yuk_durumu=False
            self.batarya-=1
            print("Yük {} Kordinatlarına Bırakıldı.".format(self.kordinat_anlik))
        else:
            print("Şuan Drone Yük Taşımıyor\n")

    def uzaklik_kalkis_noktasi(self):        #kalkış noktasına uzaklık,
        for k in range(3):
          self.uzaklik += (float(self.kordinat_anlik[k])-float(self.kordinat_baslangic[k]))**2
        print("Kalış Noktasına Uzaklığınız: {}".format(math.sqrt(self.uzaklik)))

    def kordinat_goster(self):
        print("Kordinatlarınız: {}\n".format(self.kordinat_anlik))
    def batarya_goster(self):
        print("Bataryanız: {}\n".format(self.batarya))

drone1=Drone(1,[3.0,4.0,5.0],12,35,120) #Dronu oluştururken lütfen kordinat değerini [x,y,z] cinsinden veriniz

while True:
 # Umarım çalışıyordur, bu yapı if-elif den daha pratik oldu burda :D
 drone1.kordinat_goster()
 drone1.batarya_goster()
 drone_kontrol = input('\033[95m'+'\033[1m'+"Drone Kalk: k ,Drone Kalkışa Dön d ,Drone Move: m ,Drone Yük Al: a ,Drone Yük Bırak: b ,Drone Kalkışa Uzaklık: u ,Çıkmak İçin: q Gönderiniz: \n"+'\033[0m') 
 match drone_kontrol:
     case "k":
         os.system("clear")
         drone1.takeoff()
     case "d":
         os.system("clear")
         drone1.return_to_launch()
     case "m":
         os.system("clear")
         drone1.move()
     case "a":
         os.system("clear")
         drone1.yuk_al()
     case "b":
         os.system("clear")
         drone1.yuk_birak()
     case "u":
         os.system("clear")
         drone1.uzaklik_kalkis_noktasi()
     case "q":
         os.system("clear")
         break
     case _:
         os.system("clear")
         print('\033[91m'+"Lütfen Geçerli Bir Girdi Gönderiniz. \n"+'\033[0m')


"""
#3.
1000 int den oluşan random bir liste yaratın ve istediğiniz sorting algoritmasını kullanarak küçükten büyüğe sıralayan bir script yazınız.
"""

liste_random = []

for r in range(1000):
    liste_random.append(random.randint(-5000,5000)) 

for iter in range(len(liste_random)-1,0,-1):
    for index in range(iter):
         if liste_random[index]>liste_random[index+1]:
             gecici = liste_random[index]
             liste_random[index] = liste_random[index+1]
             liste_random[index+1] = gecici

#liste_sirali= sorted(liste_random)

print(liste_random) 


"""
#4.
n katlı bir gökdelende olduğunuzu farz edin, elinizde 2 adet yumurta var. amacınız yumurtanın kırılmadan atılabileceği en yüksek katı bulmak. yumurtayı atmak için k adet deneme yapabilirsiniz ve yumurta herhangi bir katta kırılabilir (evet herhangi bir kat)
n, verilen k değerine göre en fazla kaç olabilir?
"""

#Beynim Yandı therefore Başardım, Pray the Sun! (Dark Souls Gönderme İçerir)
print("\nYumurta Atma Testi\n")
while True:
    try:
        k = int(input("Deneme Hakkı:  \n"))
        break
    except:
        print("Lütfen Geçerli bir kat giriniz (int)\n")

print("Bu kadar deneme hakkı ile anca {} katlı binada yumurta dayanıklılık testi yapabilirsin.\n".format(k*(k+1)/2))


"""
#5.
bir sayının cift olup olmadığını hesaplayan en iyi fonksiyonu yazmaya calışın. (diyer katılımcılarla karşılaştırılacak)
"""

print("Tek mi? Çift mi?")

def ciftmi(girdi):
    try:
        int(girdi)
        if(int(girdi[-1])%2==0):
            print("\n{} Çift Bir Sayı!\n".format(girdi))
        else:
            print("\n{} Tek Bir Sayı!\n".format(girdi))
    except:
        print("\nLütfen int bir değer giriniz!\n")

while True:
    ciftmi(input("Öğrenmek İstediğiniz Sayıyı Giriniz: "))
