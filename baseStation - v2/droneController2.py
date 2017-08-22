import logging
import time
import cflib

from threading import Thread
from collections import namedtuple
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.crazyflie.log import LogConfig

logging.basicConfig(level=logging.ERROR)


class DroneController:
    initDirection = 0
    init = True
    batteryLvl = 0
    connected = False
    cf = None
    scf = None

    #HARD CODED drone frequecnies"
    URI = "radio://0/80/250K"
	
    def __init__(self):
        # Initialize the low-level drivers (don't list the debug drivers)
        cflib.crtp.init_drivers(enable_debug_driver=False)

	with SyncCrazyflie(self.URI) as self.scf:
	    self.initialiseDrone(self.scf)
	    self.runTest()   

	print("Drone initialised")

	   
    def initialiseDrone(self, scf):
        self.cf = scf.cf
	self.cf.param.set_value('kalman.resetEstimation', '1')
        time.sleep(0.1)
	self.cf.param.set_value('kalman.resetEstimation', '0')
	time.sleep(2) 
	
 
    def runTest(self):
	#cflib.crtp.init_drivers(enable_debug_driver=False)
	print("power on")
	self.cf.commander.send_hover_setpoint(0,0,0,0.05)
	
	#cf = self.scf.cf
	#if self.scf != None:
         #   print(self.scf)

	"""for _ in range(5):
            cf.commander.send_hover_setpoint(0,0,0,0.1)
            time.sleep(0.1)"""

 
	    
    