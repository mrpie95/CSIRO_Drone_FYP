import logging
import time
import droneProtocols as dp
import imageProcessing as ip
import flightController as fc
import cflib.crtp

#radio channel of drone 1
URI = "radio://0/80/250K"

from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.crazyflie.syncLogger import SyncLogger
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)


if __name__ == '__main__':
	 
    print("1 - debug mode (preset coordinantes")
    print("2 - cam calibration")
    print("3 - demo day program\n")
    input = raw_input("Enter the program mode: ")

    # Initialize the low-level drivers (don't list the debug drivers)
    cflib.crtp.init_drivers(enable_debug_driver=False)

    #height that the drone will cruise at
    height = 0.4
	
    with SyncCrazyflie(URI) as scf:  
	baseStation = fc.flightController(scf,height)
	
	#menu logic
	if (input == "1"):
	    missions = []
	    missions.append([]) 
	    missions.append([])
	
	    #first coordinates
	    missions[0].append(0.5)
	    missions[0].append(0.5)
	    missions[0].append(20)
		
	    baseStation.flyDroneTo(missions[0])
	
	elif (input == "2"):
	    while True:
		baseStation.readCamera()
	
	elif (input == "3"):
	    missions = []
	    missions.append([]) 
	    missions.append([])
	
	    x = float(raw_input("Enter the x coordinante: "))
	    y = float(raw_input("Enter the y coordinante: "))
	    time = int(raw_input("Enter the sampling time: "))
    
	    missions[0].append(x)
	    missions[0].append(y)
	    missions[0].append(time)
	
	    baseStation.flyDroneTo(missions[0])
	
	
	    

            