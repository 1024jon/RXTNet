import sys
import mmap
import os

from socket import (socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR,SO_BROADCAST)
from struct import pack, unpack
from contextlib import suppress

UDP_IP = "192.168.255.255"
UDP_PORT = 6454

bufferlocation = '/tmp/'
bufferdict = {}
filedict = {}


class ArtnetPacket:

    ARTNET_HEADER = b'Art-Net\x00'

    def __init__(self):
        self.op_code = None
        self.ver = None
        self.sequence = None
        self.physical = None
        self.universe = None
        self.length = None
        self.data = None

    def __str__(self):
        return ("ArtNet package:\n - op_code: {0}\n - version: {1}\n - "
                "sequence: {2}\n - physical: {3}\n - universe: {4}\n - "
                "length: {5}\n - data : {6}").format(
            self.op_code, self.ver, self.sequence, self.physical,
            self.universe, self.length, self.data)

    def unpack_raw_artnet_packet(self, raw_data):

        if unpack('!8s', raw_data[:8])[0] != ArtnetPacket.ARTNET_HEADER:
            print("Received a non Art-Net packet")
            return None

        packet = ArtnetPacket()
        with suppress(Exception):
            (packet.op_code, packet.ver, packet.sequence, packet.physical,
                packet.universe, packet.length) = unpack('!HHBBHH', raw_data[8:18])

        with suppress(Exception):
            packet.data = unpack(
                '{0}s'.format(int(packet.length)),
                raw_data[18:18+int(packet.length)])[0]

        return packet


def listen_and_redirect_artnet_packets():
    print(("Listening in {0}:{1} and writing to memory buffers /tmp/fd# ").format(
        UDP_IP, UDP_PORT))

    sock = socket(AF_INET, SOCK_DGRAM)  # UDP
    sock.bind((UDP_IP, UDP_PORT))

    sock_broadcast = socket(AF_INET, SOCK_DGRAM)
    sock_broadcast.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock_broadcast.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

    while True:
        try:
            data, addr = sock.recvfrom(1024)
            packet = ArtnetPacket().unpack_raw_artnet_packet(data)
            filename = bufferlocation + 'fd' + str(packet.physical) #create working filename
            if packet.length == 512: #disregard any packets that dont have all 512 bytes of dmx
                if not os.path.exists(filename): #check if file exsists, if not then create and initialize to 0x00
                    print("doesnt exist...creating " + filename)
                    filedict[packet.physical] = os.open(filename, os.O_CREAT | os.O_TRUNC | os.O_RDWR)
                    os.write(filedict[packet.physical], b'\x00' * mmap.PAGESIZE)
                else: # once buffer files created/exist, take artnet data and dump into buffer files, one file per universe(physical)
                    filedict[packet.physical] = os.open(filename, os.O_RDWR)
                    bufferdict[packet.physical] = mmap.mmap(filedict[packet.physical], 0, mmap.MAP_SHARED, mmap.PROT_WRITE)
                    bufferdict[packet.physical].seek(0)
                    bufferdict[packet.physical].write(packet.data)
        except KeyboardInterrupt:
            sock.close()
            sock_broadcast.close()
            sys.exit()