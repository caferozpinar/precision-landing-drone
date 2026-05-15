uart = pyb.UART(3, 57600)
uart.init(57600, bits=8, parity=None, timeout=1, flow=0)
a = 2
while True:
    uart.write("%d\n" %(a))
    print(a)
    time.sleep(1)
    a = a + 1