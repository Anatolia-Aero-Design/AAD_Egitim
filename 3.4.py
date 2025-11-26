#!/usr/bin/env python3
import math
import rclpy
from rclpy.node import Node
from rclpy.task import Future
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy

from mavros_msgs.msg import State, Waypoint, WaypointList, WaypointReached, AttitudeTarget
from mavros_msgs.srv import CommandBool, SetMode, WaypointClear, WaypointPush
from geometry_msgs.msg import Pose, PoseStamped
from geographic_msgs.msg import GeoPoseStamped

# MAVLink command IDs
MAV_CMD_NAV_WAYPOINT = 16
MAV_CMD_NAV_LOITER_UNLIM = 17
MAV_CMD_NAV_RETURN_TO_LAUNCH = 20
MAV_CMD_NAV_LAND = 21
MAV_CMD_NAV_TAKEOFF = 22
MAV_CMD_DO_SET_MODE = 176

class ArduPlaneMissionNode(Node):

    def __init__(self):
        super().__init__('arduplane_mission_controller')
        self.get_logger().info('ArduPlane Görev ve Vektör Kontrolcüsü Başlatildi')

        # --- Internal State ---
        self.current_state = State()
        self.connection_future = None
        self.mode = None
        self.is_guiding = False       # GUIDED modda olup olmadiğimizi takip eden bayrak
        self.control_timer = None     # Vektör kontrol döngüsü zamanlayicisi
        self.pose = Pose()
        self.target = GeoPoseStamped()

        # --- Mission Step Control ---
        self.mission_steps = []
        self.current_step_index = 0

        # --- Görev 1 ---
        self.stick1 = Pose()
        self.stick1.position.x = -115.0
        self.stick1.position.y = -62.0
        self.stick2 = Pose()
        self.stick2.position.x = -125.0
        self.stick2.position.y = -72.0


        # --- Service Clients ---
        self.arming_client = self.create_client(CommandBool, '/mavros/cmd/arming')
        self.set_mode_client = self.create_client(SetMode, '/mavros/set_mode')
        self.mission_clear_client = self.create_client(WaypointClear, '/mavros/mission/clear')
        self.mission_push_client = self.create_client(WaypointPush, '/mavros/mission/push')

        # --- Yayincilar (Publishers) ---
        self.setpoint_position_local_pub = self.create_publisher(PoseStamped, '/mavros/setpoint_position/local', 10)
        self.att_target_publisher = self.create_publisher(AttitudeTarget, '/mavros/setpoint_raw/attitude', 10)

        # --- Subscriber ---
        self.state_sub = self.create_subscription(State, '/mavros/state', self.state_callback, 10)
        self.mission_sub = self.create_subscription(WaypointReached, '/mavros/mission/reached', self.mission_callback, 10)
        # Best Effort QoS profili oluştur
        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )

        self.pose_sub = self.create_subscription(
            PoseStamped, 
            '/mavros/local_position/pose', 
            self.pose_callback, 
            qos_profile
        )

        # Start the control logic
        self.start_mission_timer = self.create_timer(1.0, self.start_mission_flow)

    def state_callback(self, msg):
        """MAVLink durumunu izler ve mod geçişlerini yönetir."""
    
        self.current_state = msg
        self.mode = msg.mode

        if self.connection_future and not self.connection_future.done():
            # 'connected' özelliği State mesajinin bir parçasidir
            if self.current_state.connected:
                self.get_logger().info('MAVLink connection established!')
                self.connection_future.set_result(True)

        # Ana mod değiştirme mantiği
        if self.mode == 'GUIDED' and not self.is_guiding:
            # GUIDED moda YENİ GİRDİK
            self.is_guiding = True
            self.get_logger().info("GUIDED mod algilandi! Vektör kontrolü başliyor...")
            self.start_control()
        elif self.mode != 'GUIDED' and self.is_guiding:
            # GUIDED moddan YENİ ÇIKTIK (Güvenlik)
            self.is_guiding = False
            self.get_logger().warn("GUIDED moddan çikildi! Vektör kontrolü durduruluyor.")
            self.stop_control()

    def mission_callback(self, msg):
        if msg.wp_seq == 2:
            self.run_step_set_mode("GUIDED", "SET MODE GUIDED") 

    def pose_callback(self, msg):
        self.pose = msg.pose

    def start_mission_flow(self):
        """Ana kontrol mantiği akişi, bir zamanlayici tarafindan başlatilir."""
        self.start_mission_timer.cancel()
        self.get_logger().info('--- MAVLink bağlantisi bekleniyor ---')
        self.wait_for_connection()

    def wait_for_connection(self):
        """Devam etmeden önce bir MAVLink bağlantisi bekler."""
        self.connection_future = Future()
        
        # current_state'in henüz ayarlanmamiş olma ihtimaline karşi kontrol
        if self.current_state and self.current_state.connected:
            self.connection_future.set_result(True)

        self.connection_future.add_done_callback(self.on_connection)

    def on_connection(self, future):
        """Bağlanti 'future'i için callback."""
        if not future.result():
            self.get_logger().error('MAVLink bağlantisi kurulamadi. Duruluyor.')
            return

        self.get_logger().info('Bağlanti hazir. Görev dizisi yapilandiriliyor...')

        # --- 
        # --- GÖREV DEVRİ (HAND-OFF) DİZİSİ ---
        # ---
        self.mission_steps = [
            lambda: self.run_step_arm("ARM"),                           # Araci arm et
            lambda: self.run_step_clear_mission("CLEAR_MISSION"),       # Önce temizle
            lambda: self.run_step_push_mission("PUSH_MISSION"),         # Görevi (GUIDED'a geçiş dahil) yükle
            lambda: self.run_step_set_mode('AUTO', "SET_MODE_AUTO"),    # AUTO modu başlat
        ]
        
        self.current_step_index = 0
        self.run_next_step()

    def run_next_step(self):
        """Görev dizisindeki bir sonraki adimi yürütür."""
        if self.current_step_index < len(self.mission_steps):
            self.get_logger().info(f"--- Adim {self.current_step_index + 1}/{len(self.mission_steps)} yürütülüyor ---")
            step_func = self.mission_steps[self.current_step_index]
            step_func()
        else:
            self.get_logger().info("--- Görev Kurulumu Tamamlandi ---")
            # Kurulum bitti, şimdi state_callback'in devralmasini bekliyoruz.

    def on_step_complete(self, future, step_name):
        """Tüm servis çağrilari için evrensel callback."""
        try:
            result = future.result()
            success = False

            if hasattr(result, 'success'):
                success = result.success
                if not success and hasattr(result, 'result'):
                    self.get_logger().warn(f"'{step_name}' başarisiz oldu, sonuç kodu: {result.result}")
            elif hasattr(result, 'mode_sent'):
                success = result.mode_sent
            elif hasattr(result, 'wp_transfered'):
                success = result.success
                if success:
                    self.get_logger().info(f"Başariyla {result.wp_transfered} yol noktasi aktarildi.")

            if success:
                self.get_logger().info(f"Adim '{step_name}' başariyla tamamlandi.")
                self.current_step_index += 1
                self.run_next_step()
            else:
                self.get_logger().error(f"Adim '{step_name}' başarisiz (Sonuç: {result}). Dizi durduruluyor.")

        except Exception as e:
            self.get_logger().error(f"Adim '{step_name}' istisna ile başarisiz oldu: {e}. Dizi durduruluyor.")

    # ---
    # --- GÖREV ADIMI FONKSİYONLARI ---
    # ---

    def run_step_clear_mission(self, step_name):
        """/mavros/mission/clear servisini çağirir."""
        self.get_logger().info("Mevcut görev temizleniyor...")
        while not self.mission_clear_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Görev temizleme servisi bekleniyor...')
        
        req = WaypointClear.Request()
        future = self.mission_clear_client.call_async(req)
        future.add_done_callback(lambda f: self.on_step_complete(f, step_name))

    def run_step_push_mission(self, step_name):
        """Kalkiş, Navigasyon ve GUIDED'a geçiş görevini basar."""
        self.get_logger().info('Görev basiliyor: 1. TAKEOFF, 2. NAV_WP, 3. SET_GUIDED')
        while not self.mission_push_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Görev basma servisi bekleniyor...')

        # --- Waypoint 0: The Takeoff Command ---
        takeoff_wp = Waypoint()
        takeoff_wp.frame = Waypoint.FRAME_GLOBAL_REL_ALT
        takeoff_wp.command = MAV_CMD_NAV_TAKEOFF
        takeoff_wp.is_current = True
        takeoff_wp.autocontinue = True
        takeoff_wp.param1 = 15.0 
        takeoff_wp.z_alt = 40.0 

        # --- Waypoint 1: Navigation Waypoint ---
        nav_wp = Waypoint()
        nav_wp.frame = Waypoint.FRAME_GLOBAL_REL_ALT
        nav_wp.command = MAV_CMD_NAV_WAYPOINT
        nav_wp.is_current = False
        nav_wp.autocontinue = True
        nav_wp.x_lat = 39.819338
        nav_wp.y_long = 30.530890
        nav_wp.z_alt = 40.0  

        rtl_wp = Waypoint()
        rtl_wp.frame = Waypoint.FRAME_GLOBAL_REL_ALT
        rtl_wp.command = MAV_CMD_NAV_RETURN_TO_LAUNCH

        land_wp = Waypoint()
        land_wp.frame = Waypoint.FRAME_GLOBAL_REL_ALT
        land_wp.command = MAV_CMD_NAV_LAND

        mission = WaypointList()
        mission.waypoints.append(takeoff_wp) # 0
        mission.waypoints.append(takeoff_wp) # 1
        mission.waypoints.append(nav_wp)     # 2
        #mission.waypoints.append(rtl_wp)     # 2
        #mission.waypoints.append(land_wp)     # 2        

        req = WaypointPush.Request()
        req.start_index = 0
        req.waypoints = mission.waypoints
        
        future = self.mission_push_client.call_async(req)
        future.add_done_callback(lambda f: self.on_step_complete(f, step_name))

    def run_step_set_mode(self, mode_name, step_name):
        """Mod değiştirme talebi için genel fonksiyon."""
        self.get_logger().info(f"Mod {mode_name} olarak ayarlaniyor...")
        while not self.set_mode_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Mod servisi bekleniyor...')

        req = SetMode.Request()
        req.custom_mode = mode_name
        
        future = self.set_mode_client.call_async(req)
        future.add_done_callback(lambda f: self.on_step_complete(f, step_name))

    def run_step_arm(self, step_name):
        """Araci arm etme talebi gönderir."""
        self.get_logger().info('Araç arm ediliyor...')
        while not self.arming_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Arm servisi bekleniyor...')

        req = CommandBool.Request()
        req.value = True
        
        future = self.arming_client.call_async(req)
        future.add_done_callback(lambda f: self.on_step_complete(f, step_name))

    # ---
    # --- KONTROL FONKSİYONLARI ---
    # ---

    def euler_to_quaternion(self, roll, pitch, yaw):
        """
        Euler açılarını (radyan) Quaternion'a (x, y, z, w) çevirir.
        """
        qx = math.sin(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) - math.cos(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)
        qy = math.cos(roll/2) * math.sin(pitch/2) * math.cos(yaw/2) + math.sin(roll/2) * math.cos(pitch/2) * math.sin(yaw/2)
        qz = math.cos(roll/2) * math.cos(pitch/2) * math.sin(yaw/2) - math.sin(roll/2) * math.sin(pitch/2) * math.cos(yaw/2)
        qw = math.cos(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) + math.sin(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)
        return [qx, qy, qz, qw]

    def start_control(self):
        if self.control_timer is None:
            self.control_timer = self.create_timer(0.2, self.control_loop)
            self.get_logger().info("Kontrol döngüsü (5Hz) başlatildi.")

    def stop_control(self):
        if self.control_timer is not None:
            self.control_timer.cancel()
            self.control_timer = None
            self.get_logger().info("Kontrol döngüsü durduruldu.")

    def distance(x1,x2,y1,y2):
        return math.sqrt((x1-x2)**2 + (y1-y2)**2)

    def teget_noktalari_bul(self, m1, m2, r, d, dx, dy):
        
        # Nokta çemberin içindeyse çözüm yoktur
        if d < r:
            return None 
        
        # 2. Merkezden noktaya giden açıyı bul (theta)
        theta = math.atan2(dy, dx)
        
        # 3. Sapma açısını bul (alpha)
        # Dik üçgen bağıntısı: cos(alpha) = r / d
        alpha = math.acos(r / d)
        
        # 4. İki teğet noktasını hesapla
        # Nokta 1 (Pozitif yönlü sapma)
        t1_x = m1 + r * math.cos(theta + alpha)
        t1_y = m2 + r * math.sin(theta + alpha)
        
        # Nokta 2 (Negatif yönlü sapma)
        t2_x = m1 + r * math.cos(theta - alpha)
        t2_y = m2 + r * math.sin(theta - alpha)
        
        return ((t1_x, t1_y), (t2_x, t2_y))

    def control_loop(self):
                
        x_to_s1 = self.pose.position.x - self.stick1.position.x
        y_to_s1 = self.pose.position.y - self.stick1.position.y
        x_to_s2 = self.pose.position.x - self.stick2.position.x
        y_to_s2 = self.pose.position.y - self.stick2.position.y

        dist_s1 = math.sqrt(x_to_s1**2 + y_to_s1**2)
        dist_s2 = math.sqrt(x_to_s2**2 + y_to_s2**2)

        r = math.fabs((dist_s1 - dist_s2)/2)    

        if min(dist_s1, dist_s2) > r + 10:
            # Önce teğete git
            if dist_s1 < dist_s2:
                m1 = self.stick1.position.x
                m2 = self.stick1.position.y
                d = dist_s1
                dx = x_to_s1
                dy = y_to_s1
            else:
                m1 = self.stick2.position.x
                m2 = self.stick2.position.y
                d = dist_s2
                dx = x_to_s2
                dy = y_to_s2

            e = self.teget_noktalari_bul(m1, m2, r, d, dx, dy)[0]

            msg = PoseStamped()
            msg.pose.position.x = e[0] - self.pose.position.x
            msg.pose.position.y = e[1] - self.pose.position.y
            msg.pose.position.z = self.pose.position.z
            msg.pose.orientation.w = 1.0
            self.setpoint_position_local_pub.publish(msg)

            print(d)
            return

        # HEDEF AÇILAR
        msg = AttitudeTarget()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = "base_link"
        msg.type_mask = 7
        
        roll = math.radians(-20.0)  # 20 derece sağa yatış (Pozitif = Sağ Bank)
        pitch = math.radians(0.0)  # Burun düz
        yaw = math.radians(0.0)    # (Mevcut yönü korumak için yaw kontrolü daha karmaşıktır, burada 0 referans alınır)

        q = self.euler_to_quaternion(roll, pitch, yaw)
        msg.orientation.x = q[0]
        msg.orientation.y = q[1]
        msg.orientation.z = q[2]
        msg.orientation.w = q[3]
        msg.thrust = 1.0

        self.att_target_publisher.publish(msg)
        print("target")
        


def main(args=None):
    rclpy.init(args=args)
    node = ArduPlaneMissionNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Düğüm kapatiliyor.')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()