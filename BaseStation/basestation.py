import logging
import time
import droneProtocols as dp
import imageProcessing as ip
import flightController as fc
import cflib.crtp

URI = "radio://0/80/250K"


from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.crazyflie.syncLogger import SyncLogger
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)


if __name__ == '__main__':
    # Initialize the low-level drivers (don't list the debug drivers)
    cflib.crtp.init_drivers(enable_debug_driver=False)

    #>>>Program Starts Here<<<
    height = 0.3
	
    with SyncCrazyflie(URI) as scf:  
	baseStation = fc.flightController(scf)
	baseStation.flyDroneTo();

	#baseStation.testFlight()
	#baseStation.hoverAboveBase(height)
	#baseStation.rotDrone2Base(height)
	#baseStation.getPosition(0.4)
	#baseStation.bringDroneHome(height)

	#baseStation.testFlight()
	#baseStation.emergencyLand()
	
	"""while(True):
	    x = 0
	    baseStation.readCamera()
	
	while(True):
	    #baseStation.readCamera()
	    statues = baseStation.approuchBase()
   	    print(statues)
            if (statues):
	    	baseStation.landDrone()"""

	
	#if (statues):
	   # baseStation.landDrone()
	

		
   	"""statues = baseStation.approuchBase()
	while(True):
    	baseStation.testFlight()
    	baseStation.emergencyLand()
	
    	if (statues):
	baseStation.landDrone()
   	else:
	    print("Drone missing, emergency")
		baseStation.emergencyLand()"""
            