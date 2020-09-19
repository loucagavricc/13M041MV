import cv2
import numpy as np
#import serial
from time import sleep
import math
#import threading

##def timerThread():
##    time.sleep(0.01)
##    threading.notify()
##
##def pidLoopThread(x_q, y_q):
##    threading.notify()
##             
##
##def ballDetectThread(x_q, y_q):

kernelOpen=np.ones((5,5))
kernelClose=np.ones((20,20))
cam= cv2.VideoCapture(1)

#show image
#rotate camera if needed
#any button to resume
while(True):
    ret,img=cam.read(1)
    cv2.imshow('img',img)
    if(cv2.waitKey(1) != -1):
        break

cv2.destroyAllWindows()

# Select ROI
r = cv2.selectROI(img)
cv2.destroyAllWindows()

while True:
    #open frame
    ret,img=cam.read(1)
    #blur
    img = cv2.medianBlur(img,(5))
    #crop
    img = img[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
    #convert to gray
    imggray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #invert
    imggray = cv2.bitwise_not(imggray)
    #find threshold
    retval, threshold = cv2.threshold(imggray,50,255,cv2.THRESH_BINARY)
    #morphological opening
    maskOpen=cv2.morphologyEx(threshold,cv2.MORPH_OPEN,kernelOpen)
    #morphological closing
    maskClose=cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose)
    #get and draw contours
    contours,hierarchy=cv2.findContours(maskClose,
                                        cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)  
    cv2.drawContours(img,contours,-1,(0,255,0),3)
    #check if ball on plate
    if len(contours)>0:
        cnt=contours[0]
        #find circle parameters of the ball
        (x,y),radius=cv2.minEnclosingCircle(cnt)
        center=(int(x),int(y))
        radius=int(radius)
        #draw circle
        cv2.circle(img,center,radius,(0,255,0),2)
        label = str(int(y))+','+str(int(x))
        cv2.putText(img, label, center,
                    cv2.FONT_HERSHEY_PLAIN, 1.0, (200,100,100), 2);

        
##        if(x_q.full() == False):
##            x_q.put(x)
##            
##        if(y_q.full() == False):
##            y_q.put(y)
    
##        x=int(x)
##        print(x)
##        a=x%10
##        x=x/10
##        b=x%10
##        x=x/10

##        ser.write(str(x))
##        ser.write(str(b))
##        ser.write(str(a))        
##        y=int(y)
##        print(y)
##        d=y%10
##        y=y/10
##        e=y%10
##        y=y/10

##        ser.write(str(y))
##        ser.write(str(e))
##        ser.write(str(
        
    #show image with contours    
    cv2.imshow('img',img)
    if(cv2.waitKey(1) != -1):
        break

##q1 = queue.Queue(maxsize=1)
##q2 = queue.Queue(maxsize=1)
##t1 = threading.Thread(target = pidLoopThread, args =(q1,q2, )) 
##t2 = threading.Thread(target = ballDetectThread, args =(q1,q2, )) 
##t1.start() 
##t2.start()

cv2.destroyAllWindows()
