import math
import dataTypes as dt
import imageProcessing as ip
import droneProtocols as dp

class flightController:
    RESOLUTION = (300,300)
    LANDING_ACCURACY = 10

    #global Variables
    pos1 = None
    pos2 = None
    compensationAngle = 0

    #global objects
    drone = None
    camera = None
    connection = None
   
	#initialise camera and drone connnections    
    def __init__(self, scf):
	self.connection = scf
	self.drone = dp.initDrone(self.connection)
	self.camera = ip.imageProcessing(self.RESOLUTION, True)

    #NOTE add safety
    def landDrone(self):
	height = 0.3
	dp.hover(drone,height)
	self.pos1 = camera.readStream()
	dp.incrementForward(drone,height)
	dp.hover(drone,height)
	self.pos2 = camera.readStream()
	self.compensationAngle = self.calcComp(pos1.x,pos1.y,pos2.x,pos2.y,pos1.detected)
	dp.rotateBy(drone,connection,self.compensationAngle,height)
	
	position = None

	while(True):
		position = camera.readStream()
		if (position.x < (RESOLUTION[0]+LANDING_ACCURACY))
			dp.incrementForward(drone,height)
		elif (position.x > (RESOLUTION[0]+LANDING_ACCURACY))
			dp.incrementBackward(drone,height)

	while(True):
		position = camera.readStream()
		if (position.y < (RESOLUTION[1]+LANDING_ACCURACY))
			dp.incrementForward(drone,height)
		elif (position.y > (RESOLUTION[1]+LANDING_ACCURACY))
			dp.incrementBackward(drone,height)
	
	dp.landDrone(drone,height)
	


    #gives the angle that will can needs to rotate to align with the base
    def calcComp(self,x1,y1,x2,y2,wall):

    	X=float(abs(x1-x2))
	Y=float(abs(y1-y2))
    	result = None
    
    	try:
            angle = math.degrees(math.atan(Y/X))

            #south wall
            if wall.south:
                if ((x1>=x2)and(y1>=y2)):
                    result = -1*angle
            elif ((x1<=x2)and(y1>=y2)):
                result = angle

            #east wall
	    elif wall.east:
        	if ((x1>=x2)and(y1<=y2)):
                    result = (-1*(angle+90))
            elif ((x1>=x2)and(y1>=y2)):
                result = -1*(90-angle)

            #north wall
            if wall.north:
            	if ((x1<=x2)and(y1<=y2)):
                    result = (180-angle)
            	elif ((x1>=x2)and(y1<=y2)):
                    result = (-1*(180-angle))

            #west wall
            elif wall.west:
            	if ((x1<=x2)and(y1>=y2)):
                    result = (90-angle)
            elif ((x1<=x2)and(y1<=y2)):
                result = (angle+90)
          
	    except ZeroDivisionError:
        	return "error"

	if result == None:
            return None

	if result >= 360:
            result -= 360

	compensationAngle = result
	return result
    
        