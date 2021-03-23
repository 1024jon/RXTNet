import sys
import socket
import os
import time
import mmap

sys.path.append("/home/server/git/RXTNet/xled")
import xled

filename = '/tmp/fd0'
fd = os.open(filename, os.O_RDONLY)
buf = mmap.mmap(fd, 0, mmap.MAP_SHARED, mmap.PROT_READ)


#discovered_device = xled.discover.discover()
#print(discovered_device)

control_interface = xled.ControlInterface('192.168.3.218', '98:f4:ab:36:ae:39')
hicontrol = xled.HighControlInterface('192.168.3.218')
control_interface.set_mode('movie')
hicontrol.set_static_color(255,255,255)