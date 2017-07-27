import logging
import time
import cflib

from threading import Thread
from collections import namedtuple
from cflib.crazyflie import Crazyflie

logging.basicConfig(level=logging.ERROR)


class DroneController:
    """Example that connects to a Crazyflie and ramps the motors up/down and
    the disconnects"""

    def __init__(self):
        # Initialize the low-level drivers (don't list the debug drivers)
        cflib.crtp.init_drivers(enable_debug_driver=False)

        print('Scanning interfaces for Crazyflies...')
        available = cflib.crtp.scan_interfaces()
        print('Crazyflies found:')

        count = 0;
        for i in available:
            print('%d - %s' % (count, i[0]))
            count += 1

        j = input('Choose a flie: ')

        if (not(j < 0)) and (not(j>len(available))):

            if len(available) > 0:
                link_uri = available[j][0]
            
                #""" Initialize and run the example with the specified link_uri 

                self._cf = Crazyflie()

                self._cf.connected.add_callback(self._connected)
               #self._cf.disconnected.add_callback(self._disconnected)
                #self._cf.connection_failed.add_callback(self._connection_failed)
                #self._cf.connection_lost.add_callback(self._connection_lost)

                self._cf.open_link(link_uri)

                print('Connecting to %s' % link_uri)
                
            else:
                print('No Crazyflies found')
        else:
            print('You chose an invalid flie!')
 
    def _connected(self, link_uri):
        print("Connected to crazyflie")
       # Thread(target=self._ramp_motors).start()
    #1def calculate
    def setMotors(self):
        #unlocks drone - allows the use of the setpoint command
        #self._cf.commander.send_setpoint(roll, pitch, yawrate, thrust)
        
        self._cf.commander.send_setpoint(0, 0, 0, 0)
        	
        self._cf.commander.send_setpoint(0, 0, 0, 10000)
        #time.sleep(0.05)

    def _ramp_motors(self):
       	j = input('Choose a ramp: ')
        thrust_mult = 1
        thrust_step = 500
        thrust = 20000
        pitch = 0
        roll = 0
        yawrate = 0

        # Unlock startup thrust protection
        self._cf.commander.send_setpoint(0, 0, 0, 0)

    	print('Unlocked')


        while thrust >= 20000:
        	
            self._cf.commander.send_setpoint(roll, pitch, yawrate, thrust)
            print thrust
            time.sleep(0.1)
            if thrust >= j:
                thrust_mult = -1
            thrust += thrust_step * thrust_mult
        self._cf.commander.send_setpoint(0, 0, 0, 0)

        # Make sure that the last packet leaves before the link is closed
        # since the message queue is not flushed before closing
        time.sleep(0.1)
        self._cf.close_link()