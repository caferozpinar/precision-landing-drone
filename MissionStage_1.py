import Parameters as p


def MissionStage_1():
    try:
        print("MissionStage_1 Started.")
        if p.missionMode == 0:
            while True:
                if p.vehicle.mode.name == "LAND":
                    p.vehicle.mode = "GUIDED"
                    print("MissionStage_1 Completed.")
                    break 
        elif p.missionMode == 1:
            while True:
                if p.vehicle.mode.name == "LAND":
                    p.vehicle.mode = "GUIDED"
                    print("MissionStage_1 Completed.")
                    break 
        elif p.missionMode == 2:
            # do some quests before landing
            while True:
                if p.vehicle.mode.name == "LAND":
                    p.vehicle.mode = "GUIDED"
                    print("MissionStage_1 Completed.")
                    break 
        else:
            print("Mission Mode '%s' not found." %p.missionMode)
            raise ValueError
    except Exception as e:
        print("Unexpected error occured during mission.")
        raise e
