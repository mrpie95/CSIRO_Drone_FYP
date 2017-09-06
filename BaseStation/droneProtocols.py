oh also """These are the standard functions used to control the drone
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

INCREMENT_SIZE = 0.3
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
    print("hovering")	
    cf.commander.send_hover_setpoint(0,0,0,height+0.15)
    time.sleep(0.1)

    print("tookoff")
    for _ in range(10):	
        cf.commander.send_hover_setpoint(0.1,-0.05,0,height)
	time.sleep(0.1)
    hover(cf, height)

#lands the drone in a smooth but quick manner
def land(cf, height):
    droneHeight = height

    print("landing")
    for _ in range(10):	
        cf.commander.send_hover_setpoint(0,0,0,droneHeight)
	time.sleep(0.1)
        droneHeight = droneHeight - 0.05
    print("done")

#hovers the drone in place at a set height (m) and set time (mS)
def hover_for(cf, height, timeSet):
    print("hovering")
    for _ in range(timeSet):	
        cf.commander.send_hover_setpoint(0,0,0,height)
	time.sleep(0.1)
    print("done")

#hovers the drone in place at a set height (m) and set time (mS)
def hover(cf, height):
    print("hovering")
    for _ in range(1):	
        cf.commander.send_hover_setpoint(0,0,0,height)
	time.sleep(0.1)
    print("done")

#rotates the drone to the specified angle
def rotateTo(cf, scf, angle, height):
    print("rotating")
    
    while(True):
        droneAngle = getDirection(scf)
	print(droneAngle)
        print(angle)

	if ((angle <= (droneAngle+ANGLE_ACCURACY)) and (angle >= (droneAngle-ANGLE_ACCURACY))):
	    print("done")
	    break
	else:
            cf.commander.send_hover_setpoint(0,0,40,height)
	    time.sleep(0.1)

#moves the drone a set distance forward
def incrementForward(cf, height):
    for _ in range(10):	
        cf.commander.send_hover_setpoint(INCREMENT_SIZE,0,0,height)
        time.sleep(0.1)
    print("moved forward")

#moves the drone a set distance backward
def incrementBackward(cf, height):
    for _ in range(10):	
        cf.commander.send_hover_setpoint(-1*INCREMENT_SIZE,0,0,height)
        time.sleep(0.1)
    print("moved backward")



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

