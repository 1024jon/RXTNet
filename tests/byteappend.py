universe = 0
address = 0
currentbyte = 0
number_of_leds =  250
bytes_per_led = 3
totalbytes = number_of_leds * bytes_per_led

while currentbyte <= totalbytes:
    if address + bytes_per_led <= 512:
        for b in range(0, bytes_per_led):
            address += 1
            currentbyte += 1
            print(currentbyte, universe, address)
            if currentbyte == totalbytes:
                break
    else:
        universe += 1
        address = 0
    if currentbyte == totalbytes:
        break