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
	
	if (self.getPosition(0.3) == None):
		self.searchForBase2()
	self.land(0.4)

	dp. hover2(self.drone,0,0.3)

	dp. hover2(self.drone,2,0.1)
	dp.closeConnection(self.drone)
	print("mission complete")
	
    def flyFromBaseTo(self,mission):
	
	x = mission[0]
	y = mission[1]
	time = mission[2]
	
	angle = math.degrees(math.atan(math.fabs(y/x)))
	print(angle)	

	if ((x > 0) and (y > 0)):
	    angle = -1*angle
	
	elif ((x < 0) and (y > 0)):
	    angle = angle

	elif ((x < 0) and (y < 0)): 
	    angle =  angle + 90

	elif ((x > 0) and (y < 0)):
	    angle = -1*angle - 90
	
	print(angle)

	#pythag to get the distance
	distance = math.sqrt((x*x) + (y*y))
	print (distance)

	dp.rotateBy(self.drone, self.connection, angle, self.height)

	#dp.incrementForward_for(self.drone,self.height,5, 0.1)	

	dp.incrementForward(self.drone,self.height,distance)
	dp.hover_for(self.drone, self.height, time)

	dp.rotateBy(self.drone, self.connection, 180, self.height)
	#incrementForward_for(self.drone,self.height,5, 0.1)	
	dp.incrementForward(self.drone,self.height,distance*0.85)


  
	    	
    def hoverAboveBase(self, height):
        dp.takeoff(self.drone,height)
	
	print("rot")
	self.rotDrone2Base(height)
	
	self.land(self.drone,height)
	dp. hover2(self.drone,0,0.3)

	dp. hover2(self.drone,2,0.3)
	dp.closeConnection(self.drone)

	
    def testFlight(self):
	dp.takeoff(self.drone, self.height)
	dp.hover_for(self.drone, self.height, 10)

	self.searchForBase2()

	#------------------------------------------------#
	#self.flyFromBaseTo(0.5,0.5)
	#self.flyFromBaseTo(-0.5,0.5)
	#self.flyFromBaseTo(-0.5,-0.5)
	#self.flyFromBaseTo(0.5,-0.5)
	#------------------------------------------------#
	dp.hover_for(self.drone, 0.25, 10)	
	dp.hover_for(self.drone, 0.2, 10)
	#dp.land(self.drone, self.height)      

    #this funciton will bring the drone into land
    #currently it is assumed that GPS has brought in the drone
    #close enough to do a close proximity search
    def bringDroneHome(self,height):
	if (self.searchForBase()):
	    self.land(height)
		

    #gets the drones position with safety incase loss of drone image
    def getPosition(self,height):

	#counts if the camera uses the drone
	#if counter gets too high the landing aborts
	lostDrone = 0
        while(True):
	    if (lostDrone > 3):
	        print("no drone detected")
	        return None
	
	    dp.hover(self.drone,self.height)
	    pos = self.camera.readStream()
	
            if (pos == None):
	        lostDrone += 1
	    else:
	       	return pos      

    #aligns the drone to the center
    def moveTowardsCenter(self, height, axis, increment, pos):
        #pos = self.getPosition(height)

        if pos == None:
             return None
	accuracy = self.LANDING_ACCURACY;
	
	if (axis == "x"):	   
   	    pos = pos.x

	    if (pos < (self.GOAL_POS+30-accuracy)):
		print(">>>MOVE RIGHT<<<")
		dp.incrementRight(self.drone,height,increment)

	    elif (pos > (self.GOAL_POS+30+accuracy)):
		print(">>>MOVE LEFT<<<")
		dp.incrementLeft(self.drone,height,increment)
		
        elif (axis == "y"):
	    pos = pos.y
	    if (pos < (self.GOAL_POS-30-accuracy)):
	        dp.incrementBackward(self.drone,height,increment)
		print(">>>MOVE DOWN<<<")
	
	    elif (pos > (self.GOAL_POS-30+accuracy)):
		dp.incrementForward(self.drone,height,increment)
		print(">>>MOVE UP<<<")

    #logic used to check drones alignment
    def checkAlignment(self,height,axis,accuracy ,pos):
        #pos = self.getPosition(height)
		
	if (pos != None):
	    print("checking alignment")
   	    print(self.GOAL_POS+45+accuracy)
	    print(self.GOAL_POS+45-accuracy)
	    if (axis == "x"):
	        if ( (pos.x < (self.GOAL_POS+30+accuracy)) and (pos.x > (self.GOAL_POS+30-accuracy)) ):
		    print("X axis aligned")
		    return True
			
            elif (axis == "y"):
	        if ( (pos.y < (self.GOAL_POS-30+accuracy)) and (pos.y > (self.GOAL_POS-30-accuracy)) ):
		    print("Y axis aligned")
		    return True
		
	    elif (axis == "center"):
	        if ( (pos.x < (self.GOAL_POS+30+accuracy)) and (pos.x > (self.GOAL_POS+30-accuracy))
		and (pos.y < (self.GOAL_POS+accuracy-30)) and (pos.y > (self.GOAL_POS-30-accuracy))):
	            print("centered")
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
	
	checkRot = 0;	

        while(True):
	    dp.hover(self.drone,height)
	
	    checkRot += 1

	    if checkRot > 7: 
		self.rotDrone2Base(height)
		checkRot = 0

            pos = self.getPosition(height)
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

    #blind spiral method- spirals out until it finds the base
    def searchForBase2(self):	
	dp.hover(self.drone,self.height)
	i = 1;
	count = 1
	
	while (i < 360):
	    #roll = 0.1*math.cos(math.radians(i))
	    roll =(600/(i+30))
	    thrust = 0.1
	    print(roll)
	    print(i)
	    for _ in range(10):	
		if self.debug: print("Checking for Drone")
	       	    
		pos = self.camera.readStream()
		print(pos)
		print("^^ Pos ^^")
		
		if ((i > 1) and (pos!= None)):
		    if self.debug: print("Base found")
		    dp.hover(self.drone,self.height)	
	       	    return True;
		     
			
		self.drone.commander.send_hover_setpoint(thrust,0,roll,self.height)
        	time.sleep(0.1)
		
		
	    i = i +1

	return False
	    
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

    def rotDrone2Base(self,height):
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
	    #print("not pos1 lock")
	    return False

	#print("Pos 1: ")
	#print(pos1)
		
	dp.incrementForward(self.drone,height, 0.1)
	dp.hover(self.drone,height)
		
	#record P2
	pos2 = self.getPosition(height)

	if pos2 == None:	
	    #print("not pos2 lock")
	    return False

	#print("Pos2: ")
	#print(pos2)

	
	x1 = pos1.x
	y1 = pos1.y
	x2 = pos2.x
	y2 = pos2.y


	#points of the trinangle
	P12 = math.sqrt(math.pow((x2-x1),2)+math.pow((y2-y1),2))
	P31= math.sqrt(math.pow((x3-x2),2)+math.pow((y3-y2),2))
	P23 = math.sqrt(math.pow((x3-x1),2)+math.pow((y3-y1),2))
	
	#print(P12)
	#print(P23)
	#print(P31)

	#calculate compensation angle
	try:  
	    top = (P12*P12)+(P23*P23)-(P31*P31)
	    bottom = (2*P12*P23)

	    angle = math.degrees(math.acos(top/bottom))

	    #print("X1:")
	    #print(x1)
	    #print("x2:")
	    #print(x2)
	
	    #print("Aliging Drone")

	    if x2 < x1:
	    	angle = -1*angle

	    #print("angle:")
	    #print(angle)

	    dp.rotateBy(self.drone,self.connection,angle,height)

	except ZeroDivisionError:
	    print("something ducked up")
	
	#dp.incrementBackward(self.drone,height, 0.1)

	



    

    
        