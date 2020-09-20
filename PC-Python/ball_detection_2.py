import cv2 
import numpy as np
import time
import math
from simple_pid import PID
from plate_control import *
import threading

controlx = 0
controly = 0

def uartThread(threadID):
    global controlx
    global controly
    while(True):
        plateControlWrite(controly, controlx)
        time.sleep(0.01)
    
uartT = threading.Thread(target = uartThread, args=(1,))

def mainThread(threadID):
    global controlx
    global controly
    global uartT
    
    plateControlReset('COM3', 115200)

    cam= cv2.VideoCapture(1)

    while(True):
        ret,img=cam.read(1)
        cv2.imshow('Make plate parallel to image edge',img)
        if(cv2.waitKey(1) != -1):
            break

    cv2.destroyAllWindows()

    # Select ROI
    roi = cv2.selectROI("ROI select",img)
    cv2.destroyAllWindows()

    # Crop
    img = img[int(roi[1]):int(roi[1]+roi[3]),
              int(roi[0]):int(roi[0]+roi[2])] 

    # Select desired ballance point
    bPointReg = cv2.selectROI("Balance point select",img)
    cv2.destroyAllWindows()

    bPointX = int(bPointReg[0] + bPointReg[2]/2)
    bPointY = int(bPointReg[1] + bPointReg[3]/2)

    bPoint = (bPointX, bPointY)

    leave = False

    kpx = ( 300 / bPointX)
    kix = 0
    kdx = 0

    pidControllerx = PID(Kp = kpx, Ki = kix, Kd = kdx, setpoint = bPointX,
                        sample_time = 0.001, output_limits = (-350, 350),
                        auto_mode = True, proportional_on_measurement = False)

    kpy = ( - 300 / bPointY)
    kiy = 0
    kdy = 0

    pidControllery = PID(Kp = kpy, Ki = kiy, Kd = kdy, setpoint = bPointY,
                        sample_time = 0.001, output_limits = (-350, 350),
                        auto_mode = True, proportional_on_measurement = False)

    while True:
        if leave:
            cv2.destroyAllWindows()
            break
        
        # Open frame
        ret,img=cam.read(1)
        
        # Blur
        img = cv2.medianBlur(img,(5))
        
        # Crop
        img = img[int(roi[1]):int(roi[1]+roi[3]),
                  int(roi[0]):int(roi[0]+roi[2])]
        
        # Convert to grayscale 
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
          
        # Blur using 3 * 3 kernel
        gray_blurred = cv2.blur(gray, (3, 3)) 
          
        # Apply Hough transform on the blurred image 
        detected_circles = cv2.HoughCircles(gray_blurred,  
                           cv2.HOUGH_GRADIENT, 1, 20, param1 = 50, 
                       param2 = 30, minRadius = 1, maxRadius = 40) 
          
        # Draw circles that are detected. 
        if detected_circles is not None: 
          
            # Convert the circle parameters a, b and r to integers 
            detected_circles = np.uint16(np.around(detected_circles))

            # Extract center and circumference of detected circle
            a,b,r = detected_circles[0][0]
            
            # Draw the circumference of the circle 
            #cv2.circle(img, (a, b), r, (100, 255, 100), 2)
      
            # Draw a small circle (of radius 1) to show the center
            #cv2.circle(img, (a, b), 1, (100, 100, 255), 3)

            # Draw a small circle (of radius 1) to show the ballancing point
            #cv2.circle(img, bPoint, 1, (100, 100, 255), 3)

            # Draw error line from desired ballance point
            #cv2.line(img, (a, b), bPoint, (255, 100, 100), 1)

            
            #cv2.imshow("Detected Circle", img) 
            #if(cv2.waitKey(1) != -1):
            #    leave = True

        #errorx = bPointX - a
        #errory = bPointY - b

        controlx = pidControllerx(a)
        controly = pidControllery(b)
        if(uartT.is_alive() == False):
            uartT.start()

    ##    print('Error x: ' + str(errorx)
    ##          + ' Error y: ' + str(errory)
    ##          + ' Control x: ' + str(controlx)
    ##          + ' Control y: ' + str(controly))

    ##    if (controly > 10 or controly < -10):
    ##        plateControlWrite(controly, 0)
    ##        
    ##    time.sleep(0.01)
    ##    
    ##    if (controlx > 10 or controlx < -10):
    ##        plateControlWrite(0, controlx)   

mainT = threading.Thread(target = mainThread, args=(2,))
mainT.start()
