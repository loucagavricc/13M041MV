import serial
import time
import math

ser = serial.Serial()
ser.baudrate = 115200
ser.port = 'COM3'
ser.parity = 'N'
ser.stopbits = 1
ser.open()
xstart = 1525
ystart = 1525
x = xstart
y = ystart
deg = range(0,360,5)

ser.write(b'{1225,1325}')


while(True):
    for i in deg:
        time.sleep(0.005)
        x = xstart - 300 * math.sin(math.radians(i))
        x = math.floor(x)
        s1 = '{' + str(x) + ',' + str(y) + '}'

        y = ystart - 300 * math.cos(math.radians(i))
        y = math.floor(y)
        s2 = '{' + str(x) + ',' + str(y) + '}'

        ser.write(bytes(s1,encoding='utf-8'))
        time.sleep(0.005)
        ser.write(bytes(s2,encoding='utf-8'))
