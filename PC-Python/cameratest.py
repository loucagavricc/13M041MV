import numpy as np
import cv2
import tkinter
import queue
import threading

q1 = queue.Queue(maxsize=1)
q2 = queue.Queue(maxsize=1)
q3 = queue.Queue(maxsize=1)
q4 = queue.Queue(maxsize=1)

def putOnQueue1(val):
    if(q1.full() == False):
        q1.put(val)

def putOnQueue2(val):
    if(q2.full() == False):
        q2.put(val)
        
def putOnQueue3(val):
    if(q3.full() == False):
        q3.put(val)
        
def putOnQueue4(val):
    if(q4.full() == False):
        q4.put(val)

def tkScaleThread():
    root = tkinter.Tk()
    scale1 = tkinter.Scale(root, orient='horizontal', from_=0, to=255, command=putOnQueue1)
    scale2 = tkinter.Scale(root, orient='horizontal', from_=0, to=255, command=putOnQueue2)
    scale3 = tkinter.Scale(root, orient='horizontal', from_=0, to=10, resolution=0.01, command=putOnQueue3)
    scale4 = tkinter.Scale(root, orient='horizontal', from_=0, to=30, command=putOnQueue4)
    scale1.pack()
    scale2.pack()
    scale3.pack()
    scale4.pack()
    scale1.set(100)
    scale2.set(200)
    scale3.set(1.41)
    scale4.set(7)
    root.mainloop()

def imgThread(inQueue1, inQueue2, inQueue3, inQueue4):
    cap = cv2.VideoCapture(1)
    thresh1 = 100 
    thresh2 = 200
    blur = 1.41
    bmat = 7
    
    while(True):
        if(inQueue1.full() == True):
            thresh1 = inQueue1.get()
            
        if(inQueue2.full() == True):
            thresh2 = inQueue2.get()
            
        if(inQueue3.full() == True):
            blur = inQueue3.get()
            
        if(inQueue4.full() == True):
            bmat = inQueue4.get()
            bmat = int(bmat)
            if(bmat%2 == 0):
                bmat=bmat-1
        
        # Capture frame-by-frame
        ret, frame = cap.read()

        thresh1 = int(thresh1)
        thresh2 = int(thresh2)
        blur = float(blur)
        bmat = int(bmat)    

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        gray = cv2.GaussianBlur(gray, (bmat,bmat), blur)

        # Our operations on the frame come here
        canny = cv2.Canny(gray, thresh1, thresh2)

        # Display the resulting frame
        cv2.imshow('frame',canny)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    
t1 = threading.Thread(target = tkScaleThread, args =( )) 
t2 = threading.Thread(target = imgThread, args =(q1,q2,q3,q4, )) 
t1.start() 
t2.start() 


