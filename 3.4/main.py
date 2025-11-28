#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy

from mavros_msgs.msg import State, WaypointReached, AttitudeTarget
from mavros_msgs.srv import CommandBool, SetMode, WaypointClear, WaypointPush
from geometry_msgs.msg import Pose, PoseStamped

from decorators import service_caller
from stepper import Stepper
from guider import Guider
from auto import Auto

class ArduPlaneMissionNode(Node):

    def __init__(self):
        super().__init__('arduplane_mission_controller')
        self.get_logger().info('ArduPlane Görev ve Vektör Kontrolcüsü Başlatildi')

        # --- Flags ---
        self.state = State()
        self.pose = Pose()

        # --- Qos ---
        qos_pose = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )

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
        self.pose_sub = self.create_subscription(PoseStamped, '/mavros/local_position/pose', self.pose_callback, qos_pose)

        # --- Helper Objects ---
        self.stepper = Stepper(self.get_logger, self.step)
        self.auto = Auto(self.get_logger, self.step, self.clear_mission ,self.push_mission)
        #self.guider = Guider(self.get_logger, self.step)

        # --- Steps ---
        self.stepper.assign_steps([
            (lambda: self.arm(True), "Arm"),
            (lambda: self.auto.execute("takeoff"), "Takeoff"),
            (lambda: self.set_mode('AUTO'), "Auto")
        ])

        # Start the control logic
        self.timer = self.create_timer(1.0, self.start_mission_flow)

    # --- Mission Flow ---
    def start_mission_flow(self):
        self.stepper.start_mission_flow(self.timer)

    def on_step_end(self):
        self.stepper.step()

    # --- Callbacks ---
    def state_callback(self, msg):
        self.state = msg

    def mission_callback(self, msg):
        self.auto.mission_callback(msg)

    def pose_callback(self, msg):
        self.pose = msg.pose
 
    # --- Clients ---
    @service_caller
    def set_mode(self, mode_name):
        """Modu değiştirir (AUTO, LAND, RTL, GUIDED vb.)"""
        req = SetMode.Request()
        req.custom_mode = mode_name
        
        return self.set_mode_client, req

    @service_caller
    def arm(self, bool_val):
        """bool_val a bağli olarak arm veya disarm der"""
        req = CommandBool.Request()
        req.value = bool_val
        
        return self.arming_client, req
    
    @service_caller
    def clear_mission(self):
        """Görev listesini temizler"""
        req = WaypointClear.Request()
        
        return self.mission_clear_client, req
    
    @service_caller
    def push_mission(self, mission):
        """Görev listesini atar"""
        req = WaypointPush.Request()
        req.waypoints = mission.waypoints

        return self.mission_push_client, req
        
    
    # --- Helper Communication ---
    def step(self):
        self.stepper.step()

    def on_service_call(self, future):
        self.stepper.step()


# --- Main ---
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