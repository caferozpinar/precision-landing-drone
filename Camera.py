import Parameters as p
import cv2
from MotionControl import StopMove
#from sensor_msgs.msg import Image
#from cv_bridge import CvBridge, CvBridgeError
#import rospy

initalizerFrame = True
capture = None
bridge = None
cameradict = {
        0 : "INTERNAL",
        1 : "SIM",
        2 : "TEST"
        }

def __FrameToGlobal(data):
    global bridge
    p.frameGlobal = bridge.imgmsg_to_cv2(data, desired_encoding='passthrough')

def GetNextFrame(source: str = "INTERNAL"):
    """Gets next frame, and returns it as (status, frame)

    PARAMETERS

    source (str): Can be set as 

    ``0:INTERNAL``, ``1:SIM`` or ``2:TEST``

    ``INTERNAL``: Calls camera object of raspberry-pi\n
    ``SIM``: Calls cam object of gazebo-simulation\n
    ``TEST``: Calls given test sources object\n

    out List[``frame``]:
    
    ``frame``: Next frame of video source 
    Source crash(like video end or connection lost) returns None otherwise return ``np.array``
    """
    if type(source) != str:
        source = cameradict[source]
    global initalizerFrame
    global capture
    
    if source == "INTERNAL":
        try: 
            if initalizerFrame:
                p.capture = cv2.VideoCapture(0)
                if p.capture.isOpened():
                    initalizerFrame = False
                    print("frameinitalizeDone")
                
            
            ret, frame = p.capture.read()
            
            if not ret:
                print("frame read failed")
                StopMove()
            else:
                cv2.resize(frame, (p.frameSize[0], p.frameSize[1]))
        except ConnectionError as e:
            print("frame reading failed")
            print(e)
            raise RuntimeError
        
        except Exception as e:
            print("Something went wrong while reading frame.")
            print(e)
            raise RuntimeError
        
        return frame

    elif source == "SIM":
        try: 
            if initalizerFrame:
                rospy.init_node('image_converter')
                bridge = CvBridge()
                rospy.Subscriber(p.image_topic, Image, __FrameToGlobal)
                r = rospy.Rate(120)

            rospy.Subscriber(p.image_topic, Image, __FrameToGlobal)
            r = rospy.Rate(120)
            frame = p.frameGlobal
            p.frameGlobal = None
            try:
                cv2.resize(frame, (p.frameSize[0], p.frameSize[1]))
            except:
                StopMove()
                
            
        except ConnectionError:
            print("frame reading failed")
            print(e)
            raise RuntimeError
        
        except Exception as e:
            print("Something went wrong while reading frame.")
            print(e)
            raise RuntimeError
        
        return frame
    
    elif source == "TEST":
        try:
            if initalizerFrame:
                capture = cv2.VideoCapture(p.vehicleUARTCameraSource)
                initalizerFrame = False

            ret, frame = capture.read()
            if not ret:
                raise ConnectionError

        except ConnectionError as e:
            print("frame reading failed")
            print(e)
            raise ConnectionError
        except Exception as e:
            print("Something went wrong while reading frame.")
            print(e)
            raise RuntimeError
        
        return frame

def CloseCam(source: str = "INTERNAL"):
    if type(source) != str:
        source = cameradict[source]
    global capture
    if source == "INTERNAL":
        try:
            if capture != None and capture.isOpened():
                capture.release()
                print("INTERNAL cam closed")
        except Exception as e:
            print("Something went wrong while closing cam")
            print(e)
            raise RuntimeError
    if source == "SIM":
        pass
    if source == "TEST":
        try:
            capture.release()
            print("TEST video closed.")
        except Exception as e:
            print("Something went wrong while closing video")
            print(e)
            raise RuntimeError
