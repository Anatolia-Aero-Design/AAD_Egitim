import random
import time
import math

"""
1)
Bir deste (deck) sınıfı oluştur. Bu sınıfın içinde dahili olarak kart (card) sınıfı kullanılmalıdır. Gereksinimlerin şunlardır:
Deck (Deste) sınıfında, desteden bir kart dağıtan (deal) bir metot bulunmalı.
    Bir kart dağıtıldıktan sonra desteden çıkarılmalıdır.

Bir karıştırma (shuffle) metodu bulunmalı. Bu metot, destede tüm 52 kartın bulunduğundan emin olmalı ve kartları rastgele şekilde yeniden sıralamalıdır.

Card (Kart) sınıfı ise şu iki özelliğe sahip olmalıdır:
    - Renk (suit): Hearts (Kupa), Diamonds (Karo), Clubs (Sinek), Spades (Maça)
    - Değer (value): A, 2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K
"""

#class Card:
#    def __init__(self, suit, value):
#        self.suit = suit
#        self.value = value
#
#    def __str__(self):
#        return self.suit + " " + self.value
#
#class Deck:
#    def __init__(self):
#        self.shuffle()
#
#    def shuffle(self):
#        self.deck = []
#        for suit in ["Hearts", "Diamonds", "Clubs", "Spades"]:
#            for value in ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]:
#                self.deck.append(Card(suit, value))
#
#        random.shuffle(self.deck)
#
#    def deal(self):
#        print(f"{self.deck.pop()} karti verildi!")
#
#deck = Deck()
#for i in range(10):
#    deck.deal()  

"""
2)
basit bir drone classı yaratın her dronun sahip olması gerek standart özellikler:

*id,
*x,y,z kordinatları
*hızı,
*taşıyabiliceği yük,
*batarya,

her dronun sahip olması gereken fonksiyonlar (Bu fonksiyonlar hayali bir drone için calışmalı mesela takeoff komutunu verdiğinizde ucağın kalkmasını değil 
sadece y değerinin takeoff komutunda verdiğiniz yüksekliğe eşitlenmesini istiyorum, aynı şekilde (10,5,20) noktasına git dediğinizde gercekten oraya giden 
bir drone değil xyz'si bu birimlere eşitlenmesini istiyorum),

*takeoff
*return to launch
*move
*yük al
*yük bırak,
*kalkış noktasına uzaklık,
"""

#class Drone:
#    def __init__(self, id = time.time(), coordinates = (0,0,0), load_capacity = 10):
#        self.id = id
#        self.x, self.y, self.z = coordinates
#        self.takeoff_x, self.takeoff_y, self.takeoff_z = coordinates
#        self.load_capacity = load_capacity
#
#        self.speed = 0
#        self.battery = 100
#        self.isloaded = False
#    
#    def takeoff(self, height):
#        self.y = height
#
#    def return_to_launch(self):
#        self.move(self.takeoff_x, self.y, self.takeoff_z)
#        self.y = self.takeoff_y
#
#    def move(self, x, y, z):
#        self.x, self.y, self.z = x, y, z
#
#    def load_up(self, load_weight):
#        if(load_weight < self.load_capacity):
#            self.isloaded = True
#
#    def load_down(self):
#        self.isloaded = False
#
#    def distance(self):
#        print(f"Kalkışa uzaklık: {math.sqrt((self.takeoff_x-self.x)**2 + (self.takeoff_y-self.y)**2 + (self.takeoff_z-self.z)**2)}")

"""
3)
1000 int den oluşan random bir liste yaratın ve istediğiniz sorting algoritmasını kullanarak küçükten büyüğe sıralayan bir script yazınız.
"""

#def check_list(l):
#    for i in range(len(l)-1):
#        if l[i] > l[i+1]:
#            print(l[i], l[i+1])
#            return False
#
#    return True
#
#list_1000 = [random.randint(0, 10000) for _ in range(1000)]
#
#new_list = []
#new_list.append(list_1000.pop())
#print(new_list)
#
#for i in list_1000:
#    braked = False
#    for j in new_list:
#        if i <= j:
#            print(i, j, new_list.index(j))
#            new_list.insert(new_list.index(j), i)
#
#            if not check_list(new_list):
#                print("err")
#
#            braked = True
#            break
#
#    if not braked:
#        new_list.append(i)
    
#print(new_list)
#print(check_list(new_list))
#print(len(new_list))


"""
4)
n katlı bir gökdelende olduğunuzu farz edin, elinizde 2 adet yumurta var. amacınız yumurtanın kırılmadan atılabileceği en yüksek katı bulmak. 
yumurtayı atmak için k adet deneme yapabilirsiniz ve yumurta herhangi bir katta kırılabilir (evet herhangi bir kat)

n verilen k değerine göre en fazla kaç olabilir?
"""

#n = int(input("Gökdelen kat sayısı girin: "))
#
#üs = 0
#while(n >= pow(2,üs)):
#    üs += 1
#
#print(f"en fazla {üs} deneme hakkı ile bulunur")

"""
5)
bir sayının çift olup olmadığını hesaplayan en iyi fonksiyonu yazmaya calışın. (diğer katılımcılarla karşılaştırılacak)

"""

#csayi = input("Çift sayı girin: ")
#
#try:
#    csayi = int(csayi)
#    if csayi % 2 == 0:
#        print(f"{csayi} bir çift sayı!")
#    else:
#        print(f"{csayi} bir tek sayı!")
#
#except:
#    print(f"{csayi} bir sayı değil...")