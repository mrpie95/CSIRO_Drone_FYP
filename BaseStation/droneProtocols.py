"""These are the standard functions used to control the drone
over the base station. They have been specifically tuned to flying
over the 300mm x 300mm base station."""

import logging
import math
import time
import cflib.crtp
import logging

from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.crazyflie.syncLogger import SyncLogger

logging.basicConfig(level=logging.ERROR)

INCREMENT_SIZE = 0.02

ANGLE_ACCURACY = 7.5

#performs intialisations required the drone to fly
def initDrone(scf):
        cf = scf.cf
	cf.param.set_value('kalman.resetEstimation', '1')
        time.sleep(0.1)
	cf.param.set_value('kalman.resetEstimation', '0')
	time.sleep(2) 
	
	return cf

#closes the connection to the drone. Do this after each 
#the drone is landed.
def closeConnection(cf):
	cf.commander.send_stop_setpoint()

#take off compenstates for some of the drone drifting
def takeoff(cf, height):
    #print("hovering")	
    cf.commander.send_hover_setpoint(0,0,0,0.4)
    time.sleep(0.1)

    print("tookoff")
    for _ in range(10):	
        cf.commander.send_hover_setpoint(0.1,-0.05,0,height)
	time.sleep(0.1)
    hover(cf, height)

def takeoff2(cf, height):
    print("hovering")	
    cf.commander.send_hover_setpoint(0,0,0,0.4)
    time.sleep(0.1)

    print("tookoff")
    hover(cf, height)

def quickLand(cf, height):
  
    
   
    cf.commander.send_hover_setpoint(0,0,0,0)      
    

#lands the drone in a smooth but quick manner
def land(cf, height):
    droneHeight = height
    cf.commander.send_hover_setpoint(0,0,0,droneHeight)

    print("landing")
    for _ in range(10):	
        cf.commander.send_hover_setpoint(0,0,0,droneHeight)
	#time.sleep(0.02)
        droneHeight = droneHeight - 0.05
	if droneHeight < 0.35:
	    cf.commander.send_hover_setpoint(0,0,0,0)
	    break
    print("done")

#hovers the drone in place at a set height (m) and set time (mS)
def hover_for(cf, height, timeSet):
    #print("hovering")
    for _ in range(timeSet):	
        cf.commander.send_hover_setpoint(0,0,0,height)
	time.sleep(0.1)
    

#hovers the drone in place at a set height (m) and set time (mS)
def hover(cf, height):
    #print("hovering")
    for _ in range(1):	
        cf.commander.send_hover_setpoint(0,0,0,height)
	time.sleep(0.1)
 
#rotates the drone to the specified angle
def rotateBy(cf, scf, angle, height):
    print("rotating")
    droneAngle = getDirection(scf)
    finalAngle = droneAngle + angle

    #rate of rotation in deg/s
        
	
    if angle > 0:
    	rotRate = -40    
    else:
	rotRate = 40

    while(True):
        droneAngle = getDirection(scf)
	print(finalAngle)
	print(droneAngle)

        #if droneAngle >= finalAngle:
         #   rotRate = -1*rotRate

    	if ((finalAngle <= (droneAngle+ANGLE_ACCURACY)) and (finalAngle >= (droneAngle-ANGLE_ACCURACY))):
    	    break
    	else:
            cf.commander.send_hover_setpoint(0,0,rotRate,height)
    	    time.sleep(0.1)

#moves the drone a set distance forward
def incrementForward(cf, height, increment):
    for _ in range(10):	
        cf.commander.send_hover_setpoint(increment,0,0,height)
        time.sleep(0.1)
    print("moved forward")

#moves the drone a set distance backward
def incrementBackward(cf, height, increment):
    for _ in range(10):	
        cf.commander.send_hover_setpoint(-1*increment,0,0,height)
        time.sleep(0.1)
    print("moved backward")

#moves the drone a set distance forward
def incrementRight(cf, height, increment):
    for _ in range(10):	
        cf.commander.send_hover_setpoint(0,-1*increment,0,height)
        time.sleep(0.1)
    print("moved right")

#moves the drone a set distance backward
def incrementLeft(cf, height, increment):
    for _ in range(10):	
        cf.commander.send_hover_setpoint(0,increment,0,height)
        time.sleep(0.1)
    print("moved left")



#general purpose logging function - can be used for any 
#variable in the drones LOC
def logParameter(scf, parameter, Type):
    data = LogConfig(name='data', period_in_ms=10)
    data.add_variable(parameter, Type)
    #logs data through drone connnection
    with SyncLogger(scf, data) as logger:
        for log_entry in logger:
            data = log_entry[1]    
            return data[parameter] 
            break

#gets the current relative direction of the drone
#NOTE ADD AVERAGING FUNCITON FOR ACCURACY
def getDirection(scf):
    data = LogConfig(name='data', period_in_ms=10)
    data.add_variable('stabilizer.yaw', 'float')
    
    with SyncLogger(scf, data) as logger:   
        for log_entry in logger:
            #timestamp = log_entry[0]
            data = log_entry[1]
            #logconf_name = log_entry[2]

	    return data['stabilizer.yaw'] 
            break

