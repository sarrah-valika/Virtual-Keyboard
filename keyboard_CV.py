import mediapipe
import cv2
from cvzone.HandTrackingModule import HandDetector
import pynput
import time

cap=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cap.set(3,1280)
cap.set(4,720) #its a function to expand the dimensions of the video
detector=HandDetector(detectionCon=1, maxHands=2)

#list for the keys
keys=["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P",
    "A", "S", "D", "F", "G", "H", "J", "K", "L",
    "Z", "X", "C", "V", "B", "N", "M", "."]

#make a nested list for they keys 
list_for_keys=[]
width=80
for i in range(len(keys)):
    #if i==0:
       #x=50 
    #else:
    x=(i%9)*100 + 50
    if i<9:
        y=50
    elif i>=9 and i<18:
        y=150
    elif i>=18:
        y=250
    starting_point=(x,y)
    list_for_keys.append((starting_point, (width,width), keys[i]))

print(list_for_keys)

text1=" "#to print the letters in the big box below

t_of_firstclick=0
t_of_lastclick=0

while True:
    scuccess, img = cap.read() #returns a tuple about the success of the image and what the image is 
    img=cv2.flip(img,1) #since webcam display mirror image

    img=detector.findHands(img) #detecting the hand in a box
    lmlist, bboxInfo = detector.findPosition(img) #the finger points are given numbers that are called landmarks. this command returns those landmarks and the green box that surrounds the hand


    #Boiler Plate Code - using code that is available online
    
    
    #loop for making small rectangles
    for i in range (len(list_for_keys)):
        start_point=list_for_keys[i][0]
        sizeofkey=list_for_keys[i][1]
        key=list_for_keys[i][2]
        x,y=start_point
        h,w=sizeofkey
        ending_point=(x+h, y+w)
        cv2.rectangle(img, start_point, ending_point, (0,255,128), cv2.FILLED)
        
        cv2.putText(img, key, (x+20,y+50), cv2.FONT_HERSHEY_PLAIN, 4, (255,255,255), 4)

    if lmlist:
        for i in range (len(list_for_keys)):
            start_point=list_for_keys[i][0]
            sizeofkey=list_for_keys[i][1]
            key=list_for_keys[i][2]
            x1,y1=start_point
            h,w=sizeofkey
            ending_point=(x1+80, y1+80)
            x2, y2 = ending_point

            if x1<lmlist[8][0]<x2 and y1<lmlist[8][1]<y2:
                print(list_for_keys[i])
                print(start_point, ending_point)
                cv2.rectangle(img, start_point, ending_point, (0,155,128), cv2.FILLED)

                cv2.putText(img, key, (x1+20,y1+50), cv2.FONT_HERSHEY_PLAIN, 4, (255,255,255), 4)

                
                length, _ , _ = detector.findDistance(8, 12, img, draw=False)
                if length<=35:
                  t_of_firstclick=time.time()
                  if t_of_firstclick-t_of_lastclick>1:
                    text1=text1+key
                  t_of_lastclick=t_of_firstclick
                  
                
                



    cv2.rectangle(img, (50,350), (700,450), (0,255,255), cv2.FILLED) #to make a rectangle that is displayed on the screen.
    print(text1)
    cv2.putText(img, text1, (70,420), cv2.FONT_HERSHEY_PLAIN, 4, (255,255,255), 4)
    cv2.imshow("Image", img) #display the bits of the picture
    cv2.waitKey(1) #to wait for 1 milisecond



