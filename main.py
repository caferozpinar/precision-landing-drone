#import dronekit
import cam
import shapeFinder
import motion_control

stage = 0                                                                                                                                       # Starting stages number (0-5)
logging_file = open("last_log.txt")


###################### INITALIZE STAGE VALUES ######################
camera_threshold = (0, 0, 120), (179, 120, 255)                                                                                                 # Camera's blob detection threshold values (setted up for white blobs)
finder_threshold = (10.0, 3.0, 2.0)                                                                                                             # finder's filter threshold values (lower the values for high accuracy)
rpi_camera_on = 1                                                                                                                               # For opening Raspberry pi camera
connect_vehicle = 1                                                                                                                             # For enabling mavlink vehicle communication
connection_string = "/dev/ttyAMA0"                                                                                                              # Vehicle's serial communication port
connection_baudrate = 115200                                                                                                                    # Vehicle's serial baudrates
connection_timeout = 180                                                                                                                        # Serial connection timeout (s)
shape = "Tshape"                                                                                                                                # Define pointers shape
###################### INITALIZE STAGE VALUES ######################

###################### INITALIZE QUEST VALUES ######################
arm_and_takeoff = 1
###################### INITALIZE QUEST VALUES ######################

if __name__ == "__main__":

    ################################################################################### STAGE 0 INITALIZE ###################################################################################
    if stage == 0: # Stage 0 initalize stage, initalize Camera, Blob detector, Shapefinder and Mavlink communication 
        # start camera
        if rpi_camera_on:
            try:
                camera = cam.colorDetect()                                                                                                      # Create a camera object
                camera.captureCam(0)                                                                                                            # Capture camera source
                camera.setThreshold(camera_threshold[0], camera_threshold[1])                                                                   # Set camera detection threshold
            except Exception as error:
                print(error)
                print("Camera Initalise Error. Exiting The Script...")

        # start shape finder                                                
        if shape == "Tshape":                                               
            try:
                Tfinder = shapeFinder.TFinder                                                                                                   # Create a Tfinder object
                Tfinder.setThreshold(finder_threshold[0], finder_threshold[1], finder_threshold[2])                                             # Set Tfinder Threshold
            except Exception as error:
                print(error)
                print("Tfinder Initalize Error. Exiting The Script...")

        if shape == "triangle":
            print("no triangle function defined")

        if connect_vehicle:
            try:
                vhc_controller = motion_control.uav(connection_string, baudrate = connection_baudrate, heartbeat_timeout = connection_timeout)  # Connect Mavlink With Given Port/Baudrate/Timeout
                vhc_controller.printStatus()                                                                                                    # Print Connected Mavlink Status
                vhc_controller.setGainValues() # the new version of the self.setMultiplier()                                                    # Set Controlled Vehicle Gain Values Kp/Kd/Ki
            except Exception as error:
                print(error)
                print("Failed While Connecting : {connection_string}. Exiting The Script...")
        
        stage = 1
    ################################################################################### STAGE 0 INITALIZE ###################################################################################
    
    ##################################################################################### STAGE 1 QUEST #####################################################################################
    if stage == 1: # Stage 1 quest stage. At this stage vehicle can control landing mode, arm the vehicle and perform predefined quests
        if arm_and_takeoff:
            armable = vhc_controller.prearmCheck()
            if armable: armed = vhc_controller.armThrottle()
            else: 
                arm_and_takeoff = 0
                stage = -1
            if armed:
                vhc_controller.takeoff(25)
                start_quest = 1
            else:
                arm_and_takeoff = 0
                stage = -1
        
        if start_quest:
            pass # in there vehicle perform predefined quest like go "x" coordinates or track vehicle
            
    ##################################################################################### STAGE 1 QUEST #####################################################################################
 