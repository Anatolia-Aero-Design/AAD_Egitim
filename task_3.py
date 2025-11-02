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

# KULLANMAK İÇİN: Terminal yoluyla kamera görüntüsünü /image_raw a yolla
#class RedFinder(Node):
#    def __init__(self):
#        # Node açiyoruz
#        super().__init__("object_detection_node")
#
#        # Kamera nodeu topice görüntü göndericek, biz de bu topici atiyoruz
#        self.subscription = self.create_subscription(
#            Image, # Bu çeşit olmasi gereken şeyi
#            '/image_raw', # Bu topicten al
#            self.image_callback, # Buraya gönder
#            10 # Okuduklarin birikirse en fazla bu kadar biriktir
#        )
#
#        # Ros2 byte halinde gönderiyor, onlari Cv de kullanabileceğimiz numpy arraye çevirmeye yariyor
#        self.bridge = CvBridge()
#
#        # Konsola bilgilendirme gönderiyoruz
#        self.get_logger().info("Object detection started")
#
#    def image_callback(self, msg): # Gelen resmi işleme yeri
#        # resmi byte dan numpy yapiyoruz
#        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
#
#        # hsv filtrelemede daha iyiymiş
#        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
#
#        # Şimdi belirli renk araliklari seçicez.
#        # Bu renk araliklarinda olan pixelleri beyaz, gerisini siyah yapicaz
#        # bu beyaz siyah image e mask ismi veriyoruz
#
#        # kirmizi renk hsv de iki araliğa yayiliyormuş o yüzden iki maske
#        lower_red1 = np.array([0, 120, 70]) # renk araliği 1 taban
#        upper_red1 = np.array([10, 255, 255]) # renk araliği 1 tavan
#        lower_red2 = np.array([170, 120, 70]) # renk araliği 2 taban
#        upper_red2 = np.array([180, 255, 255]) # renk araliği 2 tavan
#
#        # maske görüntüleri oluşturuyoruz
#        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
#        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
#
#        # Birleştirip tek maske yapiyoruz.
#        mask = mask1 + mask2
#
#        # contour yani diş hat yani çerçeve buluyoruz. contourlar ve pixellerinin kordinatlari
#        # (iki değer döndürcek ikinciyi kullanmiyoruz. İkincisi hierarşiymiş mesela iki yuvarlak iç içeyse hangisi içte
#        # hangisi dişta onu anliyormuşsun ama çok detayli bakmadim)
#        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#
#        for cnt in contours:
#            # alan buluyoruz, alan fazla küçükse onu almiyoruz
#            area = cv2.contourArea(cnt)
#            if area > 500:
#                # Çevreleyen kareyi hesapla kordinat ver
#                x, y, w, h = cv2.boundingRect(cnt)
#                # (x,y) sol üst köşe
#                # (x+w(idth), y+h(eight)) sağ alt köşe 
#                # sondaki 2 kalinlik
#                cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
#                # sol üst köşenin 10 piksel üstüne 0.5 büyüklüğünde 2 klainliğinda yeşil yazi koy
#                cv2.putText(frame, "Kirmizi Cisim", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
#
#        # ekranda göster
#        cv2.imshow("Kirmizi bulucu", frame)
#        # bir milisaniye yenileme süresi
#        cv2.waitKey(1)
#
## normalde altttaki kodlar main içinde olcak buglari önlemek için, if name yapiyoruz
## burda birsürü kod var diye böyle yazdim
#
## rclpy yi, ros py kütüphanesini başlat
#rclpy.init(args=None)
#node = RedFinder()
## node un döngüsünü başlat, ctrl+c atilana kadar devam
#try:
#    rclpy.spin(node)
#except KeyboardInterrupt:
#    pass
#
## node u, cv2 ekranlarini, rclpy yi kapat
#node.destroy_node()
#cv2.destroyAllWindows()
#rclpy.shutdown()

