#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.task import Future

from mavros_msgs.msg import State, Waypoint, WaypointList
from mavros_msgs.srv import (
    CommandBool, 
    SetMode, 
    WaypointClear, 
    WaypointPush
)

# MAVLink command IDs
MAV_CMD_NAV_TAKEOFF = 22
MAV_CMD_NAV_LOITER_UNLIM = 17

class ArduPlaneMissionNode(Node):

    def __init__(self):
        super().__init__('arduplane_mission_controller')
        self.get_logger().info('ArduPlane mission controller started')

        # --- Internal State ---
        self.current_state = State()
        self.connection_future = None
        
        # --- Mission Step Control ---
        self.mission_steps = []
        self.current_step_index = 0

        # --- Service Clients ---
        self.arming_client = self.create_client(CommandBool, '/mavros/cmd/arming')
        self.set_mode_client = self.create_client(SetMode, '/mavros/set_mode')
        self.mission_clear_client = self.create_client(WaypointClear, '/mavros/mission/clear')
        self.mission_push_client = self.create_client(WaypointPush, '/mavros/mission/push')

        # --- Subscriber ---
        self.state_sub = self.create_subscription(
            State,
            '/mavros/state',
            self.state_callback,
            10)

        # Start the control logic
        self.start_mission_timer = self.create_timer(1.0, self.start_mission_flow)

    def state_callback(self, msg):
        """Monitors the MAVLink connection state."""
        self.current_state = msg
        if self.connection_future and not self.connection_future.done():
            if self.current_state.connected:
                self.get_logger().info('MAVLink connection established!')
                self.connection_future.set_result(True)

    def start_mission_flow(self):
        """The main control logic flow, started by a timer."""
        self.start_mission_timer.cancel()
        self.get_logger().info('--- Waiting for MAVLink connection ---')
        self.wait_for_connection()

    def wait_for_connection(self):
        """Waits for a MAVLink connection before proceeding."""
        self.connection_future = Future()
        
        if self.current_state.connected:
            self.connection_future.set_result(True)

        self.connection_future.add_done_callback(self.on_connection)

    def on_connection(self, future):
        """
        Callback for connection future.
        This is the main entry point for the mission sequence.
        """
        if not future.result():
            self.get_logger().error('Failed to connect to MAVLink. Stopping.')
            return

        self.get_logger().info('Connection is ready. Configuring mission sequence...')

        # --- 
        # --- FLEXIBLE MISSION SEQUENCE ---
        # ---
        # To change the order of operations, just re-order the list below.
        # Each tuple contains: (function_to_run, "STEP_NAME_FOR_LOGGING")
        #
        # This order matches your request: 1. Arm, 2. Clear, 3. Push, 4. Set Mode
        #
        self.mission_steps = [
            (self.run_step_push_mission, "PUSH_MISSION"),
            (self.run_step_set_auto, "SET_MODE_AUTO"),
            (self.run_step_arm, "ARM"),
        ]
        
        # ---
        # Example: Original order (Clear, Push, Mode, Arm)
        # ---
        # self.mission_steps = [
        #     (self.run_step_clear_mission, "CLEAR_MISSION"),
        #     (self.run_step_push_mission, "PUSH_MISSION"),
        #     (self.run_step_set_auto, "SET_MODE_AUTO"),
        #     (self.run_step_arm, "ARM")
        # ]
        # ---

        self.current_step_index = 0
        self.run_next_step()

    def run_next_step(self):
        """Executes the next step in the mission sequence."""
        if self.current_step_index < len(self.mission_steps):
            step_func, step_name = self.mission_steps[self.current_step_index]
            self.get_logger().info(f"--- Executing Step {self.current_step_index + 1}/{len(self.mission_steps)}: {step_name} ---")
            step_func() # Call the function (e.g., self.run_step_arm())
        else:
            self.get_logger().info("--- Mission Sequence Complete ---")
            # You could add logic here to shut down the node or perform other actions
            # For this example, we'll just log that it's done.

    def on_step_complete(self, future, step_name):
        """
        Universal callback for all service calls.
        Checks for success and triggers the next step.
        """
        try:
            result = future.result()
            
            # Default success check
            success = False

            # Check for success, which varies by service message type
            if hasattr(result, 'success'):
                success = result.success
                if not success:
                    # Specific to CommandBool (arming)
                    self.get_logger().warn(f"'{step_name}' failed with result code: {result.result}")
            elif hasattr(result, 'mode_sent'):
                success = result.mode_sent
            elif hasattr(result, 'wp_transfered'):
                success = result.success # WaypointPush has 'success' and 'wp_transfered'
                if success:
                    self.get_logger().info(f"Successfully transferred {result.wp_transfered} waypoints.")

            if success:
                self.get_logger().info(f"Step '{step_name}' completed successfully.")
                self.current_step_index += 1
                self.run_next_step()
            else:
                self.get_logger().error(f"Step '{step_name}' failed (Result: {result}). Stopping sequence.")

        except Exception as e:
            self.get_logger().error(f"Step '{step_name}' failed with exception: {e}. Stopping sequence.")

    # ---
    # --- INDIVIDUAL STEP FUNCTIONS ---
    # ---

    def run_step_clear_mission(self):
        """Calls the /mavros/mission/clear service."""
        while not self.mission_clear_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Mission clear service not available, waiting...')
        
        req = WaypointClear.Request()
        future = self.mission_clear_client.call_async(req)
        future.add_done_callback(lambda f: self.on_step_complete(f, "CLEAR_MISSION"))

    def run_step_push_mission(self):
        """Creates and pushes a mission with TAKEOFF and then LOITER."""
        self.get_logger().info('Pushing mission: 1. TAKEOFF, 2. LOITER')
        while not self.mission_push_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Mission push service not available, waiting...')

        # --- Waypoint 0: The Takeoff Command ---
        takeoff_wp = Waypoint()
        takeoff_wp.frame = Waypoint.FRAME_GLOBAL_REL_ALT
        takeoff_wp.command = MAV_CMD_NAV_TAKEOFF  # (22)
        takeoff_wp.is_current = True  # Make this the active command
        takeoff_wp.autocontinue = True
        takeoff_wp.param1 = 15.0  # Takeoff pitch angle (degrees)
        takeoff_wp.param2 = 0.0   # Empty
        takeoff_wp.param3 = 0.0   # Empty
        takeoff_wp.param4 = 0.0   # Empty (Yaw)
        takeoff_wp.x_lat = 0.0    # Ignored for takeoff
        takeoff_wp.y_long = 0.0   # Ignored for takeoff
        takeoff_wp.z_alt = 40.0   # Target Altitude (meters)

        # --- Waypoint 1: Loiter Indefinitely ---
        # Loiters at the same altitude as takeoff, at the current location.
        loiter_wp = Waypoint()
        loiter_wp.frame = Waypoint.FRAME_GLOBAL_REL_ALT
        loiter_wp.command = MAV_CMD_NAV_LOITER_UNLIM  # (17)
        loiter_wp.is_current = False
        loiter_wp.autocontinue = True
        loiter_wp.param1 = 0.0   # Ignored (Time)
        loiter_wp.param2 = 0.0   # Ignored (Radius)
        loiter_wp.param3 = 0.0   # Ignored
        loiter_wp.param4 = 0.0   # Ignored (Yaw)
        loiter_wp.x_lat = 0.0    # Ignored (loiter at current location)
        loiter_wp.y_long = 0.0   # Ignored (loiter at current location)
        loiter_wp.z_alt = 40.0   # Target Altitude (meters)

        # Create a mission list and add the waypoints
        mission = WaypointList()
        mission.waypoints.append(takeoff_wp)
        mission.waypoints.append(takeoff_wp)
        mission.waypoints.append(loiter_wp)

        # Create and send the service request
        req = WaypointPush.Request()
        req.start_index = 0
        req.waypoints = mission.waypoints
        
        future = self.mission_push_client.call_async(req)
        future.add_done_callback(lambda f: self.on_step_complete(f, "PUSH_MISSION"))

    def run_step_set_mode(self, mode_name, step_name):
        """Generic function to request a mode change."""
        while not self.set_mode_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Set mode service not available, waiting...')

        req = SetMode.Request()
        req.custom_mode = mode_name
        
        future = self.set_mode_client.call_async(req)
        future.add_done_callback(lambda f: self.on_step_complete(f, step_name))

    def run_step_set_auto(self):
        """Helper function to set AUTO mode."""
        self.run_step_set_mode('AUTO', "SET_MODE_AUTO")

    def run_step_arm(self):
        """Requests to arm the vehicle."""
        self.get_logger().info('Arming vehicle...')
        while not self.arming_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Arming service not available, waiting...')

        req = CommandBool.Request()
        req.value = True
        
        future = self.arming_client.call_async(req)
        future.add_done_callback(lambda f: self.on_step_complete(f, "ARM"))


def main(args=None):
    rclpy.init(args=args)
    node = ArduPlaneMissionNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Node shutting down.')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()