

#################### Vehicle Connection Parameters ####################
vehicleType = 0                                 # 0 for ardupilot connection 1 for sitl connection
vehicleConnectionIP = "/dev/ttyAMA0"                   # Connection Adress
#vehicleConnectionIP = 'tcp:127.0.0.1:5763'      # Connection Adress
vehicleConnectionBaudrate = 115200              # Connection Baudrate
vehicleConnectionTimeout = 30                   # Connection Timeout until success
vehicleConnectionWaitReady = True               # Wait Until parameters ready True/False
vehicleConnectionRate = 4                       # Data Refresh Rate. 4Hz standart (4 data per second).

vehicle = None                                  # vehicle object for public use
# Dronekit user manuel source
# https://dronekit-python.readthedocs.io/en/latest/automodule.html || (dronekit.connect)

#################### Vehicle Sensor Parameters ####################
vehicleEnableLidar = True                      # Enables/Disables Lidar
vehicleEnableGimball = True                    # Enables/Disables Gimball
vehicleCameraType = 0                          # 0: internal raspberry cam, 1:simulation test cam, 2:test video input
vehicleInternalCameraSource = 0                # 0: standart camera source. set 1 or higher for second or other sources
#vehicleUARTCameraSource = "COM3"                # openmv connection UART adress
vehicleSimCameraSource = None                   # simulation source
cameraFovAngle = [75.7, 56.775]                      # cameras fov angles -1 means calculate using given frame like (1920, 1080) frame (120/1920 * 1080)
frameSize = [640, 480]                          # !!!!!!!!!!!!! FIXED VALUE DO NOT CHANGE IT !!!!!!!!!!!!!
centerPoint = [320, 240]
capture = None                                  # Camera capture object for public use
frameGlobal = None                              # Frame object for public use
image_topic = "/roscam/cam/image_raw"		    # image topic
#################### Mission Parameters ####################
precisionReadingAltitude = 7                    # (meters) the altitude of drone to start search marker
landingAltitude = 0.3                           # (meters) the altitude of drone when will land 30cm default
missionMode = 0                                 # 0: Manuel Mode; drone waits until mode changes to "LAND"
                                                # 1: Autonomus Mode; drone does predefined ARDUPILOT mission and perform "LAND"
                                                # 2: Software Autonomus Mode; drone does predefined mission (mission defined in software)
landMode = 0                                    # 0: Direct Land; drone waits until "LAND" and start landing process
                                                # 1: GPS Supported landing; drone goes marker GPS coordinates and lands
                                                # 2: Trajectory Track Mode; Unlike GPS in this mode drone try follow moving marker and creates trajectory 
detectionTimeout = 20                           # Detection timeout on (s)
landingPoint = (-35.361354, 149.165218, 50)     # landing start point for landMode 1
zAxisDefaultSpeed = 0.1                         # default z axis descent speed = 1, velocity calc = gain * default velocity
zAxisGain = 0.50000                             # default z axis gain = 1, velocity calc = gain * default velocity
zVelocity = 0                                   # updates every frame

velocitySaturation = 1.3
xAxisProportionalGain = 0.00700000              # Kp value of x axis
yAxisProportionalGain = 0.00700000              # Kp value of y axis
