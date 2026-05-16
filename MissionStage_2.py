import Parameters as p
from MotionControl import SetVelocity
def MissionStage_2():
    print("MissionStage_2 start")
    try:
        if p.landMode == 0:
            if p.vehicle.location.global_relative_frame.alt > p.precisionReadingAltitude:
                while p.vehicle.location.global_relative_frame.alt > p.precisionReadingAltitude:
                    SetVelocity(0, 0, 0.4)
            if p.vehicle.location.global_relative_frame.alt < p.precisionReadingAltitude:
                SetVelocity(0, 0, 0)
        elif p.landMode == 1:
            p.vehicle.simple_goto(p.landingPoint)
            while True:
                if p.vehicle.location.global_relative_frame.lat >= p.landingPoint[0] * 0.95 and p.vehicle.location.global_relative_frame.lat <= p.landingPoint[0] * 1.05:
                    if p.vehicle.location.global_relative_frame.lon >= p.landingPoint[1] * 0.95 and p.vehicle.location.global_relative_frame.lon <= p.landingPoint[1] * 1.05:
                        break
            if p.vehicle.location.global_relative_frame.alt > p.precisionReadingAltitude:
                while p.vehicle.location.global_relative_frame.alt > p.precisionReadingAltitude:
                    SetVelocity(0, 0, 0.4)
            if p.vehicle.location.global_relative_frame.alt < p.precisionReadingAltitude:
                SetVelocity(0, 0, 0)
        elif p.landMode == 2:
            print("Landing Mode '%s' not found for now." %p.landMode)
            raise ValueError
        else:
            print("Landing Mode '%s' not found." %p.landMode)
            raise ValueError
        print("MissionStage_2 end")
    except Exception as e:
        print("Unexpected Error while Checking Land Mode.")
        print(e)
        raise e
