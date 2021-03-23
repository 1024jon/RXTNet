import mmap
import os
import time

filename = '/tmp/buf'
fd = os.open(filename, os.O_RDONLY)

buf = mmap.mmap(fd, 0, mmap.MAP_SHARED, mmap.PROT_READ)

i = 0

while 1:
    buf.seek(0)
    i = bytes(buf.read(752))
    print(i)
    time.sleep(3)

buf.close()
os.close(fd)