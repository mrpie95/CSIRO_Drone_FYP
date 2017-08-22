import sys
import threading
import imageProcessing as ip
import droneController as dc
import dataTypes as dt
import flightController as fc
import time
#import GUIControls

def main():
    
    resolution = (320,224)
    goalPos = dt.pos2D(resolution[0]/2, resolution[1]/2)
    init = True
    takeoffTimer = 0
    lostDroneTimer = 0
    
    
    image = ip.imageProcessing(resolution, True)
    drone = dc.DroneController()
        
    while(True):
        #get current drone data data9 center
        droneData = image.readStream()
        
        #intialisation of drone and flight controller
        if droneData != None and init:
            
            #flightCon.droneData = currentPos
            flightCon = fc.flightController(resolution, goalPos, droneData)
            
            #print(flightCon.droneData)
            #currentPos.direction = drone.initDirection 
            #flightCon.initDirection = drone.initDirection# currentPos.direction
           # print(drone.initDirection)
            init = False
        
        elif droneData != None:
            flightCon.droneData = droneData
            
            if droneData.inRadius:# or flightCon.ready:
                
                #if flightCon.ready:
                
                    #moveVec = flightCon.getMovementVector()
                    #drone.setMotors(moveVec.pitch, moveVex.roll, moveVec.yall, 0)
                
                    #print("ready")
                    #drone.setMotors()
                    #print("takeoff")
                    #drone.setMotors(35000)
                if takeoffTimer > 10:
                    #drone._ramp_motors()
                   # drone.setMotors(35000)
                    print("takeoff")
                    flightCon.ready = True
		    flightCon.angleCompensation()

                    #drone.setMotors(flightController.getTarget())
                    
                else:
                    takeoffTimer += 1
                    
            elif not droneData.detected:
		lostDroneTimer += 1

		if lostDroneTimer > 5:
	                print("power off detected")
                #drone.setMotors(0)
            else:
                print("power off radius")
                takeoffTimer = 0
		lostDroneTimer = 0

                #drone.setMotors(0)
            
                
            #print(droneData.inRadius)
            
            #direction = flightCon.getDirection()
            #print("direction - " + str(flightCon.initDirection))
    #   drone.setMotors(goalPos)
        
        #if (position!=None):
         #   print("x: "+str(position[0])+" y: "+str(position[1])+" radius: "+str(position[2]))
            
    
if __name__=="__main__":
    main()