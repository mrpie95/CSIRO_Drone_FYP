import sys
import threading
import imageProcessing as ip
#import droneController2 as dc
import dataTypes as dt
import flightController as fc
import time

import logging
import cflib

from collections import namedtuple
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
#from cflib.crazyflie.log import LogConfig

#import GUIControls



def main():
    
    URI = "radio://0/80/250K"
    resolution = (320,224)
    goalPos = dt.pos2D(resolution[0]/2, resolution[1]/2)
    init = True
    takeoffTimer = 0
    lostDroneTimer = 0
    cf = None;
    
    image = ip.imageProcessing(resolution, True)
    #drone = dc.DroneController()

    cflib.crtp.init_drivers(enable_debug_driver=False)
    with SyncCrazyflie(URI) as scf:
	    cf = initialiseDrone(scf)
	    
        
	    while(True):
	        #get current drone data data center
	        droneData = image.readStream()
	
	        if droneData != None and init:
	            flightCon = fc.flightController(resolution, goalPos, droneData)
	            init = False
	        
	        elif droneData != None:
	            flightCon.droneData = droneData
	            
	            if droneData.inRadius:# or flightCon.ready:
	                if takeoffTimer > 10:
			    runTest(cf) 
	                    print("takeoff")
	                    flightCon.ready = True
			    flightCon.angleCompensation()
	                    
	                else:
	                    takeoffTimer += 1
	                    
	            elif not droneData.detected:
			lostDroneTimer += 1
	
			if lostDroneTimer > 5:
		            print("power off detected")
	              
	            else:
	                print("power off radius")
	                takeoffTimer = 0
		lostDroneTimer = 0

def initialiseDrone(scf):
        cf = scf.cf
	cf.param.set_value('kalman.resetEstimation', '1')
        time.sleep(0.1)
	cf.param.set_value('kalman.resetEstimation', '0')
	time.sleep(2) 
	return cf
	
def runTest(cf):
	#cflib.crtp.init_drivers(enable_debug_driver=False)
	print("power on")
	#self.cf.commander.send_hover_setpoint(0,0,0,0.1)
	
	#cf = self.scf.cf
	#if scf != None:
            #print(self.scf)

	for _ in range(5):
            cf.commander.send_hover_setpoint(0,0,0,0.1)
            time.sleep(0.1)
    
if __name__=="__main__":
    print("main")
    main()