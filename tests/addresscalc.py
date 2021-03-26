
prevaddr = [0,0]

numleds = 250
bytesperled = 3

nextaddr = [prevaddr[0] + (numleds*bytesperled//512), prevaddr[1] + ((numleds*bytesperled%512)+1)]