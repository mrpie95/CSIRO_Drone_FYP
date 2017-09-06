import numpy as np
import cv2
import time
import threading
import dataTypes as dt

from Tkinter import *
from picamera import PiCamera
from picamera.array import PiRGBArray


#this class is in chrage of processing a live stream of data
#from the raspberry pi camera. 
class imageProcessing():

    FONT = cv2.FONT_HERSHEY_SIMPLEX #font used in project
    SCREEN_WIDTH = 300				
    SCREEN_HEIGHT = SCREEN_WIDTH	
    RESOLUTION = (SCREEN_WIDTH,SCREEN_HEIGHT)    

    #area on the edge of the screen used in the detection of the drone
    DETECTION_ZONE = 30
    #point definitions for each area
    NORTH_PT1 = (0,0)
    NORTH_PT2 = (SCREEN_WIDTH,DETECTION_ZONE)
    EAST_PT1 = (SCREEN_WIDTH-DETECTION_ZONE,0)
    EAST_PT2 = (SCREEN_WIDTH,SCREEN_HEIGHT)
    SOUTH_PT1 = (0,SCREEN_HEIGHT-DETECTION_ZONE)
    SOUTH_PT2 = (SCREEN_WIDTH,SCREEN_HEIGHT)
    WEST_PT1 = (0,0)
    WEST_PT2 = (DETECTION_ZONE,SCREEN_HEIGHT)

    #Colours definitions
    BLUE = (255,0,0)
    GREEN = (0,255,0)
    RED = (0,0,255)
    YELLOW = (0,255,255)
    WHITE = (255,255,255)
  
    #Upper and lowers range for colour dection
    YELLOW_UPPER = np.array([84,255,255])
    YELLOW_LOWER = np.array([26,93,93])

    #camera input - raspberry pi camera 
    cam = PiCamera()
    videoStream = None
    debug = False    
    
    #HSV color range for blue and green LEDs used on the drone
    yellowUpper = YELLOW_UPPER
    yellowLower = YELLOW_LOWER
    
    #used in creating trackbars    
    def nothing(self, x):
        pass

    #initial variables
    def __init__(self, resolution, debug):

    	#settings used for camera caputring
	self.debug = debug
        self.cam.resolution = resolution
        self.cam.exposure_mode = 'backlight'
	self.cam.awb_mode = 'flash'
        self.cam.hflip = True
        self.cam.exposure_compensation = 25
        self.cam.framerate = 60
        self.videoStream = PiRGBArray(self.cam, size=self.RESOLUTION)
        
        #Sliders used to fine tune the colour detecitons
        if (self.debug):
            cv2.namedWindow('controls')
            
            cv2.createTrackbar('H-l', 'controls', 0,179, self.nothing)
            cv2.createTrackbar('S-l', 'controls', 0,255, self.nothing)
            cv2.createTrackbar('V-l', 'controls', 0,255, self.nothing)
            
            cv2.createTrackbar('H-u', 'controls', 0,179, self.nothing)
            cv2.createTrackbar('S-u', 'controls', 0,255, self.nothing)
            cv2.createTrackbar('V-u', 'controls', 0,255, self.nothing)

            cv2.setTrackbarPos('H-l', 'controls', self.yellowLower[0])
	    cv2.setTrackbarPos('S-l', 'controls', self.yellowLower[1])
            cv2.setTrackbarPos('V-l', 'controls', self.yellowLower[2])
            
            cv2.setTrackbarPos('H-u', 'controls', self.yellowUpper[0])
            cv2.setTrackbarPos('S-u', 'controls', self.yellowUpper[1])
            cv2.setTrackbarPos('V-u', 'controls', self.yellowUpper[2])
	    
    
    #image processing required to get a specificColour
    def processImage(self, image):
        
        #convert colout from BGR to HSV
        processedImage = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        #get values from user sliders
        if (self.debug):
	    self.yellowLower = np.array([cv2.getTrackbarPos('H-l','controls'), cv2.getTrackbarPos('S-l','controls'), cv2.getTrackbarPos('V-l','controls')])
  	    self.yellowUpper = np.array([cv2.getTrackbarPos('H-u','controls'), cv2.getTrackbarPos('S-u','controls'), cv2.getTrackbarPos('V-u','controls')])

        #processing creates a binary image containg only colours defined in the range
        processedImage = cv2.inRange(processedImage, self.yellowLower, self.yellowUpper)

	#morphilogical transforms used for smoothing
	processedImage = cv2.erode(processedImage, None, iterations=2)
	processedImage = cv2.dilate(processedImage, None, iterations=2)

	return processedImage;
    
    #draws the drone
    def drawDrone(self,image,x,y):
    	#draws a circle at the center of the drone
	cv2.circle(image, (x,y), 20, (20,255,255), thickness=-1,lineType=8, shift=0) 
	posX = x+40
        posY = y 
        cv2.putText(img=image, text=("x: "+str(x)+" y: "+str(y)), org=(x,y), fontFace=self.FONT, color=(255,255,255),fontScale=0.5, lineType=cv2.LINE_AA)

    #draws a HUD with useful debug information
    def drawHUD(self,image, north, east, south, west):
	colour = None
	
	#sets colour of north based on if the drone is there
	if (north):
	    colour = self.WHITE
	else:
	    colour = self.BLUE
	cv2.rectangle(img=image,pt1=self.NORTH_PT1, pt2=self.NORTH_PT2, color=colour, thickness=-1,lineType=8, shift=0)

 	#sets colour of east based on if the drone is there
	if (east):
	    colour = self.WHITE
	else:
	    colour = self.GREEN		
	cv2.rectangle(img=image,pt1=self.EAST_PT1, pt2=self.EAST_PT2, color=colour, thickness=-1,lineType=8, shift=0) 

	#sets colour of south based on if the drone is there
	if (south):
	    colour = self.WHITE
	else:
	    colour = self.RED	
	cv2.rectangle(img=image,pt1=self.SOUTH_PT1, pt2=self.SOUTH_PT2, color=colour, thickness=-1,lineType=8, shift=0)
		
	#sets colour of west based on if the drone is there
	if (west):
	    colour = self.WHITE
	else:
	    colour = self.YELLOW	
	cv2.rectangle(img=image,pt1=self.WEST_PT1, pt2=self.WEST_PT2,color=colour,thickness=-1,lineType=8, shift=0) 

    	#calculate the position of largest contour in the image
    def calculatePosition(self, image):
        x = None
        y = None
        radius = None
        
         #find all countour in the image
        cnts = cv2.findContours(image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
        
        if len(cnts) > 0:
            #use only the largest contour
            c = max(cnts, key=cv2.contourArea)
            ((x,y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
                        
            if radius > 0:
                #exception handeling for devision by zero
                try:
                    x = int(M["m10"] / M["m00"])
                    y = int(M["m01"] / M["m00"])
                    radius = int(radius)                    
                
                    #center = (x, self.y)
                    return (x,y,radius)
                
                except ZeroDivisionError, Argument:
                    print("error") 
        return None

    #checks if the drone is in any detection zones
    def checkZones(self,x,y):
        north = False;
        east = False
	south = False
	west = False
	    	
	#area checks for each zone
	if ((x > self.NORTH_PT1[0]) and (x < self.NORTH_PT2[0]) and (y > self.NORTH_PT1[1]) and (y < self.NORTH_PT2[1])):
	    north = True

	if ((x > self.EAST_PT1[0]) and (x < self.EAST_PT2[0]) and (y > self.EAST_PT1[1]) and (y < self.EAST_PT2[1])):
	    east = True
		
	if ((x > self.SOUTH_PT1[0]) and (x < self.SOUTH_PT2[0]) and (y > self.SOUTH_PT1[1]) and (y < self.SOUTH_PT2[1])):
	    south = True

	if ((x > self.WEST_PT1[0]) and (x < self.WEST_PT2[0]) and (y > self.WEST_PT1[1]) and (y < self.WEST_PT2[1])):
	    west = True
		
	return dt.detectZone(north=north, east=east, south=south, west=west)
		 

    #read video stream from camera and return position of
    #largest contour which is (usaully...) the drone
    def readStream(self):
        currentPos = None
        currentFrame = None
        image = None
        processedImage = None
	zones = None
		
	#creates a blank image that is used as a HUD
	HUD = np.zeros((self.RESOLUTION[0],self.RESOLUTION[1] ,3),dtype=np.uint8)
		
	#caputes an image from the camera
        self.cam.capture(self.videoStream, format="bgr", use_video_port=True)
        image = self.videoStream.array

        #get the binary image using the defined colour range
        yellowImage = self.processImage(image)

        #gets the position of the drone
        dronePos = self.calculatePosition(yellowImage)
        
        if dronePos!=None:
	    posX = dronePos[0]
            posY = dronePos[1]

            #draw drone
	    self.drawDrone(HUD, posX, posY)

	    #check all zones for drone and highlight them if the drone is in them 
            zones = self.checkZones(posX,posY)
	    self.drawHUD(HUD,zones.north,zones.east,zones.south,zones.west)
	    	
	    currentPos = dt.droneData(x=posX, y=posY, detected=zones)

	else:
	    self.drawHUD(HUD,False,False,False,False)        
    	
    	#draw all windows
    	cv2.imshow("Original", image)
	cv2.imshow("HUD", HUD)
	key = cv2.waitKey(1) & 0xFF

	#end the video stream
	self.videoStream.truncate()
	self.videoStream.seek(0)
	            
	return currentPos
	        


