import logging
import time
import cflib
import sys

from threading import Thread
from collections import namedtuple
from cflib.crazyflie import Crazyflie

import imageProcessing as ip
import droneController as dc
import dataTypes as dt
import flightController as fc

from cflib.crazyflie.log import LogConfig

logging.basicConfig(level=logging.ERROR)

class BaseStation:
    """Example that connects to a Crazyflie and ramps the motors up/down and
    the disconnects"""
    
    connected = False

    def __init__(self):
        
        # Initialize the low-level drivers (don't list the debug drivers)
        cflib.crtp.init_drivers(enable_debug_driver=False)
        # Scan for Crazyflies and use the first one found
        print('Scanning interfaces for Crazyflies...')
        available = cflib.crtp.scan_interfaces()
        print('Crazyflies found:')
        for i in available:
            print(i[0])
        
        j = input('Choose a flie: ')

        link_uri = None
        
        if len(available) > 0:
            link_uri = available[j][0]
            #le = MotorRampExample(available[j][0])
        else:
            print('No Crazyflies found, cannot run example')
        
        """ Initialize and run the example with the specified link_uri """

        self._cf = Crazyflie()

        self._cf.connected.add_callback(self._connected)
        self._cf.disconnected.add_callback(self._disconnected)
        self._cf.connection_failed.add_callback(self._connection_failed)
        self._cf.connection_lost.add_callback(self._connection_lost)

        self._cf.open_link(link_uri)

        print('Connecting to %s' % link_uri)

    def _connected(self, link_uri):
        """ This callback is called form the Crazyflie API when a Crazyflie
        has been connected and the TOCs have been downloaded."""

        self.connected = True
        # Start a separate thread to do the motor test.
        # Do not hijack the calling thread!
        #Thread(target=self._ramp_motors).start()

    def _connection_failed(self, link_uri, msg):
        """Callback when connection initial connection fails (i.e no Crazyflie
        at the specified address)"""
        print('Connection to %s failed: %s' % (link_uri, msg))

    def _connection_lost(self, link_uri, msg):
        """Callback when disconnected after a connection has been made (i.e
        Crazyflie moves out of range)"""
        print('Connection to %s lost: %s' % (link_uri, msg))

    def _disconnected(self, link_uri):
        """Callback when the Crazyflie is disconnected (called in all cases)"""
        print('Disconnected from %s' % link_uri)

    def unlockMotors(self):
        self._cf.commander.send_setpoint(0, 0, 0, 0)

    def changeMotor(self):
        #Thread(target=self._ramp_motors).start()
        self._cf.commander.send_setpoint(0, 0, 0, 35000)
        #print('fly')
        
    def _ramp_motors(self):
        thrust_mult = 1
        thrust_step = 500
        thrust = 20000
        pitch = 0
        roll = 0
        yawrate = 0

        # Unlock startup thrust protection
        self._cf.commander.send_setpoint(0, 0, 0, 0)
        i =0
        
        while i < 250:
            #self.changeMotor()
            self._cf.commander.send_setpoint(0, 0, 0, 40000)
            i += 1
            print(i)
        time.sleep(0.1)
        self._cf.close_link()

if __name__ == '__main__':
   test = BaseStation()
   i=0
   
   unlock = False
   
   resolution = (320,224)
   goalPos = dt.pos2D(resolution[0]/2, resolution[1]/2)
   init = True
   takeoffTimer = 0
    
   image = ip.imageProcessing(resolution)
   
   #test code used for debuggin connectin issue of drone 
   while True:
       print(test.connected)
       
       if (test.connected):
           if not unlock:
               test.unlockMotors()
           
           unlock = True
           #test._ramp_motors()
           test.changeMotor()
           #break