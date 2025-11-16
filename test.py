#!/usr/bin/env python3
import math
import rclpy
from rclpy.node import Node
from rclpy.task import Future

from mavros_msgs.msg import State, Waypoint, WaypointList, WaypointReached
from geometry_msgs.msg import Twist  # <-- VEKTÖR KONTROLÜ İÇİN EKLENDİ
from mavros_msgs.srv import (
    CommandBool, 
    SetMode, 
    WaypointClear, 
    WaypointPush
)

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
        self.get_logger().info('ArduPlane Görev ve Vektör Kontrolcüsü Başlatıldı')

        # --- Internal State ---
        self.current_state = State()
        self.connection_future = None
        self.mode = None
        self.is_guiding = False       # GUIDED modda olup olmadığımızı takip eden bayrak
        self.control_timer = None     # Vektör kontrol döngüsü zamanlayıcısı
        self.target_velocity = Twist()  # Gönderilecek hız vektörü
        
        # --- Mission Step Control ---
        self.mission_steps = []
        self.current_step_index = 0

        # --- Service Clients ---
        self.arming_client = self.create_client(CommandBool, '/mavros/cmd/arming')
        self.set_mode_client = self.create_client(SetMode, '/mavros/set_mode')
        self.mission_clear_client = self.create_client(WaypointClear, '/mavros/mission/clear')
        self.mission_push_client = self.create_client(WaypointPush, '/mavros/mission/push')

        # --- Yayıncılar (Publishers) ---
        self.velocity_pub = self.create_publisher(
            Twist,
            '/mavros/setpoint_velocity/cmd_vel_unstamped',
            10)

        # --- Subscriber ---
        self.state_sub = self.create_subscription(
            State,
            '/mavros/state',
            self.state_callback,
            10)
        self.mission_sub = self.create_subscription(
            WaypointReached,
            '/mavros/mission/reached',
            self.mission_callback,
            10
        )

        # Start the control logic
        self.start_mission_timer = self.create_timer(1.0, self.start_mission_flow)

    def state_callback(self, msg):
        """MAVLink durumunu izler ve mod geçişlerini yönetir."""
        
        # --- KRİTİK HATA DÜZELTMESİ ---
        # self.current_state = msg, (sondaki virgül) bir tuple oluşturuyordu.
        self.current_state = msg
        self.mode = msg.mode
        # --- BİTTİ ---

        if self.connection_future and not self.connection_future.done():
            # 'connected' özelliği State mesajının bir parçasıdır
            if self.current_state.connected:
                self.get_logger().info('MAVLink connection established!')
                self.connection_future.set_result(True)

        # Ana mod değiştirme mantığı
        if self.mode == 'GUIDED' and not self.is_guiding:
            # GUIDED moda YENİ GİRDİK
            self.is_guiding = True
            self.get_logger().info("GUIDED mod algılandı! Vektör kontrolü başlıyor...")
            self.start_vector_control()
        elif self.mode != 'GUIDED' and self.is_guiding:
            # GUIDED moddan YENİ ÇIKTIK (Güvenlik)
            self.is_guiding = False
            self.get_logger().warn("GUIDED moddan çıkıldı! Vektör kontrolü durduruluyor.")
            self.stop_vector_control()

    def mission_callback(self, msg):
        if msg.wp_seq == 2:
            self.run_step_set_mode("GUIDED", "SET MODE GUIDED") 

    def start_mission_flow(self):
        """Ana kontrol mantığı akışı, bir zamanlayıcı tarafından başlatılır."""
        self.start_mission_timer.cancel()
        self.get_logger().info('--- MAVLink bağlantısı bekleniyor ---')
        self.wait_for_connection()

    def wait_for_connection(self):
        """Devam etmeden önce bir MAVLink bağlantısı bekler."""
        self.connection_future = Future()
        
        # current_state'in henüz ayarlanmamış olma ihtimaline karşı kontrol
        if self.current_state and self.current_state.connected:
            self.connection_future.set_result(True)

        self.connection_future.add_done_callback(self.on_connection)

    def on_connection(self, future):
        """Bağlantı 'future'ı için callback."""
        if not future.result():
            self.get_logger().error('MAVLink bağlantısı kurulamadı. Duruluyor.')
            return

        self.get_logger().info('Bağlantı hazır. Görev dizisi yapılandırılıyor...')

        # --- 
        # --- GÖREV DEVRİ (HAND-OFF) DİZİSİ ---
        # ---
        self.mission_steps = [
            lambda: self.run_step_clear_mission("CLEAR_MISSION"), # Önce temizle
            lambda: self.run_step_push_mission("PUSH_MISSION"),  # Görevi (GUIDED'a geçiş dahil) yükle
            lambda: self.run_step_set_mode('AUTO', "SET_MODE_AUTO"), # AUTO modu başlat
            lambda: self.run_step_arm("ARM"),                    # Aracı arm et
        ]
        
        self.current_step_index = 0
        self.run_next_step()

    def run_next_step(self):
        """Görev dizisindeki bir sonraki adımı yürütür."""
        if self.current_step_index < len(self.mission_steps):
            self.get_logger().info(f"--- Adım {self.current_step_index + 1}/{len(self.mission_steps)} yürütülüyor ---")
            step_func = self.mission_steps[self.current_step_index]
            step_func()
        else:
            self.get_logger().info("--- Görev Kurulumu Tamamlandı ---")
            self.get_logger().info("Araç AUTO modda. GUIDED moda geçiş (görev devri) bekleniyor...")
            # Kurulum bitti, şimdi state_callback'in devralmasını bekliyoruz.

    def on_step_complete(self, future, step_name):
        """Tüm servis çağrıları için evrensel callback."""
        try:
            result = future.result()
            success = False

            if hasattr(result, 'success'):
                success = result.success
                if not success and hasattr(result, 'result'):
                    self.get_logger().warn(f"'{step_name}' başarısız oldu, sonuç kodu: {result.result}")
            elif hasattr(result, 'mode_sent'):
                success = result.mode_sent
            elif hasattr(result, 'wp_transfered'):
                success = result.success
                if success:
                    self.get_logger().info(f"Başarıyla {result.wp_transfered} yol noktası aktarıldı.")

            if success:
                self.get_logger().info(f"Adım '{step_name}' başarıyla tamamlandı.")
                self.current_step_index += 1
                self.run_next_step()
            else:
                self.get_logger().error(f"Adım '{step_name}' başarısız (Sonuç: {result}). Dizi durduruluyor.")

        except Exception as e:
            self.get_logger().error(f"Adım '{step_name}' istisna ile başarısız oldu: {e}. Dizi durduruluyor.")

    # ---
    # --- GÖREV ADIMI FONKSİYONLARI ---
    # ---

    def run_step_clear_mission(self, step_name):
        """/mavros/mission/clear servisini çağırır."""
        self.get_logger().info("Mevcut görev temizleniyor...")
        while not self.mission_clear_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Görev temizleme servisi bekleniyor...')
        
        req = WaypointClear.Request()
        future = self.mission_clear_client.call_async(req)
        future.add_done_callback(lambda f: self.on_step_complete(f, step_name))

    def run_step_push_mission(self, step_name):
        """Kalkış, Navigasyon ve GUIDED'a geçiş görevini basar."""
        self.get_logger().info('Görev basılıyor: 1. TAKEOFF, 2. NAV_WP, 3. SET_GUIDED')
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

        # "İlkini atlama" hatasını düzeltmek için takeoff'u çiftle
        mission = WaypointList()
        mission.waypoints.append(takeoff_wp) # 0 (Yedek)
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
        self.get_logger().info(f"Mod {mode_name} olarak ayarlanıyor...")
        while not self.set_mode_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Mod servisi bekleniyor...')

        req = SetMode.Request()
        req.custom_mode = mode_name
        
        future = self.set_mode_client.call_async(req)
        future.add_done_callback(lambda f: self.on_step_complete(f, step_name))

    def run_step_arm(self, step_name):
        """Aracı arm etme talebi gönderir."""
        self.get_logger().info('Araç arm ediliyor...')
        while not self.arming_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Arm servisi bekleniyor...')

        req = CommandBool.Request()
        req.value = True
        
        future = self.arming_client.call_async(req)
        future.add_done_callback(lambda f: self.on_step_complete(f, step_name))

    # ---
    # --- VEKTÖR KONTROL FONKSİYONLARI ---
    # ---

    def set_target_flight_vector(self):
        """Uçağın takip edeceği hız vektörünü ayarlar."""
        # linear.x: İLERİ HIZ (m/s). ASLA STALL HIZININ ALTINA DÜŞME!
        self.target_velocity.linear.x = 10.0  # 20 m/s ileri hız

        # linear.z: DİKEY HIZ (m/s). Pozitif = Tırman
        self.target_velocity.linear.z = 0.0   # Düz uçuş

        # angular.z: DÖNÜŞ HIZI (rad/s). Pozitif = Sola
        self.target_velocity.angular.z = 0.0  # Hafif sola dönüş (daire çiz)

    def start_vector_control(self):
        """Vektör kontrol zamanlayıcısını başlatır."""
        # Hedef vektörü ayarla (değiştirmek isterseniz burada yapın)
        self.set_target_flight_vector()
        
        # Saniyede 5 kez (5Hz) çalışan kontrol döngüsünü başlat
        if self.control_timer is None:
            self.control_timer = self.create_timer(0.2, self.vector_control_loop)
            self.get_logger().info("Vektör kontrol döngüsü (5Hz) başlatıldı.")

    def stop_vector_control(self):
        """Vektör kontrol zamanlayıcısını durdurur."""
        if self.control_timer is not None:
            self.control_timer.cancel()
            self.control_timer = None
            self.get_logger().info("Vektör kontrol döngüsü durduruldu.")

    def vector_control_loop(self):
        """
        Sürekli çalışan ana kontrol döngüsü.
        Sadece hedef hız vektörünü yayınlar.
        """
        # (İsteğe bağlı: Vektörü burada anlık olarak güncelleyebilirsiniz)
        #self.target_velocity.linear.x += 0.1 * math.sin(self.get_clock().now().nanoseconds / 1e7)
        print("test")
        self.velocity_pub.publish(self.target_velocity)


def main(args=None):
    rclpy.init(args=args)
    node = ArduPlaneMissionNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Düğüm kapatılıyor.')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()