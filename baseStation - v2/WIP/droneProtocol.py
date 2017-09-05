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


INCREMENT_SIZE = 0.3
ANGLE_ACCURACY = 7.5

def wait(time):
    time.sleep(time)

#performs intialisations required the drone to fly
def initDrone(scf):
        cf = scf.cf
	cf.param.set_value('kalman.resetEstimation', '1')
        time.sleep(0.1)
	cf.param.set_value('kalman.resetEstimation', '0')
	time.sleep(2) 
	
	return cf

def closeConnection(cf):
	cf.commander.send_stop_setpoint()

#gives the angle that will straghten the drone relative to the base
def angleCompensation(x1,y1,x2,y2, wall):
    X=float(abs(x1-x2))
    Y=float(abs(y1-y2))
    result = None
	

    try:
        angle = math.degrees(math.atan(Y/X))

	#south wall
	if wall.south:
	    if ((x1>=x2)and(y1>=y2)):
                result = -1*angle
	    elif ((x1<=x2)and(y1>=y2)):
	        result = angle

	#east wall
	elif wall.east:
	    if ((x1>=x2)and(y1<=y2)):
	        result = (-1*(angle+90))
	    elif ((x1>=x2)and(y1>=y2)):
	        result = -1*(90-angle)

	#north wall
	if wall.north:
 	    if ((x1<=x2)and(y1<=y2)):
	        result = (180-angle)
	    elif ((x1>=x2)and(y1<=y2)):
	        result = (-1*(180-angle))

	#west wall
	elif wall.west:
	    if ((x1<=x2)and(y1>=y2)):
	        result = (90-angle)
	    elif ((x1<=x2)and(y1<=y2)):
	        result = (angle+90)
          
    except ZeroDivisionError:
        return "error"

    if result == None:
        return None

    if result >= 360:
	result -= 360

    return result

def getDirection(scf):
	result = None
	data = LogConfig(name='data', period_in_ms=10)
   	data.add_variable('stabilizer.yaw', 'float')
	#data.add_variable('range.zrange', 'uint16_t')
	
	with SyncLogger(scf, data) as logger:
            #endTime = time.time() + 10		
	
            for log_entry in logger:
                #timestamp = log_entry[0]
                data = log_entry[1]
                #logconf_name = log_entry[2]
	
	        result = data['stabilizer.yaw'] 
                #print(data['stabilizer.yaw'])
                #print(timestamp)
	        break
                     
                #if time.time() > endTime:
                    # break
	
	return result

#take off the compenstates for some of the drone drifting
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
def hover_quick(cf, height, timeSet):
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

def rotateTo(cf, scf, angle, height):
    print("rotating")
    
    i = 0

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