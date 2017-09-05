import sys
import threading
import imageProcessing as ip
#import droneController2 as dc
import dataTypes as dt
import flightController as fc
import droneProtocol as dp
import time

import logging
import cflib

from collections import namedtuple
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
#from cflib.crazyflie.log import LogConfig

from cflib.crazyflie.log import LogConfig



def main():
    
    URI = "radio://0/80/250K"
    resolution = (360,360)
    goalPos = dt.pos2D(resolution[0]/2, resolution[1]/2)
    init = True
    takeoffTimer = 0
    lostDroneTimer = 0
    cf = None;
    
    image = ip.imageProcessing(resolution, True)
    #drone = dc.DroneController()

    cflib.crtp.init_drivers(enable_debug_driver=False)
    with SyncCrazyflie(URI) as scf:
	    cf = dp.initialiseDrone(scf)
	    
	    while(True):
	        #get current drone data data center
	        droneData = image.readStream()
		
		if droneData != None and init:
	            flightCon = fc.flightController(resolution, goalPos, droneData)
	            init = False

		#checks if the drone positioning data has been aquired   
	        elif droneData != None:
	            flightCon.droneData = droneData
		    print(flightCon.getDirection())
	            image.drawHUD(droneData.x, droneData.y, flightCon.getMovementVector(goalPos))

	            if droneData.inRadius:
	                if takeoffTimer > 10:
	                    print("takeoff")
	                    flightCon.ready = True
			    #flightCon.angleCompensation()

	                    motorControl(cf,flightCon.getMovementVector(goalPos),0.3) 
			    
	                    
	                else:
	                    takeoffTimer += 1
	                    
	            elif not droneData.detected:
			lostDroneTimer += 1
			motorControl(cf, (0,0,0), 0)
	
			if lostDroneTimer > 5:
		            print("power off detected")
	              
	            else:
	                print("power off radius")
	                takeoffTimer = 0
		lostDroneTimer = 0



 #vx, vy in m/s, yawrae in d/s and z distance is in m
def motorControl(cf, vector, z):
	for _ in range(2):	
            cf.commander.send_hover_setpoint(vector.pitch,vector.roll,vector.yall,z)
            time.sleep(0.1)

		
    
if __name__=="__main__":
    print("main")
    main()