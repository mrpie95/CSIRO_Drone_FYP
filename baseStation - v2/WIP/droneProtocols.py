"""These are the standard functions used to control the drone
over the base station. They have been specifically tuned to flying
over the 300mm x 300mm base station."""

import time

INCREMENT_SIZE = 0.3

def wait(time)
    global.time.sleep(time)

#performs intialisations required the drone to fly
def initialiseDrone(scf):
        cf = scf.cf
	cf.param.set_value('kalman.resetEstimation', '1')
        global.time.sleep(0.1)
	cf.param.set_value('kalman.resetEstimation', '0')
	wait(2) 
	return cf

#take off the compenstates for some of the drone drifting
def takeoff(cf, height):
    print("hovering")	
    cf.commander.send_hover_setpoint(0,0,0,height+0.15)
    wait.(0.1)

    print("tookoff")
    for _ in range(10):	
        cf.commander.send_hover_setpoint(0.1,-0.05,0,height)
	wait.(0.1)
    hover(cf, height)

#lands the drone in a smooth but quick manner
def land(cf, height):
    droneHeight = height

    print("landing")
    for _ in range(10):	
        cf.commander.send_hover_setpoint(0,0,0,droneHeight)
	wait.(0.1)
        droneHeight = droneHeight - 0.05
    print("done")

#hovers the drone in place at a set height
def hover(cf, height, log):
    print("hovering")
    for _ in range(40):	
	if(log):
	    print(getDireciton(scf))

        cf.commander.send_hover_setpoint(0,0,0,height)
	wait.(0.1)
    print("done")

#moves the drone a set distance forward
def incrementForward(cf, height):
    for _ in range(10):	
        cf.commander.send_hover_setpoint(INCREMENT_SIZE,0,0,height)
        wait.(0.1)
    print("moved forward")

#moves the drone a set distance backward
def incrementBackward(cf, height):
    for _ in range(10):	
        cf.commander.send_hover_setpoint(-1*INCREMENT_SIZE,0,0,height)
        wait.(0.1)
    print("moved backward")