"""
2)
herhangi bir simülasyon ortaminda (gazebo yada mavproxy), 1 adet döner kanata

1. pre-arm check
2. takeoff
3. verilen konuma gitme
4. dronu vektorel olarak kontrol (ex: x yönüne 4 m/s ile t saniye ilerle.)
5. return to home 
6. land (land için de yazdım ama rtl zaten land yapıyor)
Siralanan görevleri yaptirin bunlarin simülasyon ortaminda gercek drone gibi hareket etmeleri gerekmektedir. Gerekirse bana ulaşin veya dökümantasyonlari inceleyin.
"""

"""
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy, HistoryPolicy
from mavros_msgs.srv import CommandBool, SetMode, CommandTOL, CommandHome
from mavros_msgs.msg import State
from sensor_msgs.msg import BatteryState
from geographic_msgs.msg import GeoPoseStamped
from geometry_msgs.msg import Vector3Stamped


# TODO: mavros inside code
# TODO: tek çalıştırma
class TakeoffNode(Node):
    def __init__(self):
        super().__init__('takeoff_node')

        # Info
        self.system_status = -2
        self.voltage = -2
        self.bat_percentage = -2
        self.football = GeoPoseStamped()
        self.football.pose.position.latitude = 39.819077
        self.football.pose.position.longitude = 30.530827
        self.football.pose.position.altitude = 45.0
        self.football.pose.orientation.z = 0.0
        self.football.pose.orientation.w = 1.0

        # QOS
        # battery verisini alırken farklı iletişim metodu kullanıyormuş
        qos_battery = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.VOLATILE,
            history=HistoryPolicy.UNKNOWN,
        )

        # Subscriptions
        self.state_sub = self.create_subscription(State, "/mavros/state", self.state_callback, 10)
        # Normalde qos_battery ile beraber çalışması lazım, ancak araştırdığımdan anladığım kadarıyla bir bug? var
        # Battery yi de kontrol etmişim say...
        #self.battery_sub = self.create_subscription(BatteryState, "/mavros/battery", self.battery_callback, qos_battery)

        # Clients
        self.set_mode_client = self.create_client(SetMode, '/mavros/set_mode')
        self.arm_client = self.create_client(CommandBool, '/mavros/cmd/arming')
        self.takeoff_client = self.create_client(CommandTOL, '/mavros/cmd/takeoff')
        self.set_home_client = self.create_client(CommandHome, '/mavros/cmd/set_home')
        self.land_client = self.create_client(CommandTOL, '/mavros/cmd/land')

        while not self.set_mode_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for set_mode service...')
        while not self.arm_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for arm service...')
        while not self.takeoff_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for takeoff service...')

        # Publishers
        self.setpoint_position_global_publisher = self.create_publisher(GeoPoseStamped, '/mavros/setpoint_position/global', 10)
        self.setpoint_position_local_publisher = self.create_publisher(GeoPoseStamped, '/mavros/setpoint_position/local', 10)
        self.setpoint_accel_publisher = self.create_publisher(Vector3Stamped, '/mavros/setpoint_accel/accel', 10)

        # Timers
        #self.setpoint_position_global_timer = self.create_timer(0.2, self.setpoint_position_global)
        #self.setpoint_position_local_timer = self.create_timer(0.2, self.setpoint_position_local)

    def state_callback(self, msg):
        self.system_status = msg.system_status

    def battery_callback(self, msg):
        self.voltage = msg.voltage
        self.bat_percentage = msg.percentage

    def pre_arm(self):
        while self.system_status not in (3,4): #https://mavlink.io/en/messages/common.html#MAV_STATE
            self.get_logger().error(f'Kötü system_status: {self.system_status}') 
            rclpy.spin_once(self) 

        # bir süre kötü system status spamlayıp sonra system status iyi 
        # diyebilir ve bu biraz garip ama basit bir çözüm bulamadım
        self.get_logger().info('System status iyi')

        # Yukarda yorumlama sebebi açıklandı
        # Buraya başka kontroller de eklenebilir...
        #while self.voltage < 0:
        #    self.get_logger().error(f'Voltage error: {self.voltage}')
        #
        #while self.voltage < 5:
        #    self.get_logger().error(f'Low voltage: {self.voltage}')
        #
        #while self.bat_percentage < 13.8:
        #    self.get_logger().error(f'Low battery percentage: {self.bat_percentage}')
        
        self.get_logger().info('Pre arm iyi')


    def set_guided(self):
        self.get_logger().info('GUIDED')
        mode_req = SetMode.Request()
        mode_req.custom_mode = 'GUIDED'
        future = self.set_mode_client.call_async(mode_req)
        while not future.done():
            rclpy.spin_once(self)


    def rtl(self):
        self.get_logger().info('RTL')
        mode_req = SetMode.Request()
        mode_req.custom_mode = 'RTL'
        future = self.set_mode_client.call_async(mode_req)
        while not future.done():
            rclpy.spin_once(self)

        
    def arm_and_takeoff(self):
        self.get_logger().info('ARM')
        arm_req = CommandBool.Request()
        arm_req.value = True
        future = self.arm_client.call_async(arm_req)
        while not future.result():
            rclpy.spin_once(self)

        
        # bazen bir miktar daha zaman isteyebiliyor
        for _ in range(5):
            rclpy.spin_once(self)

        self.get_logger().info('TAKE OFF')
        takeoff_req = CommandTOL.Request()
        # Home'dan 5 metre yukarısı
        takeoff_req.altitude = 5.0
        takeoff_req.min_pitch = 0.0
        takeoff_req.yaw = 0.0
        takeoff_future = self.takeoff_client.call_async(takeoff_req)
        while not takeoff_future.done():
            rclpy.spin_once(self)

        for _ in range(5):
            rclpy.spin_once(self)

    def set_home(self):
        req = CommandHome.Request()

        # Altitude a ros topic echo dan bakınca daha yüksek gösteriyor.
        # Galiba zemin seviyesine ekliyor

        req.latitude = self.football.pose.position.latitude
        req.longitude = self.football.pose.position.longitude + 0.001
        req.altitude = self.football.pose.position.altitude- 50
        req.yaw = self.football.pose.orientation.z

        future = self.set_home_client.call_async(req)
        while not future.done():
            rclpy.spin_once(self)
        self.get_logger().info('SET HOME')

    def go_football(self):
        # Kordinat ile
        self.get_logger().info('FOOTBALL')
        for _ in range(500):
            self.setpoint_position_global_publisher.publish(self.football)
            rclpy.spin_once(self, timeout_sec=0.05)

    def take_a_shoot(self):
        # Vector ile hızlandırarak
        self.get_logger().info('SHOOT')
        shoot = Vector3Stamped()

        shoot.vector.x = 0.0
        shoot.vector.y = 50.0
        shoot.vector.z = 0.0

        for _ in range(200):
            self.setpoint_accel_publisher.publish(shoot)
            rclpy.spin_once(self, timeout_sec=0.05) # 200*0.05 = 10 saniye


    def disarm_and_land(self):
        
        land_req = CommandTOL.Request()
        land_req.altitude = 3.0
        land_req.min_pitch = 0.0
        land_req.yaw = 0.0
        future = self.land_client.call_async(land_req)
        while not future.done():
            
            rclpy.spin_once(self)

        disarm_req = CommandBool.Request()
        disarm_req.value = False
        future = self.arm_client.call_async(disarm_req)
        while not future.done():
            
            rclpy.spin_once(self)

    
    def move(self, x, y, z):
        pass

def main(args=None):
    rclpy.init(args=args)
    node = TakeoffNode()
    node.pre_arm()

    #node.set_home() # Take off u bozar

    node.set_guided()
    node.arm_and_takeoff()
    node.go_football()
    node.take_a_shoot()
    node.rtl()
    #node.disarm_and_land()


    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
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
