# Not: Bu kisimda tam kapsamli bir ros kurulumu yapmaniz gerekmemektedir mavproxy ile de yapabilirsiniz
# fakat tam kapsamli kurulum yapmaniz tercih edilir.

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np

"""
1)
Kamera görüntüsü ile bir nesne tespiti yapin
Renkli bir çerçeve ile tespit edilen nesneyi işaretleyin ve ekranda gösterin.
Bu görüntüdeki nesneyi renk, şekil ve boyut gibi özelliklere göre ayirt edebilirsiniz. (tercih sizin)
"""

# Açikçasi çoğu şeyleri chatgptden aldim ama anlayarak yapmaya çalişiyorum. 
# Hepsi ni kopyala yapiştir yerine parça parça ilerliyorum ve kendim yaziyorum (bazi arrayleri kopyaladim uğraşmamak için)
# Anlayip anlamadiğimi test etmek için yorum satirlari ekledim
class RedFinder(Node):
    def __init__(self):
        # Node açiyoruz
        super().__init__("object_detection_node")

        # Kamera nodeu topice görüntü göndericek, biz de bu topici atiyoruz
        self.subscription = self.create_subscription(
            Image, # Bu çeşit olmasi gereken şeyi
            '/image_raw', # Bu topicten al
            self.image_callback, # Buraya gönder
            10 # Okuduklarin birikirse en fazla bu kadar biriktir
        )

        # Ros2 byte halinde gönderiyor, onlari Cv de kullanabileceğimiz numpy arraye çevirmeye yariyor
        self.bridge = CvBridge()

        # Konsola bilgilendirme gönderiyoruz
        self.get_logger().info("Object detection started")

    def image_callback(self, msg): # Gelen resmi işleme yeri
        # resmi byte dan numpy yapiyoruz
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

        # hsv filtrelemede daha iyiymiş
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Şimdi belirli renk araliklari seçicez.
        # Bu renk araliklarinda olan pixelleri beyaz, gerisini siyah yapicaz
        # bu beyaz siyah image e mask ismi veriyoruz

        # kirmizi renk hsv de iki araliğa yayiliyormuş o yüzden iki maske
        lower_red1 = np.array([0, 120, 70]) # renk araliği 1 taban
        upper_red1 = np.array([10, 255, 255]) # renk araliği 1 tavan
        lower_red2 = np.array([170, 120, 70]) # renk araliği 2 taban
        upper_red2 = np.array([180, 255, 255]) # renk araliği 2 tavan

        # maske görüntüleri oluşturuyoruz
        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

        # Birleştirip tek maske yapiyoruz.
        mask = mask1 + mask2

        # contour yani diş hat yani çerçeve buluyoruz. contourlar ve pixellerinin kordinatlari
        # (iki değer döndürcek ikinciyi kullanmiyoruz. İkincisi hierarşiymiş mesela iki yuvarlak iç içeyse hangisi içte
        # hangisi dişta onu anliyormuşsun ama çok detayli bakmadim)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            # alan buluyoruz, alan fazla küçükse onu almiyoruz
            area = cv2.contourArea(cnt)
            if area > 500:
                # Çevreleyen kareyi hesapla kordinat ver
                x, y, w, h = cv2.boundingRect(cnt)
                # (x,y) sol üst köşe
                # (x+w(idth), y+h(eight)) sağ alt köşe 
                # sondaki 2 kalinlik
                cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
                # sol üst köşenin 10 piksel üstüne 0.5 büyüklüğünde 2 klainliğinda yeşil yazi koy
                cv2.putText(frame, "Kirmizi Cisim", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)

        # ekranda göster
        cv2.imshow("Kirmizi bulucu", frame)
        # bir milisaniye yenileme süresi
        cv2.waitKey(1)

# normalde altttaki kodlar main içinde olcak buglari önlemek için, if name yapiyoruz
# burda birsürü kod var diye böyle yazdim

# rclpy yi, ros py kütüphanesini başlat
rclpy.init(args=None)
node = RedFinder()
# node un döngüsünü başlat, ctrl+c atilana kadar devam
try:
    rclpy.spin(node)
except KeyboardInterrupt:
    pass

# node u, cv2 ekranlarini, rclpy yi kapat
node.destroy_node()
cv2.destroyAllWindows()
rclpy.shutdown()

"""
2)
herhangi bir simülasyon ortaminda (gazebo yada mavproxy), 1 adet döner kanata

1. pre-arm check
2. takeoff
3. simplegoto kullanarak verilen konuma gitme
4. dronu vektorel olarak kontrol (ex: x yönüne 4 m/s ile t saniye ilerle.)
5. return to home 
6. land
Siralanan görevleri yaptirin bunlarin simülasyon ortaminda gercek drone gibi hareket etmeleri gerekmektedir. Gerekirse bana ulaşin veya dökümantasyonlari inceleyin.
"""


"""
3)
kisimda yaptiğiniz şeylerin aynisini sabit kanat ile tekrar deneyin ve farklarina bakin (vektorel hareket kismi bir miktar farkli araştirma yapmaniz gerekmekte)
----------------------------------------------------------------
"""


"""
4)
https://cdn.teknofest.org/media/upload/userFormUpload/Yay%C4%B1mlanan_V8_-_IHA_Yar%C4%B1smalar%C4%B1_Sartnamesi_2025_mceEG.pdf 
linkteki sabit kanat görev 1 ve görev 2'yi simülasyon ortaminda gerçekleştirin

*Direklerin konumlarini kendiniz belirleyin
*Görev 2 için sadece birakma mesaji çikartmaniz yeterli olacaktir. (bir test görüntüsü ile veya konumu bilinen bir nokta ile denemelerinizi gerçekleştirebilirsiniz)
*Görev 1 ve görev 2 arasinda yere inmeyip tek seferde bitirin. (görevlerden sonra başari ile tamamlandiğini gösteren bir mesaj verin)
"""

"""
5) Basit bir PID kontrolcüsü kullanarak sabit kanat bir drone'u belirlediğiniz noktalara götürün. Bu noktalar sirasiyla:
- İrtifa olarak dik bir daliş yapmak kaydiyla alçak bir irtifa seçilmelidir. (örneğin 10 metre)
- Sert bir dönüş (roll ve yaw) yapacak şekilde belirlenmelidir.
Her bir görevi ayri ayri veya bütünleşik bir şekilde gerçekleştirebilirsiniz.
"""
