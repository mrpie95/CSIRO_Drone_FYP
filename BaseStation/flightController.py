import math
import time
import dataTypes as dt
import imageProcessing as ip
import droneProtocols as dp

class flightController:
    CAM_RES = 300
    RESOLUTION = (CAM_RES,CAM_RES)
    GOAL_POS = CAM_RES/2 #the camera view is always sqaure so therefore no array is needed
    LANDING_ACCURACY = 25

    #sets if debug messages are shown
    debug = True
	
    #general cruise height used to fly the drone in meters 
    height = 0

    drone = None
    camera = None
    connection = None
   
    lastDetected = None

    #initialise camera and drone connnections    
    def __init__(self, scf, height):
	self.height = height
	print("Initialising the camera")
	self.camera = ip.imageProcessing(self.RESOLUTION, True)
	time.sleep(2)
        self.connection = scf
        print("Initialising the drone base connetion")
        self.drone = dp.initDrone(self.connection)

    def readCamera(self):
	return self.camera.readStream()

    #flies the drone to a set position
    def flyDroneTo(self, mission):	
	dp.takeoff(self.drone,self.height)

	dp.hover_for(self.drone,self.height,15)

	self.flyFromBaseTo(mission)

	dp.hover_for(self.drone,self.height,15)
	
	#if the drone is not detected over the base start the spiral search method
	if (self.getPosition(0.3) == None):
		self.searchForBase2()
	self.land(0.4)

	dp. hover2(self.drone,0,0.3)

	dp. hover2(self.drone,2,0.1)
	dp.closeConnection(self.drone)
	print("Mission Complete")
	
    #used to fly the drone to and from a set mission site
    def flyFromBaseTo(self,mission):
	x = mission[0]
	y = mission[1]
	time = mission[2]
	
	angle = 0

	try:
	    angle = math.degrees(math.atan(math.fabs(y/x)))

	except ZeroDivisionError:
	    print("Division of zero caught")

	#sanity check - thanks POD
	if ((x == 0) and (y == 0)):
	    print("Error the drone cannot fly to the position that it is already at")

	#y axis
	elif ((x == 0) and (y > 0)):
	    angle = 0

	elif ((x == 0) and (y < 0)): 
	    angle =  180
	
	#x axis
	elif ((x > 0) and (y == 0)):
	    angle = -90

	elif ((x < 0) and (y == 0)):
	    angle = 90

	#all other angles 
	elif ((x > 0) and (y > 0)):
	    angle = -1*angle
	
	elif ((x < 0) and (y > 0)):
	    angle = angle

	elif ((x < 0) and (y < 0)): 
	    angle =  angle + 90

	elif ((x > 0) and (y < 0)):
	    angle = -1*angle - 90

	#pythag to get the distance
	distance = math.sqrt((x*x) + (y*y))

	dp.rotateBy(self.drone, self.connection, angle, self.height)
	print("Rotated drone to mission coordinates")
	dp.incrementForward(self.drone,self.height,distance)

	print("Coordinates reached")
	print("Collecting Samples")
	dp.hover_for(self.drone, self.height, time)
	dp.rotateBy(self.drone, self.connection, 180, self.height)

	print("Rotated Drone Towards Base")
	dp.incrementForward(self.drone,self.height,distance*0.85)  
	print("Looking For Base")
	
    #demo mode flies drone above base and lands     	
    def hoverAboveBase(self, height):
        dp.takeoff(self.drone,height)
	
	print("rot")
	self.rotDrone2Base(height)
	
	self.land(self.drone,height)
	dp. hover2(self.drone,0,0.3)

	dp. hover2(self.drone,2,0.3)
	dp.closeConnection(self.drone)    
		

    #gets the drones position with safety incase loss of drone image
    def getPosition(self,height):

	#counts if the camera uses the drone
	#if counter gets too high the landing aborts
	lostDrone = 0

        while(True):
	    if (lostDrone > 3):
	        print("No Drone Detected")
	        return None
	
	    dp.hover(self.drone,self.height)
	    pos = self.camera.readStream()
			
	    #check if drone over base
            if (pos == None):
	        lostDrone += 1
	    else:
	       	return pos      

    #line up drone to the center of the base
    def lineUpDrone(self,height,accuracy, increment):	    
	endTime = time.time() + 10
	
	checkRot = 0;	

	#will loop until the drone is aligned with the center
	# of the base
        while(True):
	    dp.hover(self.drone,height)
	    checkRot += 1

	    #if the drone has made too many movements
	    #realign it with the base
	    if checkRot > 7: 
		self.rotDrone2Base(height)
		checkRot = 0

            pos = self.getPosition(height)
	
	    #if the drone lost use spiral method to find again
	    if (pos == None):
		self.searchForBase2()	    
		pos = self.getPosition(height)
	 
	    if(self.checkAlignment(height,"center",accuracy, pos)):
                print("Aligned to the center")
	        break;		

   	    self.moveTowardsCenter(height,"x",increment, pos)
	    dp.hover(self.drone,height)
	
	    if(self.checkAlignment(height,"center",accuracy, pos)):
                print("Aligned to the center")
	        break;
	
	    self.moveTowardsCenter(height,"y",increment, pos) 

    #aligns the drone to the center
    def moveTowardsCenter(self, height, axis, increment, pos):

        if pos == None:
             return None

	#sets how accurately the drone will land
	accuracy = self.LANDING_ACCURACY;
	
	#compensation for the cameras misalignment
	camComp = 30
	
	if (axis == "x"):	   
   	    pos = pos.x

	    if (pos < (self.GOAL_POS+camComp-accuracy)):
		print(">>>MOVE RIGHT<<<")
		dp.incrementRight(self.drone,height,increment)

	    elif (pos > (self.GOAL_POS+camComp+accuracy)):
		print(">>>MOVE LEFT<<<")
		dp.incrementLeft(self.drone,height,increment)
		
        elif (axis == "y"):
	    pos = pos.y
	    if (pos < (self.GOAL_POS-camComp-accuracy)):
	        dp.incrementBackward(self.drone,height,increment)
		print(">>>MOVE DOWN<<<")
	
	    elif (pos > (self.GOAL_POS-camComp+accuracy)):
		dp.incrementForward(self.drone,height,increment)
		print(">>>MOVE UP<<<")

    #logic used to check drones alignment over the base station
    def checkAlignment(self,height,axis,accuracy ,pos):
	#compensation for the cameras misalignment
	camComp = 30
		
	if (pos != None):
	    print("checking alignment")
   	    print(self.GOAL_POS+45+accuracy)
	    print(self.GOAL_POS+45-accuracy)
	    if (axis == "x"):
	        if ( (pos.x < (self.GOAL_POS+camComp+accuracy)) and (pos.x > (self.GOAL_POS+camComp-accuracy)) ):
		    print("X axis aligned")
		    return True
			
            elif (axis == "y"):
	        if ( (pos.y < (self.GOAL_POS-camComp+accuracy)) and (pos.y > (self.GOAL_POS-camComp-accuracy)) ):
		    print("Y axis aligned")
		    return True
		
	    elif (axis == "center"):
	        if ( (pos.x < (self.GOAL_POS+camComp+accuracy)) and (pos.x > (self.GOAL_POS+camComp-accuracy))
		and (pos.y < (self.GOAL_POS+accuracy-camComp)) and (pos.y > (self.GOAL_POS-camComp-accuracy))):
	            print("The Drone Is Centered")
		    return True
	
	return False

    #substute for GPS localisation
    #not currently used
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

    #blind spiral method- spirals out until it finds the base
    def searchForBase2(self):	
	dp.hover(self.drone,self.height)
	i = 1;
	count = 1
	
	
	while (i < 360):
	
	    #HYPERBOLA equation used to for define the spiral 
	    #parameters
	    roll =(600/(i+30))
	    thrust = 0.1
	    print(roll)
	    print(i)
	    for _ in range(10):	
		if self.debug: print("Checking for Drone")
	       	    
		pos = self.camera.readStream()
				
		#if the base locates the drone exit method
		if ((i > 1) and (pos!= None)):
		    if self.debug: print("Base found")
		    dp.hover(self.drone,self.height)	
	       	    return True; 
			
		self.drone.commander.send_hover_setpoint(thrust,0,roll,self.height)
        	time.sleep(0.1)
		
	    i = i +1

	return False
	    
    #2 Stage landing protocol used by drone to land on base
    # with soft landing just for romrom
    def land(self, h):
	print("landing drone")
	height = 0.35
	
	self.rotDrone2Base(height)

	height = 0.3
	print("First stage")	
	dp.hover(self.drone,height)
	self.lineUpDrone(height,self.LANDING_ACCURACY,0.15)

	height = 0.2

	print("Second stage")
	dp.hover(self.drone,height)
	self.lineUpDrone(height,self.LANDING_ACCURACY,0.1)  

    #trianle rotation method used to aline up the drone 
    #with the north side (up) of the base station
    def rotDrone2Base(self,height):

	#the coordinates of the triangle
	x1 = None
	y1 = None
	x2 = None
	y2 = None
	x3 = (self.CAM_RES/2)
	y3 = 0
	direction = 1
	
	#record P1
	pos1 = self.getPosition(height)

	if pos1 == None:
	    return False
		
	dp.incrementForward(self.drone,height, 0.1)
	dp.hover(self.drone,height)
		
	#record P2
	pos2 = self.getPosition(height)

	if pos2 == None:	
	    return False

	x1 = pos1.x
	y1 = pos1.y
	x2 = pos2.x
	y2 = pos2.y

	#points of the trinangle
	P12 = math.sqrt(math.pow((x2-x1),2)+math.pow((y2-y1),2))
	P31= math.sqrt(math.pow((x3-x2),2)+math.pow((y3-y2),2))
	P23 = math.sqrt(math.pow((x3-x1),2)+math.pow((y3-y1),2))

	#calculate compensation angle 
	try:  
    	    #parts of a fractions
	    top = (P12*P12)+(P23*P23)-(P31*P31)
	    bottom = (2*P12*P23)

	    angle = math.degrees(math.acos(top/bottom))

	    if x2 < x1:
	    	angle = -1*angle

	    dp.rotateBy(self.drone,self.connection,angle,height)

	except ZeroDivisionError:
	    print("something ducked up")
	

	



    

    
        