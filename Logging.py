import time
import Parameters as p
from datetime import datetime

file = None



def __init__():
    pass

current_datetime = datetime.now().strftime("%Y-%m-%d_%H.%M.%S")

filename = str(current_datetime) + "_LOG.csv"

file = open(filename, 'a')

for i in range(1,100):
    now = datetime.now()
    file.write(str(now.strftime("%H:%M:%S.%f")) + "," + str(i) + "," + str(i+i) + "," + str(1/i) +"\n")
    print(now.strftime("%H:%M:%S.%f"))
    time.sleep(0.01)

file.close()

    