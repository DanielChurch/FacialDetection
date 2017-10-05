#Imports
import numpy as np
import cv2 as cv

from tkinter import Tk
from tkinter import filedialog

#Window delcarations
default_window = 'normal';
cv.namedWindow(default_window);
           
#No TK Window
Tk().withdraw();

filename = filedialog.askopenfilename();

img = cv.imread(filename);

face_cascade = cv.CascadeClassifier("C:\\Users\\Dan\\Documents\\OpenCV\\scenes\\haarcascade_frontalface_default.xml")
eye_cascade = cv.CascadeClassifier("C:\\Users\\Dan\\Documents\\OpenCV\\scenes\\haarcascade_eye.xml")

gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY);
faces = face_cascade.detectMultiScale(gray, 1.3, 5);

width = img.shape[1];
height = img.shape[0];

global face;
face = faces[0]

faceImage = img.copy();

for index, item in enumerate(faces):
    faceImage = img.copy();
    (x,y,w,h) = item;
    cv.rectangle(faceImage, (x,y), (x+w,y+h), (255,0,0), 2);
    txtImage = faceImage.copy();
    retval, baseLine = cv.getTextSize("Correct? (y/n)", 0, 2, 1);
    print(height)
    cv.putText(txtImage, "Correct? (y/n)", (int((width-retval[0])/2),int(height*3/4)), 0, 2, (0,0,255));
    cv.imshow(default_window, txtImage);
    key = cv.waitKey() & 0xff;
    if(key == 121):
        face = faces[index];
        break;
cv.imshow(default_window, faceImage);
cv.waitKey(0)

while True:
    (x,y,w,h) = face;
    key = cv.waitKey() & 0xff;
    if(key == 97): #A
        x = x - 1;
    elif (key == 100): #S 
        x = x + 1;
    elif (key == 115): #D
        y = y + 1;
    elif (key == 119): #W
        y = y - 1;
    elif key == 108: # right arrow
        w = w + 1;
    elif key == 106: # left arrow
        w = w - 1;
    elif key == 105: # up arrow
        h = h - 1;
    elif key == 107: # down arrow
        h = h + 1;
    elif key == 13:
        break;
    face = (x,y,w,h);
    faceImage = img.copy();
    cv.rectangle(faceImage, (x,y), (x+w,y+h), (255,0,0), 2);
    cv.imshow(default_window, faceImage);

(fx,fy,fw,fh) = face;
roi_gray = gray[fy:fy+fh, fx:fx+fw];
roi_color = faceImage[fy:fy+fh, fx:fx+fw];
eyes = eye_cascade.detectMultiScale(roi_gray);

eye = [eyes[0], eyes[1]];
count = 0;

eyesImage = roi_color.copy();
for index, item in enumerate(eyes):
    eyeCopy = eyesImage.copy();
    (x,y,w,h) = item;
    cv.rectangle(eyeCopy, (x,y), (x+w,y+h), (0,255,0), 2);
    txtImage = eyeCopy.copy();
    cv.putText(txtImage, "Correct?", (0,width), 0, 2, (0,0,255));
    
    outputImage = np.zeros((img.shape[0], img.shape[1], 3), np.uint8);
    outputImage[fy:fy+fh, fx:fx+fw] = txtImage[0:fh, 0:fw];
    
    cv.imshow(default_window, outputImage);
    key = cv.waitKey() & 0xff;
    if(key == 121):
        eye[count] = item;
        while True:
            (x,y,w,h) = eye[count];
            key = cv.waitKey() & 0xff;
            if(key == 97): #A
                x = x - 1;
            elif (key == 100): #S 
                x = x + 1;
            elif (key == 115): #D
                y = y + 1;
            elif (key == 119): #W
                y = y - 1;
            elif key == 108: # right arrow
                w = w + 1;
            elif key == 106: # left arrow
                w = w - 1;
            elif key == 105: # up arrow
                h = h - 1;
            elif key == 107: # down arrow
                h = h + 1;
            elif key == 13:
                break;
            eye[count] = (x,y,w,h);
            eyeCopy = eyesImage.copy();
            cv.rectangle(eyeCopy, (x,y), (x+w,y+h), (0,255,0), 2);
            
            outputImage = np.zeros((img.shape[0], img.shape[1], 3), np.uint8);
            outputImage[fy:fy+fh, fx:fx+fw] = eyeCopy[0:fh, 0:fw];
            
            cv.imshow(default_window, outputImage);
        cv.rectangle(eyesImage, (x,y), (x+w,y+h), (0,255,0), 2);
        count=count+1;
        if(count == 2):
            break;

xvel = 1;
yvel = 1;

hsv = cv.cvtColor(eyesImage, cv.COLOR_BGR2HSV);

while True:
    if(fx <= 0 or fx + fw >= width-(xvel-1)):
        xvel = xvel * -1;
        (e1x, e1y, e1w, e1h)= eye[0];
        (e2x, e2y, e2w, e2h)= eye[1];
        
        hsv[e1y:e1y+e1h, e1x:e1x+e1w,2] -= 10
        hsv[e2y:e2y+e2h, e2x:e2x+e2w,2] -= 10
        
        eyesImage = cv.cvtColor(hsv, cv.COLOR_HSV2BGR)
    if(fy <= 0 or fy + fh >= height-(yvel-1)):
        yvel = yvel * -1;
        
    fx = fx + xvel;
    fy = fy + yvel;
    
    outputImage = np.zeros((img.shape[0], img.shape[1], 3), np.uint8);
    outputImage[fy:fy+fh, fx:fx+fw] = eyesImage[0:fh, 0:fw];
    
    cv.imshow(default_window, outputImage);
    
    k = cv.waitKey(1) & 0xff;
    if(k == 27):
        break;
cv.destroyAllWindows();