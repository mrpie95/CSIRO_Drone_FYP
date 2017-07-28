import math
import dataTypes as dt



class flightController:
    goalPos = None
    #currentPos = None
    #targetPos = None
    droneData = None
    moveMag = 5 #movement mangnitude - degrees
    initDirection = 0
    ready = False
    
    def getDirection(self):
        dirErr = 3
        direction = None
        #print(self.droneData)
       
        bluePos = dt.position(x=self.droneData.blueX, y=self.droneData.blueY, z=self.droneData.blueZ)
        greenPos = dt.position(x=self.droneData.greenX, y=self.droneData.greenY, z=self.droneData.greenZ)
        
        X=float(abs(bluePos.x-greenPos.x))
        Y=float(abs(bluePos.y-greenPos.y))

        try:
            if (bluePos.x < greenPos.x and bluePos.y < greenPos.y):
                return math.degrees(math.atan(X/Y))
           # elif (bluePos.x < greenPos.x and (bluePos.y < (greenPos.y+dirErr) and bluePos.y > (greenPos.y-dirErr))):
            #    return 45
            elif (bluePos.x < greenPos.x and bluePos.y > greenPos.y):
                return math.degrees(math.atan(X/Y))+45
            #elif ((bluePos.x < (greenPos.x+dirErr) and (bluePos.x < (greenPos.x+dirErr))) and (bluePos.y < greenPos.y)):
             #   return 135
            elif (bluePos.x > greenPos.x and bluePos.y > greenPos.y):
                return math.degrees(math.atan(X/Y))+90
            #elif (bluePos.x > greenPos.x and (bluePos.y < (greenPos.y+dirErr) and bluePos.y > (greenPos.y-dirErr))):
            #    return 225
            elif (bluePos.x > greenPos.x and bluePos.y < greenPos.y):
                return math.degrees(math.atan(X/Y))+135
            #elif (bluePos.x < greenPos.x and (bluePos.y < (greenPos.y+dirErr) and bluePos.y > (greenPos.y-dirErr))):
            #    return 315
        except ZeroDivisionError:
            return "error"

        return result
    
    def __init__(self, resolution,goalPos, currentPos):
        self.droneData = currentPos
        self.goalPos = goalPos
        self.initDirection = self.getDirection()
    
    def angleCompensation(self):
        angle = self.getDirection()
        return dt.drone2D(pitch=math.sin(angle), roll=math.cose(angle))
         
        
    
    def getMovementVector(self, goalPos):
        pitch = 0
        roll = 0
        yall = 0
        
        angleComp = self.angleCompensation()
        
        if (self.droneData.x > goalPos[0]):
            pitch = 5
        else:
            pitch = -5
        
        if (self.droneData.y > goalPos[1]):
            roll = 5
        else:
            roll = -5
        
        pitch = pitch*angleCom.x
        roll = pitch*angleCom.x
        
        return dt.droneMovment(pitch=pitch, roll=roll, yall=yall)

    
    
        