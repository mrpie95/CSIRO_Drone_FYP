import numpy as np
import cv2
import time
import threading
import dataTypes

from Tkinter import *
from picamera import PiCamera
from picamera.array import PiRGBArray


#this class is in chrage of processing a live stream of data
#from the raspberry pi camera. 
class imageProcessing():
    
    #camera input - raspberry pi camera 
    cam = PiCamera()
    videoStream = None
    resolution = (310, 220)
    
    #HSV color range for blue and green LEDs used on the drone
    blueUpper = np.array([120, 255, 255])
    blueLower = np.array([100, 40, 140])
    
    greenUpper = np.array([95, 255, 255])
    greenLower = np.array([30, 100, 100])
    
    x = None
    y = None
    radius = None
    
    #initial variables
    def __init__(self, resolution):
        self.cam.resolution = resolution
        self.cam.exposure_mode = 'backlight'
        self.cam.vflip = True
        self.cam.exposure_compensation = 25
        self.cam.framerate = 60
        self.videoStream = PiRGBArray(self.cam, size=self.resolution)

    #image processing required to get a specificColour
    def processImage(self, image, color):
        
        processedImage = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        #processing for HSV ranges
        if color=="blue":
            processedImage = cv2.inRange(processedImage, self.blueLower, self.blueUpper)
        elif color=="green":
            processedImage = cv2.inRange(processedImage, self.greenLower, self.greenUpper)
	
	#futher processing for smoothing contours
	processedImage = cv2.erode(processedImage, None, iterations=2)
	processedImage = cv2.dilate(processedImage, None, iterations=2)
	
	return processedImage;
    
    #calculate the position of largest contour in the image
    def calculatePosition(self, image, color):
        x = None
        y = None
        radius = None
        
         #find all countour in the image
        cnts = cv2.findContours(image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
        
        #print("len = " + str(len(cnts)))
        if len(cnts) > 0:
            #use only the largest contour
            c = max(cnts, key=cv2.contourArea)
            ((x,y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            #decrease the radius
            
            #if (color=="blue"):
             #   radius = radius * 0.8
            
            if radius > 0:
                #exception handeling for devision by zero
                try:
                    x = int(M["m10"] / M["m00"])
                    y = int(M["m01"] / M["m00"])
                    radius = int(radius)                    
                
                    center = (self.x, self.y)
                    return (x,y,radius)
                
                except ZeroDivisionError, Argument:
                    print("error")
                    
        return None
        
    #read video stream from camera and return position of
    #largest contour
    def readStream(self):
        currentPos = None
        currentFrame = None
        image = None
        processedImage = None
        
        self.cam.capture(self.videoStream, format="bgr", use_video_port=True)
  
        image = self.videoStream.array
        HUD = image.copy()
        
        blueImage = self.processImage(image, "blue")
        bluePos = self.calculatePosition(blueImage, "blue")
      #  if bluePos!=None:
       #     cv2.circle(image, (bluePos[0], bluePos[1]), bluePos[2], (0,255,255),thickness=10,lineType=8, shift=0)
                
        greenImage = self.processImage(image, "green")
        greenPos = self.calculatePosition(greenImage, "green")
        position = None
        
        if greenPos!=None and bluePos!=None:
            
            posX = abs(bluePos[0]-greenPos[0])
            posY = abs(bluePos[1]-greenPos[1])
            posR = (bluePos[2]+greenPos[2])/2
            
            if bluePos[0] < greenPos[0]:
                posX = posX/2+bluePos[0]
                posY = posY/2+bluePos[1]
            elif bluePos[0] > greenPos[0]:
                posX = posX/2+greenPos[0]
                posY = posY/2+greenPos[1]
            
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img=HUD, text=("x: "+str(posX)+" y: "+str(posY)), org=(posX+50,posY), fontFace=font, color=(255,255,255),fontScale=0.5, lineType=cv2.LINE_AA)
            
                
            currentPos = dataTypes.droneData(x=posX, y=posY, z=posR, direction=None, blueX=bluePos[0], blueY=bluePos[1],
                                             blueZ=bluePos[2], greenX=greenPos[0], greenY=greenPos[1], greenZ=greenPos[2], detected=False, inRadius=False)
            position = (posY,posX,posR)
            cv2.circle(HUD, (position[1], position[0]), position[2], (0,255,255),thickness=-10,lineType=8, shift=0)
            
        """if (bluePos!=None):
            print("x: "+str(bluePos[0])+" y: "+str(bluePos[1])+" radius: "+str(bluePos[2]))
        
        if (greenPos!=None):
            print("x: "+str(greenPos[0])+" y: "+str(greenPos[1])+" radius: "+str(greenPos[2])) """  
        center = (int(self.resolution[0]/2),int(self.resolution[1]/2))
        radius = 50
        
        if currentPos != None:
            if currentPos.x < (center[0]+radius/2) and currentPos.x > (center[0]-radius/2) and currentPos.y < (center[1]+radius/2) and currentPos.y > (center[1]-radius/2):
                cv2.circle(HUD, center, radius, (55,255,125),thickness=10,lineType=8, shift=0)
                currentPos = dataTypes.droneData(x=posX, y=posY, z=posR, direction=None, blueX=bluePos[0], blueY=bluePos[1],
                                             blueZ=bluePos[2], greenX=greenPos[0], greenY=greenPos[1], greenZ=greenPos[2], detected=True, inRadius=True)
            else:
                cv2.circle(HUD, center, radius, (255,255,255),thickness=10,lineType=8, shift=0)
                currentPos = dataTypes.droneData(x=posX, y=posY, z=posR, direction=None, blueX=bluePos[0], blueY=bluePos[1],
                                             blueZ=bluePos[2], greenX=greenPos[0], greenY=greenPos[1], greenZ=greenPos[2], detected=True, inRadius=False)
        else:
            cv2.circle(HUD, center, radius, (3,225,225),thickness=10,lineType=8, shift=0)
        
        cv2.imshow("Blue Processing", blueImage)
        cv2.imshow("Green Processing", greenImage)
        cv2.imshow("HUD", HUD)
        
        
        cv2.imshow("Original", image)
        key = cv2.waitKey(1) & 0xFF

        self.videoStream.truncate()
        self.videoStream.seek(0)
            
        return currentPos
        


