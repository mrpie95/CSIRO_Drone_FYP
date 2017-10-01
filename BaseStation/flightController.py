import math
import time
import dataTypes as dt
import imageProcessing as ip
import droneProtocols as dp

class flightController:
    CAM_RES = 300
    RESOLUTION = (CAM_RES,CAM_RES)
    GOAL_POS = CAM_RES/2 #the camera view is always sqaure so therefore no array is needed
    LANDING_ACCURACY = 30

    drone = None
    camera = None
    connection = None
   
    #initialise camera and drone connnections    
    def __init__(self, scf):
	print("Initialising the camera")
	self.camera = ip.imageProcessing(self.RESOLUTION, False)
	time.sleep(2)
        self.connection = scf
        print("Initialising the drone base connetion")
        self.drone = dp.initDrone(self.connection)

    def hoverAboveBase(self, height):
        dp.takeoff(self.drone,height)
	
	print("rot")
	self.rotDrone2Base(height)
	
	self.land(self.drone,height)
	dp.closeConnection(self.drone)

	
    def testFlight(self):
	dp.takeoff(self.drone, 0.3)
	dp.hover(self.drone, 0.3)
	print("right")
	dp.incrementRight(self.drone,0.3)
	dp.incrementRight(self.drone,0.3)
	dp.incrementRight(self.drone,0.3)
	dp.incrementRight(self.drone,0.3)
	print("left")
	dp.hover(self.drone, 0.3)
	dp.incrementLeft(self.drone,0.3)
	dp.incrementLeft(self.drone,0.3)
	dp.incrementLeft(self.drone,0.3)
	dp.incrementLeft(self.drone,0.3)
	
	    
    def emergencyLand(self):
	dp.quickLand(self.drone,0.3)
	#dp.land(self.drone, 0.4)
	
    def readCamera(self):
	return self.camera.readStream()

    #gets the drones position with safety incase loss of drone image
    def getPosition(self,height):

	#counts if the camera uses the drone
	#if counter gets too high the landing aborts
	lostDrone = 0
        while(True):
	    if (lostDrone > 3):
	        print("no drone detected")
	        return None
	
	    dp.hover(self.drone,height)
	    pos = self.camera.readStream()
	
            if (pos == None):
	        lostDrone += 1
	    else:
	       	return pos      

    #aligns the drone to the center
    def moveTowardsCenter(self, height, axis, increment):
        pos = self.getPosition(height)

        if pos == None:
             return None
	accuracy = self.LANDING_ACCURACY;
	
	if (axis == "x"):	   
   	    pos = pos.x

	    if (pos < (self.GOAL_POS-accuracy)):
		print(">>>MOVE RIGHT<<<")
		dp.incrementRight(self.drone,height,increment)

	    elif (pos > (self.GOAL_POS+accuracy)):
		print(">>>MOVE LEFT<<<")
		dp.incrementLeft(self.drone,height,increment)
		
        elif (axis == "y"):
	    pos = pos.y
	    if (pos < (self.GOAL_POS-accuracy)):
	        dp.incrementBackward(self.drone,height,increment)
		print(">>>MOVE DOWN<<<")
	
	    elif (pos > (self.GOAL_POS+accuracy)):
		dp.incrementForward(self.drone,height,increment)
		print(">>>MOVE UP<<<")

    #logic used to check drones alignment
    def checkAlignment(self,height,axis,accuracy):
        pos = self.getPosition(height)
		
	if (pos != None):
	    if (axis == "x"):
	        if ( (pos.x < (self.GOAL_POS+accuracy)) and (pos.x > (self.GOAL_POS-accuracy)) ):
		    return True
			
            elif (axis == "y"):
	        if ( (pos.y < (self.GOAL_POS+accuracy)) and (pos.y > (self.GOAL_POS-accuracy)) ):
		    return True
		
	    elif (axis == "center"):
	        if ( (pos.x < (self.GOAL_POS+accuracy)) and (pos.x > (self.GOAL_POS-accuracy))
		and (pos.y < (self.GOAL_POS+accuracy)) and (pos.y > (self.GOAL_POS-accuracy))):
	            return True
	
	return False

    #substute for GPS localisation
    def approuchBase(self, height):
	print("approuching base")

        dp.hover(self.drone,height)
        safety = 0	

        while(True):
            if safety > 2:
	        return False	
	    pos = self.getPosition(height)
    
            if (pos != None):
	        print("drone detected")
	        return True

	    dp.incrementForward(self.drone,height)
    	    safety += 1

    #line up drone to the center of the base
    def lineUpDrone(self,height,accuracy, increment):	    
	endTime = time.time() + 10

        while(True):
	    dp.hover(self.drone,height)

            pos = self.getPosition(height)
	    if(self.checkAlignment(height,"center",accuracy)):
                print("Aligned to the center")
	        break;		

   	    self.moveTowardsCenter(height,"x",increment)
	    dp.hover(self.drone,height)
	
	    if(self.checkAlignment(height,"center",accuracy)):
                print("Aligned to the center")
	        break;
	
	    self.moveTowardsCenter(height,"y",increment)    

    #blind method 2
    def searchForBase(self,height):	
        print("Looking for base station")
	
	xAxis = 0
	yAxis = 0

	dp.hover(self.drone,height)
	
	#pos = self.getPosition(height)
	#if pos != None:
	    #return true
	row = 0
	while (row < 8):
	    for xAxis in range(3):
	    	if ((row%2) == 0):
		    dp.incrementForward(self.drone,height,0.3)
		    if self.getPosition(height) != None:
	            	return true;
	        else:
	            dp.incrementBackward(self.drone,height,0.3)
		    if self.getPosition(height) != None:
	            	return true;
	    for yAxis in range(2):
	    	    dp.incrementRight(self.drone,height,0.15)
		    if self.getPosition(height) != None:
	            	return true;
	    row += 1
	print("base not found")
	print("retrying GPS to relocate base area")
	return false 


    def land(self,drone,h):
	print("landing drone")
	height = h
	
	self.rotDrone2Base(height)


	print("First stage")	
	dp.hover(self.drone,height)
	self.lineUpDrone(height,12,0.02)

	height = 0.25

	print("Second stage")
	dp.hover(self.drone,height)
	self.lineUpDrone(height,5,0.01)  

    def rotDrone2Base(self,height):
	x1 = None
	y1 = None
	x2 = None
	y2 = None
	x3 = self.CAM_RES/2
	y3 = 0
	direction = 1
	
	#record P1
	pos1 = self.getPosition(height)

	if pos1 == None:
	    print("not pos1 lock")
	    return False

	print("Pos 1: ")
	print(pos1)
		
	dp.incrementForward(self.drone,height, 0.1)
	dp.hover(self.drone,height)
		
	#record P2
	pos2 = self.getPosition(height)

	if pos2 == None:	
	    print("not pos2 lock")
	    return False

	print("Pos2: ")
	print(pos2)

	
	x1 = pos1.x
	y1 = pos1.y
	x2 = pos2.x
	y2 = pos2.y


	#points of the trinangle
	P12 = math.sqrt(math.pow((x2-x1),2)+math.pow((y2-y1),2))
	P31= math.sqrt(math.pow((x3-x2),2)+math.pow((y3-y2),2))
	P23 = math.sqrt(math.pow((x3-x1),2)+math.pow((y3-y1),2))
	
	print(P12)
	print(P23)
	print(P31)

	#calculate compensation angle
	try:  
	    top = (P12*P12)+(P23*P23)-(P31*P31)
	    bottom = (2*P12*P23)

	    angle = math.degrees(math.acos(top/bottom))

	    print("X1:")
	    print(x1)
	    print("x2:")
	    print(x2)
	
	    print("Aliging Drone")

	    if x2 < x1:
	    	angle = -1*angle

	    print("angle:")
	    print(angle)

	    dp.rotateBy(self.drone,self.connection,angle,height)

	except ValueError:
	    print("something fucked up")
	
	#dp.incrementBackward(self.drone,height, 0.1)

	



    

    
        