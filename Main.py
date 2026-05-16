from init import init
from MissionStage_1 import MissionStage_1
from MissionStage_2 import MissionStage_2
from MissionStage_3 import MissionStage_3
from Emergency import SafeLand
import sys

while True:
    try:
        init()
    except Exception as e:
        print("\n\n\nAn unexpected error occured on init()\n\n\n")
        print(e)
        raise e
    try:
        MissionStage_1()
        MissionStage_2()
        MissionStage_3()
    except Exception as e:
        SafeLand()
        print(e)
        sys.exit()
