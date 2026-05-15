import time
import dronekit
from dronekit import mavutil
from dronekit import VehicleMode
class uav():

    def __init__(self, connection_string, baudrate, heartbeat_timeout):
        print("initalize uav")
        print("connecting vehicle ... ")
        self.vhc = dronekit.connect(connection_string, baud = baudrate, heartbeat_timeout = heartbeat_timeout)
        print(self.vhc.mode.name)
        print("connected vehicle")
    
    def prearmCheck(self):
        print("Basic pre-arm checks")
        # Don't try to arm until autopilot is ready
        i = 0
        while not self.vhc.is_armable:
            i = i + 1
            print(" Waiting for vehicle to initialise...")
            time.sleep(1)
            if i >= 3:
                print("prearm check timeout (90s)")
                return 1
        print("Ready to Arm")
        return 0
    def armThrottle(self):
        print("Arming Motors")
        self.vhc.mode    = VehicleMode("GUIDED")
        self.vhc.armed   = True
        while not self.vhc.armed:
            print(" Waiting for arming...")
            time.sleep(0.5)
        print("Motors Armed")
        print("Taking off!")
    
    def takeoff(self, target_altitude):
        print("taking off")
        self.vhc.simple_takeoff(target_altitude) # Take off to target altitude

    def printStatus(self):
        print("System status : ", str(self.vhc.system_status.state))
        print("Battery : ", str(self.vhc.battery))
        print("Gps : ", str(self.vhc.gps_0))
        print("Last heartbeat : ", str(self.vhc.last_heartbeat))
        print("Mode : ", str(self.vhc.mode.name))

    def set_velocity_body(vehicle, vx, vy, vz):
        """ Remember: vz is positive downward!!!
        http://ardupilot.org/dev/docs/copter-commands-in-guided-mode.html
        
        Bitmask to indicate which dimensions should be ignored by the vehicle 
        (a value of 0b0000000000000000 or 0b0000001000000000 indicates that 
        none of the setpoint dimensions should be ignored). Mapping: 
        bit 1: x,  bit 2: y,  bit 3: z, 
        bit 4: vx, bit 5: vy, bit 6: vz, 
        bit 7: ax, bit 8: ay, bit 9:
        
        
        """
        msg = vehicle.message_factory.set_position_target_local_ned_encode(
                0,
                0, 0,
                mavutil.mavlink.MAV_FRAME_BODY_NED,
                0b0000111111000111, #-- BITMASK -> Consider only the velocities
                0, 0, 0,        #-- POSITION
                vx, vy, vz,     #-- VELOCITY
                0, 0, 0,        #-- ACCELERATIONS
                0, 0)
        vehicle.send_mavlink(msg)
        vehicle.flush()
    
    def setMultiplier(self, dis_pos_ref, Kp_pos, Kp_vel, Ki_vel, Upi_max):
        self.dis_pos_ref = dis_pos_ref
        self.Kp_pos = Kp_pos
        self.Kp_vel = Kp_vel
        self.Ki_vel = Ki_vel
        self.Ui_vel_integ_x = 0
        self.Ui_vel_integ_y = 0
        self.Upi_max = Upi_max
        
    def trackCoordinates(self, coor_array, resolution):
        #self.vhc.location.global_frame.alt
        if len(coor_array) < 4: return 2
        temp = (0.54630248984 * 1 * 2) / resolution[0]
        mid_pointer_x = (coor_array[0][0] + coor_array[2][0]) / 2
        mid_pointer_y = (coor_array[0][1] + coor_array[2][1]) / 2
        distance_x = (resolution[0] / 2) - mid_pointer_x
        distance_y = (resolution[1] / 2) - mid_pointer_y
        distance_real_y = distance_x * temp
        distance_real_x = distance_y * temp
        vel_x = self.vhc.velocity[1]
        error_x = self.dis_pos_ref - distance_real_x
        Upos_px = self.Kp_pos * error_x
        error_tvx = Upos_px - vel_x
        Up_vel_x = self.Kp_vel * error_tvx
        Ui_vel_x = (self.Ki_vel * error_tvx) + self.Ui_vel_integ_x
        Upi_vel_x = Up_vel_x + Ui_vel_x
        if Upi_vel_x > self.Upi_max:Upi_vel_x = self.Upi_max
        if Upi_vel_x < -1 * self.Upi_max: Upi_vel_x = self.Upi_max * -1
        velocity_x = Upi_vel_x
        self.Ui_vel_integ_x = Ui_vel_x

        vel_y = self.vhc.velocity[2]
        error_y = self.dis_pos_ref - distance_real_y
        Upos_py = self.Kp_pos * error_y
        error_tvy = Upos_py - vel_y
        Up_vel_y = self.Kp_vel * error_tvy
        Ui_vel_y = (self.Ki_vel * error_tvy) + self.Ui_vel_integ_y
        Upi_vel_y = Up_vel_y + Ui_vel_y
        if Upi_vel_y > self.Upi_max:Upi_vel_y = self.Upi_max
        if Upi_vel_y < -1 * self.Upi_max: Upi_vel_y = self.Upi_max * -1
        velocity_y = Upi_vel_y
        self.Ui_vel_integ_y = Ui_vel_y
        

        print(" x velocity : " + str(velocity_x) + " y velocity : " + str(velocity_y))

        #if self.vhc.location.global_frame.alt <= 0: return 0
        return 2
