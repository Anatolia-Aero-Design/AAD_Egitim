"""
1)
Bir deste (deck) sınıfı oluştur. Bu sınıfın içinde dahili olarak kart (card) sınıfı kullanılmalıdır. Gereksinimlerin şunlardır:
Deck (Deste) sınıfında, desteden bir kart dağıtan (deal) bir metot bulunmalı.
    Bir kart dağıtıldıktan sonra desteden çıkarılmalıdır.

Bir karıştırma (shuffle) metodu bulunmalı. Bu metot, destede tüm 52 kartın bulunduğundan emin olmalı ve kartları rastgele şekilde yeniden sıralamalıdır.

Card (Kart) sınıfı ise şu iki özelliğe sahip olmalıdır:
    - Renk (suit): Hearts (Kupa), Diamonds (Karo), Clubs (Sinek), Spades (Maça)
    - Değer (value): A, 2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K
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

class drone:
    x = int(input("x:"))
    y = int(input("y:"))
    z = int(input("z:"))
    
    
    def __init__(self, id, x, y, z, velocity, charge, battery):
        self.id = id
        self.x = x
        self.y = y
        self.z = z
        self.velocity = velocity
        self.charge = charge 
        self.battery = battery
    

    
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0
        self.yer = True
     
    
    def takeoff(self, height):
        if self.yer:
            self.y = height
            self.yer = False
            print("height:{self.y}")
        


"""
3)
1000 int den oluşan random bir liste yaratın ve istediğiniz sorting algoritmasını kullanarak küçükten büyüğe sıralayan bir script yazınız.
"""


"""
4)
n katlı bir gökdelende olduğunuzu farz edin, elinizde 2 adet yumurta var. amacınız yumurtanın kırılmadan atılabileceği en yüksek katı bulmak. 
yumurtayı atmak için k adet deneme yapabilirsiniz ve yumurta herhangi bir katta kırılabilir (evet herhangi bir kat)

n verilen k değerine göre en fazla kaç olabilir?
"""


"""
5)
bir sayının çift olup olmadığını hesaplayan en iyi fonksiyonu yazmaya calışın. (diğer katılımcılarla karşılaştırılacak)

"""
