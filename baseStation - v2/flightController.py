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
       
        yellowPos = dt.position(x=self.droneData.yellowX, y=self.droneData.yellowY, z=self.droneData.yellowZ)

        greenPos = dt.position(x=self.droneData.greenX, y=self.droneData.greenY, z=self.droneData.greenZ)
        
        X=float(abs(yellowPos.x-greenPos.x))
        Y=float(abs(yellowPos.y-greenPos.y))

        try:
            if (yellowPos.x < greenPos.x and yellowPos.y < greenPos.y):
                return math.degrees(math.atan(X/Y))+90
           # elif (yellowPos.x < greenPos.x and (yellowPos.y < (greenPos.y+dirErr) and yellowPos.y > (greenPos.y-dirErr))):
            #    return 45
            elif (yellowPos.x < greenPos.x and yellowPos.y > greenPos.y):
                return math.degrees(math.atan(X/Y))+135
            #elif ((yellowPos.x < (greenPos.x+dirErr) and (yellowPos.x < (greenPos.x+dirErr))) and (yellowPos.y < greenPos.y)):
             #   return 135
            elif (yellowPos.x > greenPos.x and yellowPos.y > greenPos.y):
                return math.degrees(math.atan(X/Y))+180
            #elif (yellowPos.x > greenPos.x and (yellowPos.y < (greenPos.y+dirErr) and yellowPos.y > (greenPos.y-dirErr))):
            #    return 225
            elif (yellowPos.x > greenPos.x and yellowPos.y < greenPos.y):
                return math.degrees(math.atan(X/Y))+225
            #elif (yellowPos.x < greenPos.x and (yellowPos.y < (greenPos.y+dirErr) and yellowPos.y > (greenPos.y-dirErr))):
            #    return 315
        except ZeroDivisionError:
            return "error"

        #return result
    
    def __init__(self, resolution,goalPos, currentPos):
        self.droneData = currentPos
        self.goalPos = goalPos
        self.initDirection = self.getDirection()
    
    def angleCompensation(self):
        angle = self.getDirection()
        return dt.drone2D(pitch=math.sin(angle), roll=math.cos(angle))
         
        
    
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

    
    
        