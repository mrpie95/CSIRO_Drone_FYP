import logging
import time
import cflib

from threading import Thread
from collections import namedtuple
from cflib.crazyflie import Crazyflie

from cflib.crazyflie.log import LogConfig

logging.basicConfig(level=logging.ERROR)


class DroneController:
    initDirection = 0
    init = True

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
        
        self._lg_stab = LogConfig(name='Stabilizer', period_in_ms=10)
       #self._lg_stab.add_variable('stabilizer.roll', 'float')
        #self._lg_stab.add_variable('stabilizer.pitch', 'float')
        self._lg_stab.add_variable('stabilizer.yaw', 'float')
        
        try:
            self._cf.log.add_config(self._lg_stab)
            # This callback will receive the data
            self._lg_stab.data_received_cb.add_callback(self.logStabData)
            
            
            # This callback will be called on errors
           # self._lg_acc.error_cb.add_callback(self._stab_log_error)
            # Start the logging
            self._lg_stab.start()
             
        except KeyError as e:
            print('Could not start log configuration,'
                  '{} not found in TOC'.format(str(e)))
        except AttributeError:
            print('Could not add Stabilizer log config, bad configuration.')
    
    def logStabData(self, timestamp, data, logconf):
        if self.init:
            self.initDirection = data['stabilizer.yaw']
         #   print(data['stabilizer.yaw'])
            self.init = False
        #print(data['stabilizer.yaw'])
        self.initDirection =  timestamp #data['stabilizer.yaw']
        #print('[%s]: %s\n' % (logconf.name, data))
        
        
        
        
       # Thread(target=self._ramp_motors).start()
    #1def calculate
    
       
    def setMotors(self, value):
        #unlocks drone - allows the use of the setpoint command
        #self._cf.commander.send_setpoint(roll, pitch, yawrate, thrust)
        print("motors on")
        
        self._cf.commander.send_setpoint(0, 0, 0, 0)
        time.sleep(0.1)
        self._cf.commander.send_setpoint(0, 0, 0, value)
        time.sleep(0.1)

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
        #self._cf.close_link()