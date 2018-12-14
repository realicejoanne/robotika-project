import numpy as np
import cv2
import imutils
import serial
import time

# Always changes !!IMPORTANT TO CHECK!!
# Capture the video from the following IP address
cap = cv2.VideoCapture("http://10.202.105.13:8080/video")

# Serial variable to send data to Arduino
ser1 = serial.Serial('COM12', 9600)

while(True):
    # Hue, Saturation, Value of the obejct that needs to be tracked
    h, s, v = 0, 0, 130

    # Decodes and read the next frame
    ret, frame = cap.read()
    frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

    # Varibles for the width, height, and channel of the frame
    height, width, channel = frame.shape

    # Set the maximum and minimum boundries HSV value of the object
    BLUE_MIN = np.array([110, 50, 50], np.uint8)
    BLUE_MAX = np.array([130, 255, 255], np.uint8)

    # Converts the image in the frame to an HSV color space one
    hsv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Checks if the HSV value of the frame is within boundries defined 
    frame_threshed = cv2.inRange(hsv_img, BLUE_MIN, BLUE_MAX)

    # Define the Kernel size for image processing
    kernel = np.ones((10, 10), np.uint8)

    # I dont know what this does :)
    opening = cv2.morphologyEx(frame_threshed, cv2.MORPH_OPEN, kernel)

    # Redefine the Kernel size
    kernel = np.ones((20, 20), np.uint8)

    # Dilates the image
    dilation = cv2.dilate(opening, kernel, iterations=1)

    # Find contours in the thresholded image
    cnts = cv2.findContours(
        dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]

    # Variables of bondaries that denotes the middle of the robot's vision
    boundLeft = int(width * 0.40)
    boundRight = int(width * 0.60)

    # Loops over the contours
    for c in cnts:

        # Gets the biggest contour value
        con = max(cnts, key=cv2.contourArea)
        
        # Compute for the center of the contour
        M = cv2.moments(con)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        # Draw the contour and center of the shape on the image
        cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)

        # Define the x, y coordinates; width and height of the bounding object
        x, y, w, h = cv2.boundingRect(con)
        
        # Create a bounding rectangle based on the largest contour value
        # cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)

        # Define the center, radius of the bounding circle
        #(x, y), radius = cv2.minEnclosingCircle(con)
        #center = (int(x), int(y))
        #radius = int(radius)

        # Draw a grey dot in the center of the object
        cv2.circle(frame, (cX, cY), 7, (255, 255, 255), -1)

        # Draw the bounding circle based on the center and radius
        #cv2.circle(frame, center, radius, (255, 255, 0), 2)

        # Draw a vertical line that intersects the center of the object
        # cv2.line(frame, (int(x), int(y-h/2)),
        #          (int(x), int(y+h/2)), (255, 0, 0), 5)

        # Draw the robot's middle boundaries
        cv2.line(frame, (boundLeft, 0), (boundLeft, height), (255, 0, 0), 3)
        cv2.line(frame, (boundRight, 0), (boundRight, height), (255, 0, 0), 3)

        # Checks the position of the object relative to the boundaries
        if cX > boundRight:
            # Move to the right --- 1
            ser1.write('1'.encode())
            print("Kanan")
        elif cX < boundLeft:
            # Move to the left 	--- 2
            ser1.write('2'.encode())
            print("Kiri")
        else:
            # Forward
            ser1.write('3'.encode())
            print("Maju")

    # Display the image
    cv2.imshow("Image", frame)
    #time.sleep(10)
    #ser1.write('0'.encode())
    #print("Not Detected")

    # Close the program if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        ser1.write('2'.encode())
        break

cap.release()
cv2.destroyAllWindows()	