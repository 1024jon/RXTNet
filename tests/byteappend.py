universe = 0
address = 1
currentbyte = 1
number_of_leds =  250
bytes_per_led = 3
totalbytes = number_of_leds * bytes_per_led

"""
while currentbyte <= totalbytes:
    for b in range(0, bytes_per_led):
        address += 1
        currentbyte +=1 
        print(currentbyte, universe, address)
        if currentbyte == totalbytes:
            print("break1")
            break
    if currentbyte == totalbytes:
        print("break2")
        break
    universe += 1
    address = 1
    """
    
while currentbyte <= totalbytes:
    for b in range(0, bytes_per_led):
        address += 1
        currentbyte += 1
        print(currentbyte, universe, address)