import Parameters as p
from pymavlink import mavutil
import math
errorX = 0
errorY = 0

def SetVelocity(vx, vy, vz):
    """ Remember: vz is positive downward!!!
    http://ardupilot.org/dev/docs/copter-commands-in-guided-mode.html
        
    Bitmask to indicate which dimensions should be ignored by the vehicle 
    (a value of 0b0000000000000000 or 0b0000001000000000 indicates that 
    none of the setpoint dimensions should be ignored). Mapping: 
    bit 1: x,  bit 2: y,  bit 3: z, 
    bit 4: vx, bit 5: vy, bit 6: vz, 
    bit 7: ax, bit 8: ay, bit 9:
    """
    msg = p.vehicle.message_factory.set_position_target_local_ned_encode(
            0,
            0, 0,
            mavutil.mavlink.MAV_FRAME_BODY_NED,
            0b0000111111000111, #-- BITMASK -> Consider only the velocities
            0, 0, 0,        #-- POSITION
            vx, vy, vz,     #-- VELOCITY
            0, 0, 0,        #-- ACCELERATIONS
            0, 0)
    p.vehicle.send_mavlink(msg)
    p.vehicle.commands.upload()

def SetHeading(heading):
    msg = p.vehicle.message_factory.command_long_encode(
    0, 0,    # target_system, target_component
    mavutil.mavlink.MAV_CMD_CONDITION_YAW, #command
    0, #confirmation
    heading,    # param 1, yaw in degrees
    0,          # param 2, yaw speed deg/s
    1,          # param 3, direction -1 ccw, 1 cw
    0, # param 4, relative offset 1, absolute angle 0
    0, 0, 0)    # param 5 ~ 7 not used
    # send command to vehicle
    p.vehicle.send_mavlink(msg)
    p.vehicle.commands.upload()
def StopMove():
    SetVelocity(0, 0, 0)
    
def TrackCoordinates(markerPoints, inputref):
    global errorX
    global errorY
    referencepoint = [None, None]
    if not p.vehicleEnableGimball:
        # fix the reference point with using vehicle attitude.
        rollAngleDegree = math.degrees(p.vehicle.attitude.roll)
        pitchAngleDegree = math.degrees(p.vehicle.attitude.pitch)
        referencepoint[0] = inputref[0] - ((inputref[0] * rollAngleDegree) / (p.cameraFovAngle[0] / 2))
        referencepoint[1] = inputref[1] - ((inputref[1] * pitchAngleDegree) / (p.cameraFovAngle[1] / 2))
    else:
        referencepoint = inputref
    if len(markerPoints) == 0:
        velocityX = errorX * p.xAxisProportionalGain
        velocityY = errorY * p.yAxisProportionalGain

    else:
        # Fix yaw direction
        # errorAngle = math.atan2((markerPoints[1][1] - markerPoints[3][1]),(markerPoints[1][0] - markerPoints[3][0]))
        # fixedAngle = p.vehicle.heading + errorAngle
        # SetHeading(fixedAngle)
        # Head Marker
        markerCenter = [0, 0]
        for i in markerPoints:
            markerCenter[0] += i[0]
            markerCenter[1] += i[1]
        markerCenter[0] /= 4
        markerCenter[1] /= 4

        errorX = referencepoint[0] - markerCenter[0]
        errorY = referencepoint[1] - markerCenter[1]
        
        velocityX = errorX * p.xAxisProportionalGain
        velocityY = errorY * p.yAxisProportionalGain

    if velocityY > p.velocitySaturation: velocityY = p.velocitySaturation
    if velocityY < p.velocitySaturation * -1: velocityY = p.velocitySaturation * -1
    if velocityX > p.velocitySaturation: velocityX = p.velocitySaturation
    if velocityX < p.velocitySaturation * -1: velocityX = p.velocitySaturation * -1
    velocityX = velocityX * -1
    velocityY = velocityY * -1
    print(velocityX, velocityY, p.zVelocity)
    SetVelocity(velocityX, velocityY, p.zVelocity)
    
def DecreaseAltitude(markerPoints, inputref):
    global errorX
    global errorY
    referencepoint = [None, None]
    if not p.vehicleEnableGimball:
        # fix the reference point with using vehicle attitude.
        rollAngleDegree = math.degrees(p.vehicle.attitude.roll)
        pitchAngleDegree = math.degrees(p.vehicle.attitude.pitch)
        referencepoint[0] = inputref[0] - ((inputref[0] * rollAngleDegree) / (p.cameraFovAngle[0] / 2))
        referencepoint[1] = inputref[1] - ((inputref[1] * pitchAngleDegree) / (p.cameraFovAngle[1] / 2))
    else:
        referencepoint = inputref
    if len(markerPoints) == 0:
        velocityX = errorX * p.xAxisProportionalGain
        velocityY = errorY * p.yAxisProportionalGain

    else:
        # Fix yaw direction
        # errorAngle = math.atan2((markerPoints[1][1] - markerPoints[3][1]),(markerPoints[1][0] - markerPoints[3][0]))
        # fixedAngle = p.vehicle.heading + errorAngle
        # SetHeading(fixedAngle)
        # Head Marker
        markerCenter = [0, 0]
        for i in markerPoints:
            markerCenter[0] += i[0]
            markerCenter[1] += i[1]
        markerCenter[0] /= 4
        markerCenter[1] /= 4

        errorX = referencepoint[0] - markerCenter[0]
        errorY = referencepoint[1] - markerCenter[1]
        
        velocityX = errorX * p.xAxisProportionalGain
        velocityY = errorY * p.yAxisProportionalGain

    if velocityY > p.velocitySaturation: velocityY = p.velocitySaturation
    if velocityY < p.velocitySaturation * -1: velocityY = p.velocitySaturation * -1
    if velocityX > p.velocitySaturation: velocityX = p.velocitySaturation
    if velocityX < p.velocitySaturation * -1: velocityX = p.velocitySaturation * -1
    velocityX = velocityX * -1
    velocityY = velocityY * -1
    p.zVelocity = ((p.velocitySaturation - abs(velocityX)) + (p.velocitySaturation - abs(velocityY))) / 2

def CheckDisarmAltitude() -> bool: #"returns true or false value"
    if p.vehicle.location.global_relative_frame.alt < p.landingAltitude:
        return True
    return False

def DisarmMotors():
    p.vehicle.mode = "LAND"
