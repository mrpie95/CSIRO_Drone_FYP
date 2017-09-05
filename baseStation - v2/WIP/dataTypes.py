from collections import namedtuple

#droneData = namedtuple("droneData", "x y z direction yellowX yellowY yellowZ greenX greenY greenZ detected inRadius")

droneData = namedtuple("droneData", "x y detected")

position = namedtuple("position", "x y z")

droneMovement = namedtuple("droneMovement", "pitch roll yall")

drone2D = namedtuple("drone2D", "pitch roll")

pos2D = namedtuple("pos2D", "x y")

detectZone = namedtuple("detectZone", "north south east west")
