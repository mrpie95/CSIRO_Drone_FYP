import logging
import time
from threading import Thread

import cflib
from cflib.crazyflie import Crazyflie

logging.basicConfig(level=logging.ERROR)


class MotorRampExample:
    """Example that connects to a Crazyflie and ramps the motors up/down and
    the disconnects"""

    def __init__(self, link_uri):
        """ Initialize and run the example with the specified link_uri """

        self._cf = Crazyflie()

        self._cf.connected.add_callback(self._connected)
        self._cf.disconnected.add_callback(self._disconnected)
        self._cf.connection_failed.add_callback(self._connection_failed)
        self._cf.connection_lost.add_callback(self._connection_lost)

        self._cf.open_link(link_uri)

        print('Connecting to %s' % link_uri)

    def _connected(self, link_uri):
        Thread(target=self._ramp_motors).start()

    def _connection_failed(self, link_uri, msg):
        print('Connection to %s failed: %s' % (link_uri, msg))

    def _connection_lost(self, link_uri, msg):
        print('Connection to %s lost: %s' % (link_uri, msg))

    def _disconnected(self, link_uri):
        print('Disconnected from %s' % link_uri)

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
        	
            self._cf.commander.send_setpoint(roll, thrust, yawrate, 0)
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


if __name__ == '__main__':
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

		    le = MotorRampExample(available[0][j])
		else:
		    print('No Crazyflies found')
    else:
		print('You chose an invalid flie!')
