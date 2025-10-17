#random
import random
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
def test_1():
    pass
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

def test_2():
    pass
"""
3)
1000 int den oluşan random bir liste yaratın ve istediğiniz sorting algoritmasını kullanarak küçükten büyüğe sıralayan bir script yazınız.
"""
#Bubble sort
def test_3():
    list_uzunluk = get_input("Liste uzunluğu giriniz: ", int)
    rand_list = random.sample(range(1, list_uzunluk+1), list_uzunluk)
    print(rand_list)

    def Bubble_sort(list_to_sort):
        for j in range(len(list_to_sort)-1, 0, -1):
            swapped = False
            for i in range(j):
                if i+1 < len(list_to_sort) and list_to_sort[i] > list_to_sort[i+1]:
                    list_to_sort[i], list_to_sort[i+1] = list_to_sort[i+1], list_to_sort[i]
                    swapped = True
            if not swapped: break
        return list_to_sort

    print(Bubble_sort(rand_list))

"""
4)
n katlı bir gökdelende olduğunuzu farz edin, elinizde 2 adet yumurta var. amacınız yumurtanın kırılmadan atılabileceği en yüksek katı bulmak. 
yumurtayı atmak için k adet deneme yapabilirsiniz ve yumurta herhangi bir katta kırılabilir (evet herhangi bir kat)

n verilen k değerine göre en fazla kaç olabilir?
"""

def test_4():
    n = get_input("Kat sayısını giriniz: ", int)
    k = int((1 + 8 * n)**(1/2) / 2)

    print("Maksimum deneme sayısı: ", k)

"""
5)
bir sayının çift olup olmadığını hesaplayan en iyi fonksiyonu yazmaya calışın. (diğer katılımcılarla karşılaştırılacak)

"""

def test_5():
    sayu = get_input("Çift mi tek mi diye kontrol etmek istediğiniz sayıyı giriniz: ",int)
    
    #ilk bite bak ona göre çift mi tek mi söyle
    if(sayu & 1 == 1): 
    	print("Tek") 
    else: 
    	print("Çift") 


while True:
    test = get_input("Test seçiniz (6 ile çıkınız): ", int)
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
            break
        case _:
            print("Yanlış girdiniz.")