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

filename2 = '/tmp/fd1'
fd = os.open(filename2, os.O_RDONLY)
buf2 = mmap.mmap(fd, 0, mmap.MAP_SHARED, mmap.PROT_READ)


#discovered_device = xled.discover.discover()
#print(discovered_device)

control_interface = xled.ControlInterface('192.168.3.218', '98:f4:ab:36:ae:39')
hicontrol = xled.HighControlInterface('192.168.3.218')

#ctx = common_preamble('192.168.3.218', '98:f4:ab:36:ae:39')
#log.debug("Get device info...")
response = control_interface.get_device_info()
number_of_led = response["number_of_led"]
led_profile = response["led_profile"]
bytes_per_led = len(led_profile)
max_frame = (bytes_per_led*number_of_led)
print("LED profile: {}".format(led_profile))
print("Format: {}".format(number_of_led))
print("Bytes per LED: {}".format(bytes_per_led))
print("Max Frame Size: {}".format(max_frame))
print("Max Packet Size: {}".format(max_frame+10))
#log.debug("Turning realtime on...")
control_interface.set_mode('rt')
print("Realtime turned on. Send packets to {}:7777".format(control_interface.host))
print("Authentication Token: {} / {}".format(
    control_interface._session.access_token,
    control_interface._session.decoded_access_token.hex()))
print("Open UDP Socket.")
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP

buf.seek(0)
buf2.seek(0)
i=0
while True:
    packet = bytearray(b'\x01')
    packet.extend(control_interface._session.decoded_access_token)
    packet.append(bytes_per_led)
    for l in range(0,number_of_led*bytes_per_led):
        if l <= 512:#512 - start channel?
            if l = 512 - 3 or l = 512 - 2:
                #next universe
                #break
            #start universe
            packet.append(ord(buf.read(1)))
        else:
            packet.append(ord(buf2.read(1)))
    buf.seek(0)
    buf2.seek(0)
    #print(packet)
    sock.sendto(packet, (control_interface.host, 7777))
    #print("Length: {}".format(len(packet)))
    #print("{}".format(packet.hex()))
    time.sleep(0.025)
    
def packetdata()