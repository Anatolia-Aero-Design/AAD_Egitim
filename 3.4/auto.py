MAV_CMD_NAV_WAYPOINT = 16
MAV_CMD_NAV_LOITER_UNLIM = 17
MAV_CMD_NAV_RETURN_TO_LAUNCH = 20
MAV_CMD_NAV_LAND = 21
MAV_CMD_NAV_TAKEOFF = 22
MAV_CMD_DO_SET_MODE = 176


class Auto:
    def __init__(self, logger, clear_mission, push_mission):
        self.logger = logger
        self.clear_mission = clear_mission
        self.push_mission = push_mission

        self.mission_len = -1
        self.missions = {
            "Takeoff": self.takeoff_mission  
        }

    def execute(self, order, param=None):
        try:
            mission = self.missions[order](param)
            self.mission_len = len(mission)
            self.push_mission(mission)

        except KeyError:
            print("Auto, execute | Order doesnt exist...")

    def mission_callback(self, msg):
        if msg.wp_seq == self.mission_len:
            self.on_mission_end()
     


"""
def run_step_clear_mission(self, step_name):
        /mavros/mission/clear servisini çağirir.
        self.get_logger().info("Mevcut görev temizleniyor...")
        while not self.mission_clear_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Görev temizleme servisi bekleniyor...')
        
        req = WaypointClear.Request()
        future = self.mission_clear_client.call_async(req)
        future.add_done_callback(lambda f: self.on_step_complete(f, step_name))

    def run_step_push_mission(self, step_name):
        Kalkiş, Navigasyon ve GUIDED'a geçiş görevini basar.
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
"""