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
""""""
class Card:
    Suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    Values = ['A', '2', '3','4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        
    def __str__(self):
        return(f"{self.value} of {self.suit}")
    
import random
class Deck:
    def __init__(self):
        self.cards = [Card(suit, value) for suit in Card.Suits for value in Card.Values]
        
    def shuffle(self):
        random.shuffle(self.cards)
        
    def deal(self, num_cards):
        dealt_cards = self.cards[:num_cards]
        self.cards = self.cards[num_cards:]
        return dealt_cards

deck = Deck()
deck.shuffle()
hand = deck.deal(5)
for card in hand:
    print(card)
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
import math 

class drone:
    def __init__(self, id, x=0, y=0, z=0, velocity=0, capacity=100, battery=1000):
        self.id = id
        self.x = x
        self.y = y
        self.z = z
        self.velocity = velocity
        self.capacity = capacity
        self.battery = battery
        self.kalkis_noktası = (x, y, z)
        self.charge = 0 
    
    def take_off(self, height):
        self.y = height
        print(f"drone {self.id}: {height}")
    
    def move(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        print(f"drone {self.id}: ({x}, {y}, {z})")
    
    def return_to_launch(self):
        self.x, self.y, self.z = self.kalkis_noktası
        print(f"drone {self.id}: {self.kalkis_noktası}")
        
    def charge_al(self,charge_miktarı):
        if self.capacity >= charge_miktarı:
           self.charge = self.capacity 
           print(f"drone {self.id}: {charge_miktarı} miktar yük alndı")
        else:
            print(f"drone {self.id}: yük miktarı fazla taşıyamaz")
        
    def charge_bırak(self):
        print(f"drone {self.id}: miktar yük bıraktı")
        self.charge = 0
    
    def kalkıs_noktasına_uzaklık(self):
        x1 = self.x - self.kalkis_noktası[0]
        y1 = self.y - self.kalkis_noktası[1]
        z1 = self.z - self.kalkis_noktası[2]
        uzaklik = math.sqrt(x1**2 + y1**2 + z1**2)
        print(float(uzaklik))
        return uzaklik 
        

drone1 = drone(0)
def main():
    
    drone1.charge_al(200)
    drone1.take_off(10)
    drone1.move(10,10,10)
    drone1.charge_bırak()
    drone1.kalkıs_noktasına_uzaklık()
    drone1.return_to_launch()

if __name__ == '__main__':
    main()

"""
3)
1000 int den oluşan random bir liste yaratın ve istediğiniz sorting algoritmasını kullanarak küçükten büyüğe sıralayan bir script yazınız.
"""
import random
n = 1000
list = random.sample(range(0,1000),n)
print(list)

def insertionSort(arr):
    n = len(arr)
    if n <= 1:
        return
    for i in range(1,n):
        key = arr[i]
        j = i - 1
        while j>= 0 and key < arr[j]:
            arr[j+1] = arr[j]
            j -= 1 
        arr[j+1] = key 

arr = list 
insertionSort(arr)
print(arr)

"""
4)
n katlı bir gökdelende olduğunuzu farz edin, elinizde 2 adet yumurta var. amacınız yumurtanın kırılmadan atılabileceği en yüksek katı bulmak. 
yumurtayı atmak için k adet deneme yapabilirsiniz ve yumurta herhangi bir katta kırılabilir (evet herhangi bir kat)

n verilen k değerine göre en fazla kaç olabilir?  (k * (k+1)) / 2 >= n 
"""
import math
n = int(input("sayı giriniz:"))
k = math.ceil((-1 + math.sqrt(1 + 8 * n)) / 2)

print(f"deneme sayısı: {k}")


    
    

"""
5)
bir sayının çift olup olmadığını hesaplayan en iyi fonksiyonu yazmaya calışın. (diğer katılımcılarla karşılaştırılacak)

"""
sayı = int(input("sayı girin:"))
for i in range(sayı+1):
    if i % 2 == 0:
        print(i)
        
# Review
"""
Test 1deki deste oluşturma kısmı güzel yapılmış.
Test 5de her iterasyonda print yapmak yerine sonuca göre tek seferde çıktı almak daha iyi olur. 
(terminal overflow, stack overflow Araştır)
"""