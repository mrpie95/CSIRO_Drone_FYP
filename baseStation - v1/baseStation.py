import sys
import threading
import imageProcessing as ip
import droneController as dc
import dataTypes as dt
import flightController as fc
#import GUIControls

def main():
    
    resolution = (320,224)
    goalPos = (resolution[0]/2, resolution[1]/2)
    
    image = ip.imageProcessing(resolution)
    #drone = droneController.DroneController()
    flightCon = fc.flightController(resolution, goalPos)
    
    while(True):
        currentPos = image.readStream()
        flightCon.droneData = currentPos
        
        if currentPos != None:
            direction = flightCon.getDirection()
            print("direction - " + str(direction))
    #   drone.setMotors(goalPos)
        
        #if (position!=None):
         #   print("x: "+str(position[0])+" y: "+str(position[1])+" radius: "+str(position[2]))
            
    
if __name__=="__main__":
    main()