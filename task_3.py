# Not: Bu kısımda tam kapsamlı bir ros kurulumu yapmanız gerekmemektedir mavproxy ile de yapabilirsiniz
# fakat tam kapsamlı kurulum yapmanız tercih edilir.

"""
1)
Kamera görüntüsü ile bir nesne tespiti yapın
Renkli bir çerçeve ile tespit edilen nesneyi işaretleyin ve ekranda gösterin.
Bu görüntüdeki nesneyi renk, şekil ve boyut gibi özelliklere göre ayırt edebilirsiniz. (tercih sizin)
"""

"""
2)
herhangi bir simülasyon ortamında (gazebo yada mavproxy), 1 adet döner kanata

1. pre-arm check
2. takeoff
3. simplegoto kullanarak verilen konuma gitme
4. dronu vektorel olarak kontrol (ex: x yönüne 4 m/s ile t saniye ilerle.)
5. return to home 
6. land
Sıralanan görevleri yaptırın bunların simülasyon ortamında gercek drone gibi hareket etmeleri gerekmektedir. Gerekirse bana ulaşın veya dökümantasyonları inceleyin.
"""


"""
3)
kısımda yaptığınız şeylerin aynısını sabit kanat ile tekrar deneyin ve farklarına bakın (vektorel hareket kısmı bir miktar farklı araştırma yapmanız gerekmekte)
----------------------------------------------------------------
"""


"""
4)
https://cdn.teknofest.org/media/upload/userFormUpload/Yay%C4%B1mlanan_V8_-_IHA_Yar%C4%B1smalar%C4%B1_Sartnamesi_2025_mceEG.pdf 
linkteki sabit kanat görev 1 ve görev 2'yi simülasyon ortamında gerçekleştirin

*Direklerin konumlarını kendiniz belirleyin
*Görev 2 için sadece bırakma mesajı çıkartmanız yeterli olacaktır. (bir test görüntüsü ile veya konumu bilinen bir nokta ile denemelerinizi gerçekleştirebilirsiniz)
*Görev 1 ve görev 2 arasında yere inmeyip tek seferde bitirin. (görevlerden sonra başarı ile tamamlandığını gösteren bir mesaj verin)
"""

"""
5) Basit bir PID kontrolcüsü kullanarak sabit kanat bir drone'u belirlediğiniz noktalara götürün. Bu noktalar sırasıyla:
- İrtifa olarak dik bir dalış yapmak kaydıyla alçak bir irtifa seçilmelidir. (örneğin 10 metre)
- Sert bir dönüş (roll ve yaw) yapacak şekilde belirlenmelidir.
Her bir görevi ayrı ayrı veya bütünleşik bir şekilde gerçekleştirebilirsiniz.
"""
