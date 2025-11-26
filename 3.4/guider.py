

class Guider:
    pass

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