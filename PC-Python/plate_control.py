import serial
import time
import math

ser = 0
xstart = 1350
ystart = 1415
x = 1350
y = 1400

## Function for writing to serial
## xToWrite     in range [-250,250]
## yToWrite     in range [-250,250]
##
## Writes difference from start point
def plateControlWrite(xToWrite, yToWrite):
    global d
    global y
    global xstart
    global ystart
    global ser
    
    x = xstart + int(xToWrite)
    y = ystart + int(yToWrite)
    s1 = '{' + str(x) + ',' + str(y) + '}'
    ser.write(bytes(s1,encoding='utf-8'))

##    s2 = '{' + str(x) + ',' + str(y) + '}'
##    ser.write(bytes(s1,encoding='utf-8'))
##    time.sleep(0.005)
##    ser.write(bytes(s2,encoding='utf-8'))
##    time.sleep(0.005)

def plateControlInit(comPort, baudRate):
    global ser
    
    ser = serial.Serial()
    ser.baudrate = baudRate
    ser.port = comPort
    ser.parity = 'N'
    ser.stopbits = 1
    ser.open()
    plateControlWrite(0,0)

def plateControlDeInit():
    ser.close()

def plateControlReset(comPort, baudRate):
    plateControlDeInit()
    plateControlInit(comPort, baudRate)

def plateControlDemo(cntLimit):
    global x
    global y
    global xstart
    global ystart
    global ser

    deg = range(0,360,5)
    time.sleep(1)

    repcnt = 0

    while(repcnt < cntLimit):
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
        repcnt = repcnt + 1

plateControlInit("COM3",115200)
