import mmap
import os

bufferfile = '/tmp/buf'

## create and initialize file with code like this
#fd = os.open(filename, os.O_CREAT | os.O_TRUNC | os.O_RDWR)
#os.write(fd, '\x00' * mmap.PAGESIZE)

fd = os.open(bufferfile, os.O_RDWR)
buf = mmap.mmap(fd, 0, mmap.MAP_SHARED, mmap.PROT_WRITE)

while 1:
    buf.seek(0)
    packet = bytearray(b'\x01')
    packet.append(3)
    for l in range(0,750):
        packet.append(ord(os.urandom(1)))
    
    buf.write(bytes(packet))
    print(packet)
    #buf.flush()
    input('ENTER')
    
buf.close()
os.close(fd)