"""
*1.
https://drive.google.com/drive/folders/1nLAgHSuMhNH3ieTT7ZUl4p6LQJ3uCR_J?usp=sharing

bu linkteki 2 adet rar dosyasını indirin

2 dosyanın içerisinde de düzenlenmemiş datalar bulunmakta.

datalar cift halinde her .jpg dosyasının aynı ada sayıh .txt dosyası vardır

bu dataları 0 dan başlayarak yeni isimler veren bir program yazmanız gerekmektedir.

deneme.jpg, deneme.txt ----->>>>> 0.jpg, 0.txt
deneme2.jpg, deneme2.txt ----->>>>> 1.jpg, 1.txt

*yeni isimlendirilen dosyalar farklı bir dosyaya alınmalı
*txt ve jpg ler aynı dosya içinde olmalı
*eşi olmayan dosya başka bir not defterine not edilmeli
kafanızda takılan bir sorun varsa bana ulaşın
"""






"""
*2.
herhangi bir similasyon ortamında (gazebo yada mavproxy), 1 adet döner kanata

1. pre-arm check
2. takeoff
3. simplegoto kullanarak verilen xyz ye gitme(burda kullanılan ortamlar xyz kordinatı kullanmaz gps kullanır verilen xyz yi gps e cevirip fonksiyona o şekilde vermeniz lazım)
4. dronu vektorel olarak kontrol (ex: x yönüne 4 mt/s ile t saniye ilerle.)
5. return to home 
6. land
sıralanan şeyleri yaptırın bunların similasyon ortamında gercek drone gibi hareket etmeleri gerekmektedir. şuanki planlar cercevesinde bunun eğitimi benim tarafımdan verilmesi planlanmaktadır. planda herhangi bir sorun yada erken ilerleme durumunda dronekit dökümantasyonları kullanılarak yapılabilir.
"""




"""
*3.
kısımda yaptığınız şeylerin aynısını sabit kanat ile tekrar deneyin ve farklarına bakın (vektorel hareket kısmı bir miktar farklı araştırma yapmanız gerekmekte)
----------------------------------------------------------------
"""



"""
Python temelleri kısmının final kısmı
https://www.teknofest.org/upload/diger/ULUSLARARASI%20İHA%20YARIŞMASI%20KURALLAR%20KİTAPÇIĞI%20GÜNCEL.pdf linkteki döner kanat görev 1 ve görev 2(sayfa 53) yi similasyon ortamında gercekleştiriniz

*wp noktalarını kendiniz belirleyin (su alma ve su bırakma alanlarını bulmanıza gerek yok her nokta daha önceden belirlenmiş olsun ve tek tek o noktalar ile görevi simüle edin)
*su alma ve su bırakma kısmında 3 er saniye bekleyin 
*görev 1 ve görev 2 arasında yere inmeyip tek seferde bitirin. 
"""