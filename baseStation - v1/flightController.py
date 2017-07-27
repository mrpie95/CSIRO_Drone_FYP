import math
import dataTypes as dt



class flightController:
    goalPos = None
    #currentPos = None
    #targetPos = None
    droneData = None
    
    
    def __init__(self, resolution,goalPos):
        self.goalPos = goalPos
    
    def getDirection(self):
        dirErr = 3
        direction = None
        #print(self.droneData)
       
        bluePos = dt.position(x=self.droneData.blueX, y=self.droneData.blueY, z=self.droneData.blueZ)
        greenPos = dt.position(x=self.droneData.greenX, y=self.droneData.greenY, z=self.droneData.greenZ)
        
        X=float(abs(bluePos.x-greenPos.x))
        Y=float(abs(bluePos.y-greenPos.y))
        #print("---")
        #print(bluePos)
       # print(greenPos)
        #print(X)
        #print(Y)
           
        #print(math.degrees(math.atan(26.01/124.09)))
        result = None
       
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
    
    def getTargetPos(self, droneData):
        self.droneData = droneData
        
        #get angle of the drone: 0 is when the drone ready for landing
        direction = self.getDirection()
        
        return None
    
    
        