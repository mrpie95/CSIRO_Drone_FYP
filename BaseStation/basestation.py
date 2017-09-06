import logging
import time
import droneProtocols as dp
import imageProcessing as ip
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
    #camera = ip.imageProcessing(RESOLUTION, True)

    #>>>Program Starts Here<<<

    with SyncCrazyflie(URI) as scf:
	    baseStation = fc.flightController(scf)
			
			while(True):
				
				
		droneData = camera.readStream()
		if droneData != None:
		    print(dp.angleCompensation(0,1,1,2, droneData.detected))
		

    
        cf = dp.initDrone(scf)
	height = 0.4

	dp.takeoff(cf, height)
	dp.rotateTo(cf, scf, 180, 0.3)
	dp.land(cf, height)


	"""dp.takeoff(cf, height)
	dp.incrementForward(cf, height)
	dp.hover(cf,height)
	dp.incrementBackward(cf, height)
	dp.hover(cf,height)
	dp.land(cf, height)"""

	dp.closeConnection(cf)
